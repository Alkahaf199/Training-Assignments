from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession

class Analysis(object):
    def __init__(self, spark: SparkSession, DF: DataFrame):
        self.spark = spark
        self.data = DF
    
    def __showTable(self, df):
        # Collect data and column names as lists
        data = df.collect()
        columns = list(df.columns)

        # Build the HTML table string
        html = ["<table>"]

        # Create the header row
        html.append("  <tr>")
        for col in columns:
            html.append(f"    <th>{col}</th>")
        html.append("  </tr>")

        # Add data rows
        for row in data:
            html.append("  <tr>")
            for value in row:
                html.append(f"    <td>{value}</td>")
            html.append("  </tr>")

        html.append("</table>")
        return "".join(html)
    
    def showData(self):
        return self.__showTable(self.data)
    
    def deathsByCases(self, type="min"):
        if type == "max":
            aggregation_func = max
        else:
            aggregation_func = min

        # Calculate the ratio of total deaths to total COVID-19 cases
        covidData = self.data.withColumn("death_to_cases_ratio", col("deaths_total") / col("cases_total"))

        # Calculate the maximum ratio
        max_ratio = covidData.agg(aggregation_func(col("death_to_cases_ratio")).alias("max_ratio")).collect()[0]["max_ratio"]

        # Filter out the countries with ratios equal to the maximum
        result = covidData.filter(col("death_to_cases_ratio") == max_ratio).select("country", "death_to_cases_ratio")
        
        return self.__showTable(result)
    
    def casesWise(self, type="max"):
        if type == "min":
            aggregation_func = min
        else:
            aggregation_func = max

        # Calculate the maximum number of COVID-19 cases
        max_cases = self.data.agg(aggregation_func(col("cases_total")).alias("max_cases")).collect()[0]["max_cases"]

        # Filter the original DataFrame to include data only for the country with the highest cases
        result = self.data.select("country").filter(col("cases_total") == max_cases)
        return self.__showTable(result)

    def totalCases(self):
        result = self.data.select(sum("cases_total").alias("Total Cases"))
        return self.__showTable(result)

    def recoveryPerCase(self, type="max"):
        if type == "min":
            aggregation_func = min
        else:
            aggregation_func = max

        # Calculate the efficiency ratio of total recoveries to total COVID-19 cases
        covidData = self.data.withColumn("efficiency_ratio", col("cases_recovered") / col("cases_total"))

        # Calculate the maximum efficiency ratio
        max_efficiency_ratio = covidData.agg(aggregation_func(col("efficiency_ratio")).alias("max_efficiency_ratio")).collect()[0]['max_efficiency_ratio']

        # Filter the original DataFrame to include data only for the country with the maximum efficiency ratio
        result = covidData.select("country", "efficiency_ratio").filter(col("efficiency_ratio") == max_efficiency_ratio)
        return self.__showTable(result)

    def criticalWise(self, type="max"):
        if type == "min":
            aggregation_func = min
        else:
            aggregation_func = max

        value = self.data.agg(aggregation_func("cases_critical").alias("critical")).collect()[0]['critical']

        result = self.data.filter(col("cases_critical") == value).select("country", "cases_critical")
        return self.__showTable(result)
