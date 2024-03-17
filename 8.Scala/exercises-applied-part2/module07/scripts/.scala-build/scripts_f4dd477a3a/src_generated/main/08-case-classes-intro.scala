

final class `08$minuscase$minusclasses$minusintro$_` {
def args = `08$minuscase$minusclasses$minusintro_sc`.args$
def scriptPath = """08-case-classes-intro.sc"""
/*<script>*/
import java.time.LocalDate

case class Car(make: String, model: String, year: Int) {
  lazy val isVintage: Boolean =
    LocalDate.now.getYear - year > 20
}

val mustang = Car("Ford", "Mustang", 1965)

mustang.make
mustang.model
mustang.year
mustang.isVintage

mustang == Car("Ford", "Mustang", 1965)
mustang == Car("Ford", "Mustang", 1964)

/*</script>*/ /*<generated>*//*</generated>*/
}

object `08$minuscase$minusclasses$minusintro_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `08$minuscase$minusclasses$minusintro$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `08$minuscase$minusclasses$minusintro_sc`.script as `08-case-classes-intro`

