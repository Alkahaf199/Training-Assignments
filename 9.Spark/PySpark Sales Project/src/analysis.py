from pyspark.sql.functions import *
from pyspark.sql import DataFrame

def calculate_customer_expense(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for customer expense
    result_df = sales_df.groupBy("Customer Id", "Product Id").agg(sum("Quantity").alias("count"))
    result_df = result_df.join(product_df, "Product Id") \
            .withColumn("Amount", col("Price")*col("count")) \
            .groupBy("Customer Id") \
            .agg(sum("Amount").alias("Total Amount"))

    # result_df = sales_df.join(product_df, "Product Id").withColumn("Amount", col("Price")*col("Quantity")).groupBy("Customer Id").agg(sum("Amount").alias("Total Amount"))

    return result_df

def calculate_category_expense(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for category expense
    result_df = sales_df.groupBy("Product Id").count() \
        .join(product_df, "Product Id") \
        .select("Product Id", "Name", (col("count")*col("Price")).alias("Total Amount"))
    
    return result_df

def calculate_monthly_sales(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for quarterly sales
    result_df = sales_df \
        .groupBy(date_format("Date", "MMMM").alias("Month"), month("Date").alias("MonthNumber"), "Product Id") \
        .agg(sum("Quantity").alias("Count")) \
        .join(product_df, "Product Id") \
        .withColumn("Amount", col("Count") * col("Price")) \
        .groupBy("Month", "MonthNumber") \
        .agg(sum("Amount").alias("Sales")) \
        .orderBy("MonthNumber") \
        .select("Month", "Sales")
    
    return result_df

def calculate_yearly_sales(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for quarterly sales
    result_df = sales_df \
        .join(product_df, "Product Id") \
        .withColumn("Amount", col("Quantity")*col("Price")) \
        .groupBy(year("Date").alias("Year")) \
        .agg(sum("Amount").alias("Sales")) \
        .orderBy("Year")
    
    return result_df

def calculate_quarterly_sales(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for quarterly sales
    result_df = sales_df \
        .join(product_df, "Product Id") \
        .withColumn("Amount", col("Quantity") * col("Price")) \
        .groupBy(year("Date").alias("Year"), quarter("Date").alias("Quarter")) \
        .agg(sum("Amount").alias("QuarterlySales")) \
        .orderBy("Year", "Quarter")
    
    return result_df

def calculate_category_orders(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for category orders
    result_df = sales_df.groupBy("Product Id") \
        .agg(sum("Quantity").alias("Count")) \
        .join(product_df, "Product Id") \
        .select("Product Id", "Name", "Count")
    
    return result_df

def calculate_customer_frequency(sales_df: DataFrame):
    # Calculation logic for customer frequency
    result_df = sales_df \
        .groupBy("Customer Id") \
        .agg(count("*").alias("VisitFrequency"))
    
    return result_df

def calculate_country_sales(sales_df: DataFrame, product_df: DataFrame):
    # distinct_locations = sales_df.select("Location").distinct()

    exchange_rates = {"USA": 1.0, "UK": 0.79, "India": 83.0}
    result_df = sales_df.join(product_df, "Product Id") \
        .withColumn("Amount", col("Price")*col("Quantity")) \
        .groupBy("Location") \
        .agg(sum("Amount").alias("Total Sales USD")) \
        .withColumn("Total Sales Local Currency", col("Total Sales USD")*when(col("Location") == "USA", 1.0).
                                                                        when(col("Location") == "UK", exchange_rates["UK"]).
                                                                        when(col("Location") == "India", exchange_rates["India"]))
    
    return result_df

def calculate_source_sales(sales_df: DataFrame, product_df: DataFrame):
    # Calculation logic for source sales
    result_df = sales_df.join(product_df, "Product Id") \
        .withColumn("Amount", col("Price")*col("Quantity")) \
        .groupBy("Source") \
        .agg(sum("Amount").alias("Sales"))
    
    return result_df




