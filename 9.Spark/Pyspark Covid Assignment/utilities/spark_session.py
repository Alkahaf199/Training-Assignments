from pyspark.sql import SparkSession

def get_spark_session(app_name="covidAnalysis"):
    spark = SparkSession.builder.master("local[*]").appName(app_name).getOrCreate()
    return spark
