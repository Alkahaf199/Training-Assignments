

final class async_for$_ {
def args = async_for_sc.args$
def scriptPath = """/Users/cellarzero/Sigmoid Training/8.Scala/async_for.sc"""
/*<script>*/
import scala.concurrent._
import duration._
import ExecutionContext.Implicits.global
val f1 = Future(1.0)
val f2 = Future(2.0)
val f3 = Future(3.0)
val f4 = for {
  v1 <- f1
  v2 <- f2
  v3 <- f3
} yield v1 + v2 + v3
Await.result(f4, 10.seconds)
/*</script>*/ /*<generated>*//*</generated>*/
}

object async_for_sc {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new async_for$_

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export async_for_sc.script as `async_for`

