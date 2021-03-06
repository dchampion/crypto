# Definitions
## Theorem
A statement that has been proven to be true.
## Lemma
A minor statement of fact that can be used in the construction of a theorem.
## Proof
Argues why a lemma or theorem is true. A special case is a proof by contradiction, which proves a lemma or theorem by assuming it is not true and demonstrating that this is a contradiction.
# Notation
The symbol '|' means <i>divides</i>. For example, <i>a</i> | <i>b</i> means <i>a</i> divides <i>b</i> evenly; that is, without leaving a remainder.
# Lemma 1
If <i>a</i> | <i>b</i> and <i>b</i> | <i>c</i>, then <i>a</i> | <i>c</i>
## Proof:
* If <i>a</i> | <i>b</i>, then there is an integer <i>k</i> such that <i>ak</i> = <i>b</i>
* If <i>b</i> | <i>c</i>, then there is an integer <i>l</i> such that <i>bl</i> = <i>c</i>
* Therefore, <i>c</i> = <i>bl</i> = (<i>ak</i>)<i>l</i> = <i>a</i>(<i>kl</i>)
# Lemma 2
Let <i>n</i> be a positive number greater than 1. Let <i>d</i> be the smallest divisor of <i>n</i> that is greater than 1. Then <i>d</i> is prime.
## Proof (by contradiction):
* <i>n</i> is a divisor of <i>n</i>, and <i>n</i> > 1; therefore, there is at least one divisor of <i>n</i> that is greater than 1, and there must also be a smallest divisor of <i>n</i> that is greater than 1
* Assume <i>d</i> is not a prime
* If <i>d</i> is not a prime, it has a divisor <i>e</i> such that 1 < <i>e</i> < <i>d</i>
* If <i>e</i> | <i>d</i> and <i>d</i> | <i>n</i> then <i>e</i> | <i>n</i> (Lemma 1)
* So <i>e</i> is a divisor of <i>n</i> and <i>e</i> is also smaller than <i>d</i>; but <i>d</i> is the smallest divisor of <i>n</i> (contradiction)
# Theorem
There are an infinite number of primes.
## Proof (by contradiction):
* Assume the number of primes is finite
* Let <i>n</i> be the product of this set plus one; that is, <i>p<sub>1</sub></i> * <i>p<sub>2</sub></i> * <i>p<sub>3</sub></i> * ... * <i>p<sub>k</sub></i> + 1, where <i>k</i> is the number of primes.
* Let <i>d</i> be the smallest divisor of <i>n</i>, which must be prime (Lemma 2)
* None of the primes in the set is a divisor of <i>n</i> (they are instead divisors of <i>n</i> - 1); therefore, dividing <i>n</i> by any <i>p</i> in the set leaves a remainder of 1
* Therefore, <i>d</i> is prime and it is not in the list (contradiction)
# Fundamental Theorem of Arithmetic
Any integer greater than 1 can be written in exactly one way as the product of primes (if you disregard the order in which they are written). For example, 15 = 3 * 5, and 60 = 2 * 2 * 3 * 5.
# Computations Modulo a Prime
* Any integer taken modulo <i>p</i> is always in the range 0, ..., <i>p</i> - 1.
# Groups and Finite Fields
* The set of numbers modulo a prime is a <i>finite field</i>.
* You can always add and subtract any multiple of <i>p</i> without changing the result (equivalence classes).
* Results are always in the range 0, 1, ..., <i>p</i> - 1.
* The finite field of integers modulo <i>p</i> is written <i>Z<sub>p</sub></i>.
* A <i>group</i> is a finite field together with an operation, such as addition or multiplication.
* The numbers in <i>Z<sub>p</sub></i> form a group together with addition; you can add any two numbers and get a third number in the group.
* A group whose operator is multiplication cannot contain 0 (because you cannot divide by 0), and consists of the set 1, ..., <i>p</i> - 1; this is known as the muliplicative group modulo <i>p</i>, and is written <i>Z*<sub>p</sub></i>.
* A group can contain a <i>subgroup</i>, which consists of a subset of the elements of the full group.
* If you apply the group operation to two elements of the subgroup, you again get an element of the subgroup.
* The inverse of multiplication is division.
# Greatest Common Divisor
* The greatest common divisor (<i>GCD</i>) of two numbers <i>a</i> and <i>b</i> is the largest <i>k</i> such that <i>k</i> | <i>a</i> and <i>k</i> | <i>b</i>.
* Use the <i>Euclidean Algorithm</i> to compute the GCD of two numbers.
# Least Common Multiple
* The least common multiple (<i>LCM</i>) of two numbers <i>a</i> and <i>b</i> is smallest <i>k</i> such that <i>k</i> is a multiple of both <i>a</i> and <i>b</i>; it is found by <i>ab</i> / <i>gcd</i>(<i>a</i>,<i>b</i>).
# The Extended Euclidean Algorithm
* Use the <i>Extended Euclidean Algorithm</i> to compute division modulo <i>p</i>.
* Finds two integers <i>u</i> and <i>v</i> such that <i>gcd</i>(<i>a</i>, <i>b</i>) = <i>ua</i> + <i>vb</i> = 1.
* Allows us to compute the inverse of a number modulo <i>p</i>.
# Muliplicative Groups Modulo <i>p</i>
* Each member <i>g</i> of the group <i>G</i> has an <i>order</i>, which is the smallest positive exponent <i>q</i> such that <i>g<sup>q</sup></i> = 1 (mod <i>p</i>). After this, the sequence of remainders repeats.
* This <i>g</i> is called a <i>generator</i>.
* In the multiplicative group modulo <i>p</i>, there is at least one <i>g</i> that generates the whole group <i>G</i>. Such a <i>g</i> is called a <i>primitive element</i> of the group.
* Other values of <i>g</i> generate smaller sets, or <i>subgroups</i>, of <i>G</i>.
* Multiplication or division of any two elements in the group or subgroup generated by <i>g</i> yield another element of that group or subgroup.
* For any element <i>g</i>, the order of <i>g</i> is a divisor of <i>p</i> - 1.
# The Chinese Remainder Theorem
* The numbers modulo a composite <i>n</i> that is the product of exactly two primes <i>p</i> and <i>q</i> are 0, 1, ..., <i>n</i> - 1, which is not a finite field as it would be if <i>n</i> were prime.
* This set is called a <i>ring</i>, and is written <i>Z<sub>n</sub></i>.
* For each <i>x</i> in <i>Z<sub>n</sub></i>, you can compute the unique pair (<i>x</i> mod <i>p</i>, <i>x</i> mod <i>q</i>).
* Given the pair (<i>x</i> mod <i>p</i>, <i>x</i> mod <i>q</i>), you can efficiently compute <i>x</i>.
# Multiplication Modulo <i>n</i>
* The numbers modulo <i>n</i>, where <i>n</i> is the product of exactly two primes <i>p</i> and <i>q</i>, are 0, 1, ..., <i>n</i> - 1.
* These numbers do not form a finite field, but rather a <i>ring</i>.
* For any prime <i>p</i>, for all <i>x</i> where 0 < <i>x</i> < <i>p</i> the equation <i>x<sup>p-1</sup> = 1</i> (mod <i>p</i>) holds. This is <i>Fermat's Little Theorem</i>.
* For a composite <i>n</i> that is the product of exactly two primes <i>p</i> and <i>q</i>, there is an exponent <i>t</i> such that <i>x<sup>t</sup></i> = 1 mod <i>n</i> for <i>almost</i> all <i>x</i>; the exceptions are values of <i>x</i> that are multiples of either <i>p</i> or <i>q</i>.
* The frequency of such exceptions is in the proportion (<i>p</i> + <i>q</i>) / <i>pq</i>.
* The smallest <i>t</i> that is a multiple of <i>p</i> - 1 and <i>q</i> - 1 is their least common mulitple, or <i>lcm</i>(<i>p</i> - 1, <i>q</i> - 1).