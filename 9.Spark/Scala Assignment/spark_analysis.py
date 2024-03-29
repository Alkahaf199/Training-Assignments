from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession

from index import create_spark_dataframe


class SparkAnalysis(object):

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def create_spark_dataframe():
        covidData = spark.read.option("inferSchema", "True").option("header", "true").csv(dataFile)
        covidData.printSchema()
        # Neglecting the data which is based on continents
        covidData = covidData.filter(covidData.continent != covidData.country)
        print("Filling null values")
        covidData = covidData.fillna(0, ["deaths_total", "cases_recovered", "cases_critical", "cases_active"])
        return covidData


dataFile = "covid_data.csv"
spark = SparkSession.builder.master("local[*]").appName("CovidApp").getOrCreate()


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

# covidData = spark.read.schema(covidSchema).option("header", "true").csv(dataFile)
covidData = spark.read.option("inferSchema", "True").option("header", "true").csv(dataFile)
covidData.printSchema()
    # Neglecting the data which is based on continents
covidData = covidData.filter(covidData.continent != covidData.country)
print("Filling null values")
covidData = covidData.fillna(0, ["deaths_total", "cases_recovered", "cases_critical", "cases_active"])
print("Running first query")

query1 = covidData.groupBy("country").agg(max(covidData.deaths_total/covidData.cases_total).alias("ratio"))
maxValue = query1.agg(max(col("ratio")).alias("max_ratio")).collect()[0]["max_ratio"]

result = query1.filter(col("ratio") == maxValue).select("country")
result.show()
print("Stopping")
spark.stop()

