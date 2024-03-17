//package com.sundogsoftware.spark
//
//import org.apache.spark._
//import org.apache.log4j._
//import scala.math.min
//
///** Find the minimum temperature by weather station */
//object MinTemperatures {
//
//  def parseLine(line:String): (String, String, Float) = {
//    val fields = line.split(",")
//    val stationID = fields(0)
//    val entryType = fields(2)
//    val temperature = fields(3).toFloat * 0.1f * (9.0f / 5.0f) + 32.0f
//    (stationID, entryType, temperature)
//  }
//    /** Our main function where the action happens */
//  def main(args: Array[String]) {
//
//    // Set the log level to only print errors
//    Logger.getLogger("org").setLevel(Level.ERROR)
//
//    // Create a SparkContext using every core of the local machine
//    val sc = new SparkContext("local[*]", "MinTemperatures")
//
//    // Read each line of input data
//    val lines = sc.textFile("data/1800.csv")
//
//    // Convert to (stationID, entryType, temperature) tuples
//    val parsedLines = lines.map(parseLine)
//
//    // Filter out all but TMIN entries
//    val minTemps = parsedLines.filter(x => x._2 == "TMIN")
//
//    // Convert to (stationID, temperature)
//    val stationTemps = minTemps.map(x => (x._1, x._3.toFloat))
//
//    // Reduce by stationID retaining the minimum temperature found
//    val minTempsByStation = stationTemps.reduceByKey( (x,y) => min(x,y))
//
//    // Collect, format, and print the results
//    val results = minTempsByStation.collect()
//
//    for (result <- results.sorted) {
//       val station = result._1
//       val temp = result._2
//       val formattedTemp = f"$temp%.2f F"
//       println(s"$station minimum temperature: $formattedTemp")
//    }
//
//  }
//}

package com.sundogsoftware.spark

import org.apache.spark._
import org.apache.log4j._
import scala.math.min
import scala.math.max

object MinTemperatures {
  def parserLine(line: String): (String, String, Float) = {
    val fields = line.split(',')
    val id = fields(0)
    val entryType = fields(2)
    val temp = fields(3).toFloat * 0.1f
    (id, entryType, temp)
  }

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)

    val sc = new SparkContext("local[*]", "MinTemperatures")

    val lines = sc.textFile("data/1800.csv")
    val parsedLines = lines.map(parserLine)

    val minTemperatures = parsedLines.filter(x => x._2 == "TMIN")
    val maxTemperatures = parsedLines.filter(x => x._2 == "TMAX")

    val stationMinTemps = minTemperatures.map(x => (x._1, x._3.toFloat))
    val stationMaxTemps = maxTemperatures.map(x => (x._1, x._3.toFloat))

    val minTempsByStation = stationMinTemps.reduceByKey((x,y) => min(x,y))
    val maxTempsByStation = stationMaxTemps.reduceByKey((x,y) => max(x,y))

    val joinedTemps = minTempsByStation.join(maxTempsByStation)

    val result = joinedTemps.collect()

    result.foreach {
      case (stationId, (minTemp, maxTemp)) =>
        val formattedMinTemp = f"$minTemp%.2f"
        val formattedMaxTemp = f"$maxTemp%.2f"
        println(s"Station $stationId - Min Temp: $formattedMinTemp, Max Temp: $formattedMaxTemp")
    }
  }
}