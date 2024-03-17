

final class `02$minusuniform$minusaccess$minusand$minusoverrides$_` {
def args = `02$minusuniform$minusaccess$minusand$minusoverrides_sc`.args$
def scriptPath = """02-uniform-access-and-overrides.sc"""
/*<script>*/
import java.time.LocalDate

abstract class Car(
  val make: String,
  val model: String,
  val year: Int
) {
  def isVintage: Boolean
}

val mustang = new Car("Ford", "Mustang", 1965) {
  def isVintage = LocalDate.now.getYear - year > 20
}
/*</script>*/ /*<generated>*//*</generated>*/
}

object `02$minusuniform$minusaccess$minusand$minusoverrides_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `02$minusuniform$minusaccess$minusand$minusoverrides$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `02$minusuniform$minusaccess$minusand$minusoverrides_sc`.script as `02-uniform-access-and-overrides`

