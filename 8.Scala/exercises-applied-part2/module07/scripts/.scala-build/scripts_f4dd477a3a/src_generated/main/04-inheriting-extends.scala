

final class `04$minusinheriting$minusextends$_` {
def args = `04$minusinheriting$minusextends_sc`.args$
def scriptPath = """04-inheriting-extends.sc"""
/*<script>*/
abstract class Food {
  def name: String
}

abstract class Fruit extends Food

class Orange(val name: String) extends Fruit

val jaffa = new Orange("Jaffa")
/*</script>*/ /*<generated>*//*</generated>*/
}

object `04$minusinheriting$minusextends_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `04$minusinheriting$minusextends$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `04$minusinheriting$minusextends_sc`.script as `04-inheriting-extends`

