// val y = 1.+(2)

// val s = "hello"
// s.charAt(1)
// s charAt 1 
// This can be written as above

// println "hello"
// Above code wont work

// val arr = Array("scooby", "dooby", "doo")
// println(arr.apply(1)) 
// println(arr(0))


// Array("scooby", "dooby", "doo")
// // is re-written to
// Array.apply("scooby", "dooby", "doo")

// arr(1) = "dappy"
// is re-written to
// arr.update(1, "dappy")

// def squareRootsOf(xs: List[Int]): List[Double] =
//   for (x <- xs) yield math.sqrt(x)

import scala.collection._
val s1 = mutable.Set(1,2,3)
var s2 = immutable.Set(1,2,3)

s1 += 4  // works because s1 has a += operator
s2 += 4  // works because s2 is a var
