package com.sundogsoftware.spark

import org.apache.spark.sql.types.{FloatType, IntegerType, StringType, StructType}
import org.apache.log4j._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

/** Find the minimum temperature by weather station */
object MinTemperaturesDataset {

  case class Temperature(stationID: String, date: Int, measure_type: String, temperature: Float)

  /** Our main function where the action happens */
  def main(args: Array[String]) {
   
    // Set the log level to only print errors
    Logger.getLogger("org").setLevel(Level.ERROR)

    // Create a SparkSession using every core of the local machine
    val spark = SparkSession
      .builder
      .appName("MinTemperatures")
      .master("local[*]")
      .getOrCreate()

    val temperatureSchema = new StructType()
      .add("stationID", StringType, nullable = true)
      .add("date", IntegerType, nullable = true)
      .add("measure_type", StringType, nullable = true)
      .add("temperature", FloatType, nullable = true)

    // Read the file as dataset
    import spark.implicits._
    val ds = spark.read
      .schema(temperatureSchema)
      .csv("data/1800.csv")
      .as[Temperature]
    
    // Filter out all but TMIN entries
    val minTemps = ds.filter($"measure_type" === "TMIN")
    val maxTemps = ds.filter($"measure_type" === "TMAX")
    
    // Select only stationID and temperature)
    val stationTemps = minTemps.select("stationID", "temperature")
    val stationTemps2 = maxTemps.select("stationID", "temperature")
    
    // Aggregate to find minimum temperature for every station
    val minTempsByStation = stationTemps.groupBy("stationID").min("temperature")
    val maxTempsByStation = stationTemps2.groupBy("stationID").max("temperature")

    val joinDS = minTempsByStation.join(maxTempsByStation, "stationID")

    // Convert temperature to fahrenheit and sort the dataset
    val tempsByStationF = joinDS
      .withColumn("min(temperature)", round($"min(temperature)" * 0.1f * (9.0f / 5.0f) + 32.0f, 2))
      .withColumn("max(temperature)", round($"max(temperature)" * 0.1f * (9.0f / 5.0f) + 32.0f, 2))
      .select("stationID", "min(temperature)", "max(temperature)")

    // Collect, format, and print the results
    val results = tempsByStationF.collect()
    
    for (result <- results) {
       val station = result(0)
       val temp1 = result(1).asInstanceOf[Float]
       val formattedTemp1 = f"$temp1%.2f F"
      val temp2 = result(2).asInstanceOf[Float]
      val formattedTemp2 = f"$temp2%.2f F"
       println(s"$station : Minimum temperature: $formattedTemp1 Maximum Temperature: $formattedTemp2")
    }

    spark.stop()
  }
}