import http.client
import ssl
import csv
import json

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Function to make the API request
def make_request():
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
        statistics = json_data['response']
        write_to_csv(statistics)
    else:
        print("No data available.")

# Function to write data to CSV file
def write_to_csv(statistics):
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

    # CSV file name
    csv_file = "covid_statistics.csv"

    # Flattened CSV fieldnames (headers)
    fieldnames = set()
    for stat in statistics:
        flattened_stat = flatten_dict(stat)
        fieldnames.update(flattened_stat.keys())

    # Writing data to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for stat in statistics:
            flattened_stat = flatten_dict(stat)
            writer.writerow(flattened_stat)

    print("Data written to", csv_file)

# Call the function to make the request
make_request()
