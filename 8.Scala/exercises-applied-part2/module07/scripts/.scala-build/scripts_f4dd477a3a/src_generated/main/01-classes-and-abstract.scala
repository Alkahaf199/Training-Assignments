

final class `01$minusclasses$minusand$minusabstract$_` {
def args = `01$minusclasses$minusand$minusabstract_sc`.args$
def scriptPath = """01-classes-and-abstract.sc"""
/*<script>*/
import java.time.LocalDate

class Person(name: String, age: Int) {
  def isAdult: Boolean = age >= 21
}

val p1 = new Person("Dave", 18)
val p2 = new Person("Jill", 25)

p1.isAdult
p2.isAdult

// always get a new instance, vs string interning

"hello".eq("hello")

new String("hello").eq(new String("hello"))

abstract class Car(make: String, model: String, year: Int) {
  def isVintage: Boolean = LocalDate.now.getYear - year > 20
}

// will not compile
// val mustang = new Car("Ford", "Mustang", 1965)

// but this will
val mustang = new Car("Ford", "Mustang", 1965) {}
/*</script>*/ /*<generated>*//*</generated>*/
}

object `01$minusclasses$minusand$minusabstract_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `01$minusclasses$minusand$minusabstract$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `01$minusclasses$minusand$minusabstract_sc`.script as `01-classes-and-abstract`

