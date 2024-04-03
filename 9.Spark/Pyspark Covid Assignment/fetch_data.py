import http.client
import ssl
import json
import csv
from pyspark.sql.types import *
from pyspark.sql import SparkSession

class InputData(object):
    def __init__(self, spark,CSVfname = "covid_data.csv"):
        self.spark = spark
        self.CSVfname = CSVfname

    def __write_to_csv(self, data, filename):
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

    def loadJSON(self):

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
        data = json_data['response']

        self.__write_to_csv(data, self.CSVfname)

        covidData = self.spark.read.option("inferSchema", "True").option("header", "true").csv(self.CSVfname)
        covidData = covidData.filter(covidData.continent != covidData.country)
        print("Filling null values")
        covidData = covidData.fillna(0, ["deaths_total", "cases_recovered", "cases_critical", "cases_active"])

        return covidData

