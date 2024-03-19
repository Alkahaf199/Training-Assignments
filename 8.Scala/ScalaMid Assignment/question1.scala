import scala.io.StdIn

object Bucketize {
  def main(args: Array[String]): Unit = {
    println("Enter numbers separated by spaces:")
    val inputString = StdIn.readLine()
    val inputArray = inputString.split(" ").map(_.toDouble)
    val buckets = bucketize(inputArray)
    println("Output: " + buckets.mkString(", "))
  }

  def bucketize(input: Array[Double]): Array[String] = {
    val bucketRanges = (0 to 2000).map(_ * 0.049).toArray // Creating an array of bucket ranges
    input.map { num =>
      val range = bucketRanges.find(_ >= num).getOrElse(100.0) // If num exceeds the maximum range, set it to 100.0
      f"${range - 0.049}%1.3f-${range}%1.3f"
    }
  }
}
