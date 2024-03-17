

final class `06$minusoverride$_` {
def args = `06$minusoverride_sc`.args$
def scriptPath = """06-override.sc"""
/*<script>*/
abstract class Upper {
  def blip: String
  val blop: String = "blop"
  def op(x: Int, y: Int): Int
}

class Lower extends Upper {
  override def blip: String = "blip"
  override val blop: String = "bloop"
  override def op(x: Int, y: Int): Int = x + y
  def op(x: Double, y: Double): Double = x + y
}


/*</script>*/ /*<generated>*//*</generated>*/
}

object `06$minusoverride_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `06$minusoverride$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `06$minusoverride_sc`.script as `06-override`

