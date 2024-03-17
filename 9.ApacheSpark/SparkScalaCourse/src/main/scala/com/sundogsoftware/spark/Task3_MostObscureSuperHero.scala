package com.sundogsoftware.spark

import org.apache.spark._
import org.apache.spark.sql.{SparkSession, Dataset}
import org. apache.spark.sql.functions._
import org.apache.spark.sql.types.{IntegerType, StringType, StructType}
import org.apache.log4j._


object Task3_MostObscureSuperHero {

  case class SuperHero(id: Int, value: Int)
  case class SuperHeroNames(name: String, id: Int)
//  case class SuperHero(value: String)

  def parserLine(line: String): (Int, Int) = {
    val data = line.split("\\s")
    (data(0).toInt, data.length-1)
  }

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)

    val sc = new SparkContext("local[*]", "MostObscureSuperhero")
    val spark = SparkSession
      .builder
      .appName("MostObscureSuperhero")
      .master("local[*]")
      .getOrCreate()

    val data = sc.textFile("data/marvel-graph.txt")
    val pairings = data.map(parserLine)

    val superHeroNamesSchema = new StructType()
      .add("id", IntegerType, nullable = true)
      .add("name", StringType, nullable = true)

    import spark.implicits._
    val names = spark.read
      .schema(superHeroNamesSchema)
      .option("sep", " ")
      .csv("data/Marvel-names.txt")
      .as[SuperHeroNames]

    val pairingsDS: Dataset[SuperHero] = pairings.toDS().map { case (id, value) => SuperHero(id, value) }
    val connections = pairingsDS.groupBy("id").agg(sum("value").alias("connections"))
    val minConnections = connections.agg(min("connections")).first().getLong(0)
    val filteredConnections = connections.filter($"connections" === minConnections)

    val minConnectionsWithNames = filteredConnections.join(names, usingColumn = "id")

    println("The following have only " + minConnections + " connection(s) : ")
    minConnectionsWithNames.select("name").show()

//    filteredConnections.show()

//    names.show(truncate = true)

//    val minConnectionCount = connections.agg(min("connection"))
//    minConnectionCount.show()

    spark.stop()
    sc.stop()

  }
}
