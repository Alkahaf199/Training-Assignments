name := "MinTemperatureDataset"

version := "1.0"

organization := "com.sundogsoftware"

scalaVersion := "2.12.19"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "3.5.1" % "provided",
"org.apache.spark" %% "spark-sql" % "3.5.1" % "provided"
)
