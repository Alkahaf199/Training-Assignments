import scala.io.Source

object PlayerStatistics {
  case class Player(year: Int, name: String, country: String, matches: Int, runs: Int, wickets: Int)

  def main(args: Array[String]): Unit = {
    val fileName = "player_statistics.txt"
    val players = readPlayerStatistics(fileName)

    // Task 1: Player with the highest run scored
    val playerWithHighestRun = players.maxBy(_.runs)
    println(s"\nPlayer with the highest run scored: ${playerWithHighestRun.name} - ${playerWithHighestRun.runs} runs\n\n")

    // Task 2: Top 5 players by run scored
    val top5PlayersByRun = players.sortBy(_.runs)(Ordering[Int].reverse).take(5)
    println("Top 5 players by run scored:")
    top5PlayersByRun.foreach(player => println(s"${player.name} - ${player.runs} runs"))
    print("\n\n")

    // Task 3: Top 5 players by wickets taken
    val top5PlayersByWickets = players.sortBy(_.wickets)(Ordering[Int].reverse).take(5)
    println("Top 5 players by wickets taken:")
    top5PlayersByWickets.foreach(player => println(s"${player.name} - ${player.wickets} wickets"))
    print("\n\n")

    // Task 4: Rank players with overall performance
    val rankedPlayers = players.map(player => (player, player.runs * 0.05 + player.wickets * 5)).sortBy(_._2)(Ordering[Double].reverse)
    println("Ranked players with overall performance:")
    rankedPlayers.zipWithIndex.foreach { case ((player, performance), index) =>
      println(s"${index + 1}. ${player.name} - Performance: $performance")
    }
    print("\n\n")
  }

  def readPlayerStatistics(fileName: String): List[Player] = {
    val source = Source.fromFile(fileName)
    val lines = source.getLines().toList
    source.close()
    lines.tail.map { line =>
      val Array(year, name, country, matches, runs, wickets) = line.split(", ").map(_.trim)
      Player(year.toInt, name, country, matches.toInt, runs.toInt, wickets.toInt)
    }
  }
}
