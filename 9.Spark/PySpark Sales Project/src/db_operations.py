def write_to_mysql(dataframe, mysql_url, mysql_user, mysql_password, db_table):
    dataframe.write \
        .format("jdbc") \
        .option("url", mysql_url) \
        .option("dbtable", db_table) \
        .option("user", mysql_user) \
        .option("password", mysql_password) \
        .mode("overwrite") \
        .save()
