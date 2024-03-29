# Databricks notebook source
from pyspark.sql.types import StructType, StructField, IntegerType, DateType, StringType
from pyspark.sql.functions import *

# Create a Spark session
spark = SparkSession.builder \
    .appName("Export to MySQL") \
    .config("spark.driver.extraClassPath", "/path/to/mysql-connector-java.jar") \
    .getOrCreate()


# COMMAND ----------

salesSchema = StructType([
    StructField("ProductId", IntegerType(), True),
    StructField("CustomerId", StringType(), True),
    StructField("Date", DateType(), True),
    StructField("Location", StringType(), True),
    StructField("Source", StringType(), True),
    StructField("Quantity", IntegerType(), True),
])

# COMMAND ----------

salesDF = spark.read.schema(salesSchema).option("header", "True").csv("dbfs:/FileStore/sales.csv")

# COMMAND ----------

salesDF.printSchema()

# COMMAND ----------

salesDF = salesDF.dropna(subset=["CustomerId"])
salesDF.count()

# COMMAND ----------

productSchema = StructType([
    StructField("ProductId", IntegerType(), True),
    StructField("Name", StringType(), True),
    StructField("Price", IntegerType(), True),
])

# COMMAND ----------

productsDF = spark.read.schema(productSchema).csv("dbfs:/FileStore/products.csv")

# COMMAND ----------

productsDF.printSchema()

# COMMAND ----------

q1 = salesDF.groupBy("CustomerId", "ProductId").agg(sum("Quantity").alias("count"))
q1 = q1.join(productsDF, "ProductId").withColumn("Amount", col("Price")*col("count")).groupBy("CustomerId").agg(sum("Amount").alias("Total Amount"))
q1.show()

# COMMAND ----------

q1 = salesDF.join(productsDF, "ProductId").withColumn("Amount", col("Price")*col("Quantity")).groupBy("CustomerId").agg(sum("Amount").alias("Total Amount"))
q1.show()

# COMMAND ----------

q2 = salesDF.groupBy("ProductId").count().join(productsDF, "ProductId").select("ProductId", "Name", (col("count")*col("Price")).alias("Total Amount"))
q2.show()

# COMMAND ----------

monthly_sales = salesDF \
    .groupBy(date_format("Date", "MMMM").alias("Month"), month("Date").alias("MonthNumber"), "ProductId") \
    .agg(sum("Quantity").alias("Count")) \
    .join(productsDF, "ProductId") \
    .withColumn("Amount", col("Count") * col("Price")) \
    .groupBy("Month", "MonthNumber") \
    .agg(sum("Amount").alias("Sales")) \
    .orderBy("MonthNumber") \
    .select("Month", "Sales")
monthly_sales.show()

# COMMAND ----------

yearly_sales = salesDF \
    .join(productsDF, "ProductId") \
    .withColumn("Amount", col("Quantity")*col("Price")) \
    .groupBy(year("Date").alias("Year")) \
    .agg(sum("Amount").alias("Sales")) \
    .orderBy("Year")
yearly_sales.show()

# COMMAND ----------

quarterly_sales = salesDF \
    .join(productsDF, "ProductId") \
    .withColumn("Amount", col("Quantity") * col("Price")) \
    .groupBy(year("Date").alias("Year"), quarter("Date").alias("Quarter")) \
    .agg(sum("Amount").alias("QuarterlySales")) \
    .orderBy("Year", "Quarter")
quarterly_sales.show()

# COMMAND ----------

orders_by_category = salesDF.groupBy("ProductId").agg(sum("Quantity").alias("Count")).join(productsDF, "ProductId").select("ProductId", "Name", "Count")
orders_by_category.sort("ProductId").show()

# COMMAND ----------

orders_by_category.orderBy(desc("Count")).limit(5).show()

# COMMAND ----------

customer_visit_frequency = salesDF \
    .groupBy("CustomerId") \
    .agg(count("*").alias("VisitFrequency"))

customer_visit_frequency.show()

# COMMAND ----------

distinct_locations = salesDF.select("Location").distinct()
distinct_locations.show()

# COMMAND ----------

exchange_rates = {"USA": 1.0, "UK": 0.79, "India": 83.0}
sales_by_country = salesDF.join(productsDF, "ProductId") \
    .withColumn("Amount", col("Price")*col("Quantity")) \
    .groupBy("Location") \
    .agg(sum("Amount").alias("Total Sales USD")) \
    .withColumn("Total Sales Local Currency", col("Total Sales USD")*when(col("Location") == "USA", 1.0).when(col("Location") == "UK", exchange_rates["UK"]).when(col("Location") == "India", exchange_rates["India"]))
sales_by_country.show()

# COMMAND ----------

sales_by_source = salesDF.join(productsDF, "ProductId") \
    .withColumn("Amount", col("Price")*col("Quantity")) \
    .groupBy("Source") \
    .agg(sum("Amount").alias("Sales"))
sales_by_source.show()

# COMMAND ----------


