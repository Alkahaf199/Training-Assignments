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