

final class `07$minusfinal$_` {
def args = `07$minusfinal_sc`.args$
def scriptPath = """07-final.sc"""
/*<script>*/
// Can't do this, == is final

//class BadClass {
//  override def ==(other: Any): Boolean = {
//    println(s"Comparing $this to $other")
//    false
//  }
//}

class Authority {
  final def theWord: String =
    "This is the final word on the matter!"
}

// this won't compile either

//class Argumentative extends Authority {
//  override def theWord: String =
//    "No, it's not!"
//}

// String is final, so can't extend it

// class BadString extends String

final class Infinity

class Beyond extends Infinity

/*</script>*/ /*<generated>*//*</generated>*/
}

object `07$minusfinal_sc` {
  private var args$opt0 = Option.empty[Array[String]]
  def args$set(args: Array[String]): Unit = {
    args$opt0 = Some(args)
  }
  def args$opt: Option[Array[String]] = args$opt0
  def args$: Array[String] = args$opt.getOrElse {
    sys.error("No arguments passed to this script")
  }

  lazy val script = new `07$minusfinal$_`

  def main(args: Array[String]): Unit = {
    args$set(args)
    val _ = script.hashCode() // hashCode to clear scalac warning about pure expression in statement position
  }
}

export `07$minusfinal_sc`.script as `07-final`

