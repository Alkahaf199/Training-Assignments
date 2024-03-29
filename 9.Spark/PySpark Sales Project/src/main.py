from pyspark.sql import SparkSession
import data_processing as dp
import analysis as ana
import db_operations as dbo

if __name__ == "__main__":
    # Create a Spark session
    spark = SparkSession.builder \
        .appName("SaleAnalysis") \
        .config("spark.driver.extraClassPath", "lib/mysql-connector-j-8.3.0/mysql-connector-j-8.3.0.jar") \
        .getOrCreate()

    # Read database credentials from config.ini
    mysql_url, mysql_user, mysql_password = dp.read_database_credentials()

    # Read sales and products data
    sales_df = dp.read_sales_data(spark)
    products_df = dp.read_products_data(spark)

    # Perform data processing and analysis
    customer_expense = ana.calculate_customer_expense(sales_df, products_df)
    category_expense = ana.calculate_category_expense(sales_df, products_df)
    monthly_sales = ana.calculate_monthly_sales(sales_df, products_df)
    yearly_sales = ana.calculate_yearly_sales(sales_df, products_df)
    quarterly_sales = ana.calculate_quarterly_sales(sales_df, products_df)
    category_orders = ana.calculate_category_orders(sales_df, products_df)
    customer_frequency = ana.calculate_customer_frequency(sales_df)
    country_sales = ana.calculate_country_sales(sales_df, products_df)
    source_sales = ana.calculate_source_sales(sales_df, products_df)

    # Write results to MySQL database
    dbo.write_to_mysql(customer_expense, mysql_url, mysql_user, mysql_password, "Customer_Expense")
    dbo.write_to_mysql(category_expense, mysql_url, mysql_user, mysql_password, "Category_Expense")
    dbo.write_to_mysql(monthly_sales, mysql_url, mysql_user, mysql_password, "Monthly_Sales")
    dbo.write_to_mysql(yearly_sales, mysql_url, mysql_user, mysql_password, "Yearly_Sales")
    dbo.write_to_mysql(quarterly_sales, mysql_url, mysql_user, mysql_password, "Quarterly_Sales")
    dbo.write_to_mysql(category_orders, mysql_url, mysql_user, mysql_password, "Category_Orders")
    dbo.write_to_mysql(customer_frequency, mysql_url, mysql_user, mysql_password, "Customer_Frequency")
    dbo.write_to_mysql(country_sales, mysql_url, mysql_user, mysql_password, "Country_Sales")
    dbo.write_to_mysql(source_sales, mysql_url, mysql_user, mysql_password, "Source_Sales")

    print("Completed warehousing")

    # Stop the Spark session
    spark.stop()
