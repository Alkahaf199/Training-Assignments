import http.client
import ssl
import json
import csv
import yaml
from pyspark.sql import SparkSession
from utilities.config_loader import get_config

class InputData(object):
    def __init__(self, spark):
        self.spark = spark
        self.config = get_config()
        self.CSVfname = self.config['csv']['filename']

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
    
        conn = http.client.HTTPSConnection(self.config['api']['url'])

        headers = {
            'X-RapidAPI-Key': self.config['api']['key'],
            'X-RapidAPI-Host': self.config['api']['host']
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
