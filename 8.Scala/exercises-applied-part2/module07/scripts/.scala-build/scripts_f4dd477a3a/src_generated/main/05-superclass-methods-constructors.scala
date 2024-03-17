

final class `05$minussuperclass$minusmethods$minusconstructors$_` {
def args = `05$minussuperclass$minusmethods$minusconstructors_sc`.args$
def scriptPath = """05-superclass-methods-constructors.sc"""
/*<script>*/
abstract class Vehicle(val name: String, val age: Int) {
  override def toString: String =
    s"$name, $age years old"
}

class Car(
  override val name: String,
  val make: String,
  val model: String,
  override val age: Int
) extends Vehicle(name, age) {

  override def toString: String =
    s"a $make $model, named ${super.toString}"
}

val mustang = new Car("Sally", "Ford", "Mustang", 50)

/*</script>*/ /*<generated>*//*</generated>*/
}

object `05$minussuperclass$minusmethods$minusconstructors_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `05$minussuperclass$minusmethods$minusconstructors$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `05$minussuperclass$minusmethods$minusconstructors_sc`.script as `05-superclass-methods-constructors`

