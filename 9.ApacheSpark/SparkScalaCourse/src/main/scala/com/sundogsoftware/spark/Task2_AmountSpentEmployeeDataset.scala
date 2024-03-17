package com.sundogsoftware.spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.log4j._
import org.apache.spark.sql.types.{FloatType, IntegerType, StructType}

object Task2_AmountSpentEmployeeDataset {

  case class Customer(customerId: Int, purchaseId: Int, amount: Float)

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)

    val spark = SparkSession
      .builder
      .appName("AmountSpentEmployee")
      .master("local[*]")
      .getOrCreate()

    val customerSchema = new StructType()
      .add("customerId", IntegerType, nullable = true)
      .add("purchaseId", IntegerType, nullable = true)
      .add("amount", FloatType, nullable = true)

    import spark.implicits._
    val ds = spark.read
      .schema(customerSchema)
      .csv("data/customer-orders.csv")
      .as[Customer]

    val purchases = ds.select("customerId", "amount")
    val totalAmount = purchases.groupBy("customerId").agg(round(sum("amount"),2).alias("totalAmount")).sort("totalAmount")

    totalAmount.show(totalAmount.count.toInt)


    spark.close()





  }

}
