from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType
import configparser

def read_database_credentials():
    config = configparser.ConfigParser()
    config.read('config.ini')
    mysql_url = config['database']['url']
    mysql_user = config['database']['user']
    mysql_password = config['database']['password']
    return mysql_url, mysql_user, mysql_password

def read_sales_data(spark):
    sales_schema = StructType([
        StructField("Product Id", IntegerType(), True),
        StructField("Customer Id", StringType(), True),
        StructField("Date", DateType(), True),
        StructField("Location", StringType(), True),
        StructField("Source", StringType(), True),
        StructField("Quantity", IntegerType(), True),
    ])
    sales_df = spark.read.schema(sales_schema).option("header", "True").csv("data/sales.csv")
    return sales_df.dropna(subset=["Customer Id"])

def read_products_data(spark):
    product_schema = StructType([
        StructField("Product Id", IntegerType(), True),
        StructField("Name", StringType(), True),
        StructField("Price", IntegerType(), True),
    ])
    return spark.read.schema(product_schema).option("header", "False").csv("data/products.csv")
