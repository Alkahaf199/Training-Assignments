import language.implicitConversions 

class Rational private (val n: Int, val d: Int) {
    require(d != 0, "Zero denominator!") // precondition
    override def toString: String = s"R($n/$d)"

    // Passing int to Rational, i.e. Auxillary Constructor
    // def this(i: Int) = this(i, 1) 
  
    def min(other: Rational): Rational =
      if ((n.toDouble / d) < (other.n.toDouble / other.d))
        this else other  // have to use this to return

    def add(other: Rational): Rational =
      new Rational(
        this.n * other.d + this.d * other.n,
        this.d * other.d
      )
    def +(other: Rational): Rational =
      new Rational(
        this.n * other.d + this.d * other.n,
        this.d * other.d
      )
    // Another way of Passing single Int, i.e. Overloading
    // def +(i: Int): Rational = 
    //   this + Rational(i)
    // No longer required after the use of implicit
}

object Rational {
  def apply(n: Int, d: Int): Rational = {
    println("Making a new Rational Number here.")
    new Rational(n, d)
  }
  implicit def apply(i: Int): Rational =
    new Rational(i, 1)
}