

final class file$_ {
def args = file_sc.args$
def scriptPath = """/Users/cellarzero/Sigmoid Training/8.Scala/file.sc"""
/*<script>*/
import java.io._
// class WriterOutput(writer: PrintWriter) {
//   def write(s: String): Unit = writer.println(s)
// }
// val ex1 = new PrintWriter(new File("ex1.txt"))
// val out1 = new WriterOutput(ex1)
// out1.write("Hello")
// out1.write("to")
// out1.write("you")
// ex1.close()

class WriterOutput2(writer: PrintWriter) {
  def write(s: String): WriterOutput2 = {
    writer.println(s)
    this
} }
val ex2 = new PrintWriter(new File("ex2.txt"))
val out2 = new WriterOutput2(ex2)
out2.write("Hello").write("to").write("you")
ex2.close()
/*</script>*/ /*<generated>*//*</generated>*/
}

object file_sc {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new file$_

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export file_sc.script as `file`

