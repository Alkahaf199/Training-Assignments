

final class case$_ {
def args = case_sc.args$
def scriptPath = """/Users/cellarzero/Sigmoid Training/8.Scala/case.sc"""
/*<script>*/
val x = 1
val res = x match {
  case 1 => "one"
  case 2 => "two"
  case _ => "something else"
}

val n = -1
n match {
  case 0 => "It's zero"
  case v if v > 0 => s"It's positive $v"
  case v => s"It's negative ${v.abs}"
}

def matchIt(x: Any): String = x match {
  case "Hello" => "Well, hello back"
  case 1 :: rest => s"A list beginning with 1, rest is $rest"
  case Nil => "The empty list"
  case 5 => "The number 5"
  case _: List[_] => "Some kind of list, not empty and not starting with 1"
}

matchIt(5)           // The number 5
matchIt(List(1,2,3)) // A list beginning with 1, rest is List(2, 3)
matchIt(List(1))
matchIt(List(2,3))
matchIt(Nil)
matchIt(2.0)
matchIt("Hello")

/*</script>*/ /*<generated>*//*</generated>*/
}

object case_sc {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new case$_

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export case_sc.script as `case`

