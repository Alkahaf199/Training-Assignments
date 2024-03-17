

final class `09$minusinheritance$minusand$minuscomposition$_` {
def args = `09$minusinheritance$minusand$minuscomposition_sc`.args$
def scriptPath = """09-inheritance-and-composition.sc"""
/*<script>*/
abstract class Vehicle {
  def name: String
  def description: Vector[String]

  override def toString: String = s"Vehicle($name)"

  def fullDescription: String = {
    (name +: description).mkString("\n")
  }
}

case class Car(
  name: String,
  description: Vector[String] = Vector.empty
) extends Vehicle


val mustang = Car("Ford Mustang", Vector(
  "1965 Mustang", "Metallic Blue", "302 ci V8"
))

val datsun = Car("Datsun 280Z", Vector(
  "1982 Datsun 280Z", "Candy Apple Red", "2.8 Liter I6"
))


mustang.fullDescription

abstract class VehicleStorage {
  def name: String
  def vehicles: Vector[Vehicle]

  def vehicleCount: Int = vehicles.size

  override def toString: String =
    s"$name with $vehicleCount vehicles"
}

case class ParkingStructure(name: String,
  vehicles: Vector[Vehicle]
) extends VehicleStorage {
  def describeGarage: String = {
    val vehicleString = vehicles.mkString(", ")
    s"$name containing $vehicleString"
  }

  override def toString = describeGarage
}

val lot = ParkingStructure(
  "Parking garage",
  Vector(mustang, datsun)
)

lot.vehicleCount



/*</script>*/ /*<generated>*//*</generated>*/
}

object `09$minusinheritance$minusand$minuscomposition_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `09$minusinheritance$minusand$minuscomposition$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `09$minusinheritance$minusand$minuscomposition_sc`.script as `09-inheritance-and-composition`

