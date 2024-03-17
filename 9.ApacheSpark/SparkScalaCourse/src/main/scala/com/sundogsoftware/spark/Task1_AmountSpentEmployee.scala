package com.sundogsoftware.spark

import org.apache.spark._
import org.apache.log4j._

object Task1_AmountSpentEmployee {

  def extractData(lines: String): (String, Float) = {
    val data = lines.split(',')
    val id = data(0)
    val amount = data(2).toFloat
    (id, amount)
  }
  def main(args: Array[String]): Unit = {

    Logger.getLogger("org").setLevel(Level.ERROR)

    val sc = new SparkContext("local[*]", "AmountSpentEmployee")
    val input = sc.textFile("data/customer-orders.csv")

    val data = input.map(extractData)
    val totalByEmployee = data.reduceByKey((x,y) => x + y)
    val sortedTotal = totalByEmployee.map(x => (x._2, x._1)).sortByKey(ascending = false)

    val results = sortedTotal.collect()

    for(result <- results) {
      val bill = result._1
      val formattedBill = f"$bill%.2f $$"
      val id = result._2
      println(s"$id\t$formattedBill")

    }
  }
}
