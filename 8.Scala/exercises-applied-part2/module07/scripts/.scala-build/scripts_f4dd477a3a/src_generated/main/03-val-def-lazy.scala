

final class `03$minusval$minusdef$minuslazy$_` {
def args = `03$minusval$minusdef$minuslazy_sc`.args$
def scriptPath = """03-val-def-lazy.sc"""
/*<script>*/
class Demo {
  val a: Int = {
    println("evaluating a")
    10
  }
  def b: Int = {
    println("evaluating b")
    20
  }
  lazy val c: Int = {
    println("evaluating c")
    30
  }
}

val demo = new Demo
demo.a
demo.b
demo.b
demo.c
demo.c

/*</script>*/ /*<generated>*//*</generated>*/
}

object `03$minusval$minusdef$minuslazy_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `03$minusval$minusdef$minuslazy$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `03$minusval$minusdef$minuslazy_sc`.script as `03-val-def-lazy`

