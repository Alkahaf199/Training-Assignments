import http.client
import ssl
import csv
import json
import requests
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import http.server
import socketserver



# Step 1: Make a request to the COVID-19 API and collect data for at least 20 countries
def fetch_covid_data():

    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    
    conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "65c3050d7cmsha83ea2591ea05d3p11a4a1jsn5b2f7d9e6464",
        'X-RapidAPI-Host': "covid-193.p.rapidapi.com"
    }

    conn.request("GET", "/statistics", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Parse JSON data
    json_data = json.loads(data)

    # Check if data is available
    if json_data.get('response'):
        return json_data['response']
    else:
        print("No data available.")

# Step 2: Write the data to a CSV file
def write_to_csv(data, filename):
    # Recursive function to flatten nested dictionaries
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Flattened CSV fieldnames (headers)
    fieldnames = set()
    for stat in data:
        flattened_stat = flatten_dict(stat)
        fieldnames.update(flattened_stat.keys())

    # Writing data to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for stat in data:
            flattened_stat = flatten_dict(stat)
            writer.writerow(flattened_stat)

    print("Data written to", filename)

# Step 3: Create a Spark DataFrame from the CSV file
def create_spark_dataframe(filename):
    spark = SparkSession.builder.appName("CovidApp").getOrCreate()
    covidSchema = StructType([
        StructField("total_cases", IntegerType(), True),
        StructField("country", StringType(), True),
        StructField("total_deaths", IntegerType(), True),
        StructField("total_tests", IntegerType(), True),
        StructField("new_cases", IntegerType(), True),
        StructField("new_deaths", IntegerType(), True),
        StructField("population", LongType(), True),
        StructField("tests_1M_pop", IntegerType(), True),
        StructField("date", DateType() , True),
        StructField("deaths_1M_pop", IntegerType(), True),
        StructField("cases_1M_pop", IntegerType(), True),
        StructField("critical", IntegerType(), True),
        StructField("active", IntegerType(), True),
        StructField("recovered", IntegerType(), True),
        StructField("time", TimestampType(), True),
        StructField("continent", StringType(), True),
    ])

    covidData = spark.read.schema(covidSchema).option("header", "true").csv(filename)

    # Neglecting the data which is based on continents
    covidData = covidData.filter(covidData.continent != covidData.country)
    covidData = covidData.fillna(0, ["total_deaths", "recovered", "critical", "active"])
    
    return covidData

# Step 4: Perform computations and analysis to answer the questions
def analyze_covid_data(db):

    most_affected_country = db.select("country",round((db.total_deaths/db.total_cases),6).alias("ratio")).where(col("ratio") != 0).sort(desc("ratio")).limit(1)
    most_affected_country.show()

    least_affected_country = db.select("country",round((db.total_deaths/db.total_cases),6).alias("ratio")).sort("ratio").limit(1)

    country_with_highest_cases = db.select("country", "total_cases").sort(desc("total_cases")).limit(1)

    country_with_minimum_cases = db.select("country", "total_cases").sort("total_cases").limit(1)

    total_cases = db.select(sum("total_cases").alias("Total Cases"))

    most_efficient_country = db.select("country", round((db.recovered/db.total_cases),6).alias("Recovery Ratio")).where(col("Recovery Ratio").isNotNull()).sort(desc("Recovery Ratio")).limit(1)

    least_efficient_country = db.select("country", round((db.recovered/db.total_cases),6).alias("Recovery Ratio")).sort("Recovery Ratio", "country").limit(1)

    country_least_suffering = db.select("country").sort("critical", "country").limit(1)

    country_most_suffering = db.select("country", "critical", "continent").sort(desc("critical"), "country").limit(1)

    return {
        "most_affected_country": most_affected_country.toJSON().collect(),
        "least_affected_country": least_affected_country.toJSON().collect(),
        "country_with_highest_cases": country_with_highest_cases.toJSON().collect(),
        "country_with_minimum_cases": country_with_minimum_cases.toJSON().collect(),
        "total_cases": total_cases.toJSON().collect(),
        "most_efficient_country": most_efficient_country.toJSON().collect(),
        "least_efficient_country": least_efficient_country.toJSON().collect(),
        "country_least_suffering": country_least_suffering.toJSON().collect(),
        "country_most_suffering": country_most_suffering.toJSON().collect()
    }

if __name__ == "__main__":

    def run_handler(query_name, db):
        handlers = {
            "mostAffected": lambda db: analyze_covid_data(db)["most_affected_country"],
            "leastAffected": lambda db: analyze_covid_data(db)["least_affected_country"],
            "highestCases": lambda db: analyze_covid_data(db)["country_with_highest_cases"],
            "lowestCases": lambda db: analyze_covid_data(db)["country_with_minimum_cases"],
            "totalCases": lambda db: analyze_covid_data(db)["total_cases"],
            "mostEfficient": lambda db: analyze_covid_data(db)["most_efficient_country"],
            "leastEfficient": lambda db: analyze_covid_data(db)["least_efficient_country"],
            "highestCritical": lambda db: analyze_covid_data(db)["country_most_suffering"],
            "lowestCritical": lambda db: analyze_covid_data(db)["country_least_suffering"]
        }
        if query_name in handlers:
            return handlers[query_name](db)
        else:
            return None
        
    
    jsonData = fetch_covid_data()
    filename = "covid_data.csv"
    write_to_csv(jsonData, filename)
    db = create_spark_dataframe(filename)
    print("Data fetched and loaded into DataFrame")  # Display message


    class service(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
        # Extract request path and query parameters
            request_path = self.path.split("/")[-1]

            if request_path == '':
            # Handle home path request
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Welcome to COVID data</h1><ul>"
                              b"<li><a href='/mostAffected'>Most Affected Countries</a></li>"
                              b"<li><a href='/leastAffected'>Least Affected Countries</a></li>"
                              b"<li><a href='/highestCases'>Countries with Highest Cases</a></li>"
                              b"<li><a href='/lowestCases'>Countries with Lowest Cases</a></li>"
                              b"<li><a href='/totalCases'>Total Cases</a></li>"
                              b"<li><a href='/mostEfficient'>Most Efficient Countries</a></li>"
                              b"<li><a href='/leastEfficient'>Least Efficient Countries</a></li>"
                              b"<li><a href='/highestCritical'>Countries with Highest Critical Cases</a></li>"
                              b"<li><a href='/lowestCritical'>Countries with Lowest Critical Cases</a></li>"
                              b"</ul></body></html>")
                # Fetch data, write to CSV, and create DataFrame
                
            else:
                # Run specific query handler if it exists
                response = run_handler(request_path, db)
                if response:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    beautified_json = json.dumps(response, indent=4)  # Beautify JSON with indentation
                    self.wfile.write(beautified_json.encode())
                else:
                    self.send_error(404, "Not Found")

    class MyTCPServer(socketserver.TCPServer):
        def server_close(self):
            super().server_close()
            print("Socket released.")

    HOST = 'localhost'
    PORT = 8000
    with MyTCPServer((HOST, PORT), service) as httpd:
        print(f"Serving at http://{HOST}:{PORT}")
        httpd.serve_forever()

