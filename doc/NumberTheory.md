# Definitions

## _Theorem_

A statement of fact that has been proven to be true.

## _Lemma_

A minor statement of fact that can be used in the construction of a theorem.

## _Proof_

Argues why a lemma or theorem is true. A special case is a proof by contradiction, which proves a lemma or theorem by assuming it is not true and demonstrating that this is a contradiction.

# Notation

_Unless otherwise noted, assume all integers are positive._

The symbol | means _divides_. For example, given two integers $a$ and $b$, $a|b$ means $a$ divides $b$ without leaving a remainder.

The symbol $\equiv$ denotes a congruence relation (which in effect tranlates to _is equivalent to_). For example, $a \equiv b \pmod{c}$ means $a$ is congruent to $b$ modulo $c$, where $a$, $b$ and $c$ are all integers. In such a relation, $a - b$ is a multiple of $c$; or, more formally, $a - b = kc$ for some integer $k$.

The symbol $\phi$ (the letter _phi_ in the Greek alphabet) denotes [_Euler's Totient Funtion_](https://en.wikipedia.org/wiki/Euler%27s_totient_function), as in $\phi(n)$, where $n$ is some integer. For any integer $n$, $\phi(n)$ gives the number of integers between $1$ and $n$ that are [_coprime_](https://en.wikipedia.org/wiki/Coprime_integers), or [_relatively prime_](https://en.wikipedia.org/wiki/Coprime_integers), to $n$.

# Transitivity of Divisors Lemma

If $a|b$ and $b|c$, then $a|c$.

## Proof:

- If $a|b$, then there is an integer $k$ such that $ak = b$
- If $b|c$, then there is an integer $l$ such that $bl = c$
- Therefore, $c = bl = (ak)l = a(kl)$

# Prime Factors Lemma

Let $n$ be an integer greater than $1$. Let $d$ be the smallest divisor of $n$ that is greater than $1$. Then $d$ is prime.

## Proof (by contradiction):

- $n$ is a divisor of $n$, and $n > 1$; therefore, there is at least one divisor of $n$ that is greater than $1$, and there must also be a smallest divisor of $n$ that is greater than $1$
- Assume $d$ is not a prime (contradiction)
- If $d$ is not a prime, it has a divisor $e$ such that $1 < e < d$
- If $e|d$ and $d|n$, then $e|n$ (proven by transitivity of divisors lemma)
- So $e$ is a divisor of $n$, and $e$ is also smaller than $d$; but $d$ is the smallest divisor of $n$

# [Euclid's Lemma](https://en.wikipedia.org/wiki/Euclid%27s_lemma)

If $p$ is prime, and $p|ab$, where $ab$ is the product of two integers $a$ and $b$, then $p$ must divide either $a$ or $b$.

If on the other hand $p$ is composite, and $p|ab$, then $p$ may divide either $a$ or $b$. For example, if $p=10$, $a=4$ and $b=25$, then $p$ divides neither $a$ nor $b$ individually, but it divides $ab$.

## Proof

- Let $p$ be a prime, and $a$ an integer coprime with $p$; i.e., $p$ does not divide $a$
- There are integers $x$ and $y$ such that $xp + ya = 1$ (this is [Bezout's identity](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity))
- Multiply both sides of this equation by $b$, giving $xpb + yab = b$
- The term $xpb$ is divisible by $p$
- The term $yab$ is divisible by $ab$
- Since $p|ab$, the sum of $xpb$ and $yab$, or $b$, is also divisible by $p$


# [Fundamental Theorem of Arithmetic](https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic)

All integers greater than $1$ are the product of a unique set of primes. For example, $3$ and $5$ are the unique prime factors of $15$; and $2$, $2$, $3$ and $5$ are the unique prime factors $60$.

## Proof
- If a prime divides the product of two integers, then it must divide at least one of these integers (proven by Euclid's lemma)

# [Miller&ndash;Rabin Theorem](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test) 

If $p$ is prime, then the only possible square roots of $1$ modulo $p$ are either $1$ or $-1$.

This is technically just a specialization of Euclid's lemma; it is important because it is used to test very large integers for primality (see subsection [_Finding Large Primes_](#finding-large-primes) for a more thorough discussion).

## Proof
- Let $a^2 \equiv 1 \pmod{p}$, giving that $a$ is the square root of $1$ modulo $p$
- Subtract $1$ from both sides of the relation, giving $a^2 - 1 \equiv 0 \pmod{p}$
- Thus, $p$ divides $a^2-1$
- Factor the term $a^2 - 1$ into the difference of its squares, giving $(a+1)(a-1)$
- Thus, $p$ divides $(a+1)(a-1)$
- Since $p$ is prime, then $p$ divides either $(a+1)$ or $(a-1)$ (proven by [Euclid's lemma](#euclids-lemma))
- Therefore, $a$ is congruent to either $1$ or $-1$ modulo $p$

# [Fermat's Factorization Algorithm](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method)

Attempts to factor a composite odd integer $n$, where $n$ is the product of exactly two distinct prime factors $p$ and $q$ (e.g., an RSA modulus). If $n$ can be factored using this algorithm, then the difference of its factors is too small, and the factors therefore cryptographically weak. Suitable factors of an RSA modulus should be distant enough to defeat this algorithm for a sufficiently long run time.

Note that if $n$ is an RSA modulus it cannot be even; otherwise one of its factors would be $2$.

1. Set $i$ to the integer floor of the square root of $n$
2. Set $a=i+1$
3. Set $b=a^2 - n$
4. If $b$ is _not_ a perfect square, set $a=a+1$ and go to step 3; otherwise, $(a+b)$ and $(a-b)$ are the factors of $n$ and we're done
5. Repeat steps 3 and 4 until $b$ is a perfect square, or a sensible number of attempts has been made.

Fermat's factorization algorithm is based on the fact that any odd integer $n$ can be expressed as the [difference of two consecutive squares](#difference-of-two-squares), i.e., $n = a^2 - b^2$ for two consecutive integers $b$ and $a$. The right&ndash;hand side of this equation can be factored into $(a+b)(a-b)$. And if $(a+b) \ne 1$ and $(a-b) \ne 1$, then $(a+b)(a-b)$ is a nontrivial factorization of $n$.

# [Shor's Factorization Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)

Attempts to factor a composite odd integer $n$, where $n$ is the product of exactly two distinct prime factors $p$ and $q$ (e.g., an RSA modulus).

In 1994, Peter Shor proposed a theoretical version of this algorithm that would run in polynomial time on a sufficiently powerful quantum computer. At the time of this writing, no such computer yet exists. The algorithm can nevertheless be executed on a classical computer, albeit with an exponential running time.

The algorithm reduces the problem of factoring to one of order&ndash;finding, and leverages the fact that the order of any element in the finite multiplicative group of integers modulo $n$ divides the order of $n$.

The classical version runs as follows:

1. Set $a$ to a value randomly selected from the range $[2..n-1]$
2. Set $g = gcd(a,n)$
3. If $g \ne 1$, then $g$ and $n/g$ are the nontrivial factors of $n$ and we are done
4. Set $r = 1$
5. While $a^r \bmod n \ne 1$, set $r = r+1$
6. If $r$ is even, set $s$ = $a^{r/2} \bmod n$; otherwise, return to step 1
7. If $s \ne n-1$, then $gcd(s-1, n)$ and $gcd(s+1,n)$ are the nontrivial factors of $n$ and we are done; otherwise, return to step 1.

Step 5&mdash;which is the order&ndash;finding part of the algorithm&mdash;is the bottleneck, and would take millions of years to run against a proper RSA modulus on even the most powerful classical computer. On a sufficiently large quantum computer, however, the order of $a$ can be identified in polynomial time using a quantum fourier transform.

## Proof

* Let $n$ be a semiprime integer
* Let $r$ be the smallest integer such that $a^r \equiv 1 \pmod n$ for some integer $a$, where $1 < a < n$ (if $r$ is odd, start over with another $a$)
* Therefore, $n$ divides $a^r - 1$; incidentally, also note that $r$ divides $\phi(n)$
* Let $s = a^{r/2}$; i.e., the square root of $a^r$
* It cannot be the case that $s \equiv 1 \pmod n$, because $a^r \equiv 1 \pmod n$, and $r$ is the smallest integer such that $a^r \equiv 1 \pmod n$
* If it is the case that $s \equiv -1 \pmod n$, then $n$ divides $s+1$, and $s+1$ is a trivial factor of $n$
* Otherwise, $s \not \equiv 1 \pmod n$ and $s \not \equiv -1 \pmod n$, and therefore neither $s-1$ nor $s+1$ is a multiple of $n$, but their product is; i.e., $a^r-1 = (a^{r/2}-1)(a^{r/2}+1) = (s-1)(s+1) \equiv 0 \pmod n$ (see [Euclid's lemma](#euclids-lemma))
* Therefore, the prime factors of $n$ must share factors with $(s-1)$ and $(s+1)$
* Let $p=gcd(n,s-1)$ and $q=gcd(n,s+1)$
* Then $p$ and $q$ are the prime factors of $n$

# [Difference of Two Squares](https://en.wikipedia.org/wiki/Difference_of_two_squares)
Every odd number $n$ can be expressed as the difference of two consecutive squares, such that $n=a^2-b^2$ for two consecutive integers $b$ and $a$.

## Proof
- If $n$ is an odd integer, then $n = 2k+1$ trivially for some integer $k$
- By the difference of squares, $n = a^2 - b^2$ for two consecutive integers $b$ and $a$
- Let $a=(k+1)$ and $b=k$
- Then $n = (k+1)^2 - k^2$
- $n = (k+1)(k+1) - k^2$
- $n = k^2 + 2k+1 - k^2$
- $n = 2k+1$

# [Euclid's Theorem](https://en.wikipedia.org/wiki/Euclid%27s_theorem)

There are an infinite number of primes.

## Proof (by contradiction):

- Assume the number of primes is finite
- Let $n$ be the product of the following set, plus $1$; that is, $p_{1} \times p_{2} \times p_{3} ...\times p_{k} + 1$, where $k$ is the number of primes
- Let $d$ be the smallest divisor of $n$, which must be prime (proven by prime factors lemma)
- None of the primes in the set is a divisor of $n$ (they are instead divisors of $n - 1$); therefore, dividing $n$ by any $p$ in the set leaves a remainder of $1$
- Therefore, $d$ is prime and it is not in the set (contradiction)

# [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem)

$a^{p-1} \equiv 1 \pmod{p}$, where $a$ is an integer not divisible by $p$, and $p$ is prime.

It therefore follows that $a^p \equiv a \pmod{p}$ for the same $a$ and $p$, if we multiply both sides of the relation by $a$, as in:

- $a^{p-1} \equiv 1 \pmod{p}$
- $a^{p-1} \times a \equiv 1 \times a \pmod{p}$
- $a^{p-1+1} \equiv a \pmod{p}$
- $a^p \equiv a \pmod{p}$

There are many proofs of Fermat's little theorem. The following proof uses [group theory](#groups), and is based specifically on [LaGrange's theorem](#lagranges-theorem).

## Proof:
- Let $p$ be a prime
- Let $G$ be the set $\{1, 2, ...,p-1\}$ (which in group theory is called _the multiplicative group modulo p_)
- Let $a$ be a member of this group, i.e., $1 \le a \le p-1$
- Let $k$ be the order of $a$; i.e., the smallest integer such that $a^k \equiv 1 \pmod p$
- Then the numbers $a, a^2, ..., a^k$ modulo $p$ form a subgroup of $G$ whose order is $k$
- By LaGrange's theorem, $k$ divides the order of $G$, or $p-1$
- Then $p-1 = km$ for some integer $m$
- Therefore, $a^{p-1} = a^{km} = (a^{k})^m \equiv 1^m \equiv 1 \pmod p$

For another interesting proof, based on [Euclid's lemma](#euclids-lemma), see [power-product expansions](https://en.wikipedia.org/wiki/Proofs_of_Fermat%27s_little_theorem#Proof_using_power_product_expansions).


# Finding Large Primes
Primality&ndash;testing algorithms based on trial division are not feasible for primes of the size necessary for use in cryptographic applications. Even though the time complexity of these algorithms is linear, their candidate inputs are so large that even linear&ndash;time algorithms are too slow. (How slow? they would require many times the age of the universe to complete.)

However, combining some theorems and lemmas from above, we can identify very large primes using an algorithm of logarithmic time complexity. Perhaps the most famous of these is the [Miller&ndash;Rabin](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test) algorithm, which in its accepted form was developed by Michael Rabin in 1980. Rabin's variant is probabalistic, and builds on a deterministic version of the algorithm developed by Gary Miller in 1976.

## Lemmas Used in Miller&ndash;Rabin

- Fermat's little theorem, which states that if $p$ is prime, then $a^{p-1} \equiv 1 \pmod{p}$, where $1 < a < p$.
- Euclid's lemma, which states that if $p$ is prime, and $p|ab$, where $ab$ is the product of two integers $a$ and $b$, then $p$ must divide either $a$ or $b$.

## Miller&ndash;Rabin

If Miller&ndash;Rabin were a theorem, it would state that if $p$ is prime, then the square root of $1$ modulo $p$ is either $1$ or $-1$. Conversely, if the square root of $p$ modulo $1$ is neither $1$ nor $-1$, then $p$ must be composite (see subsection [_Miller&ndash;Rabin Theorem_](#miller–rabin-theorem) for a more general proof).

### Proof

- By Fermat, we have that if $p$ is prime, then $a^{p-1} \equiv 1 \pmod{p}$
- If we subtract $1$ from both sides of this relation, we get $a^{p-1} - 1 \equiv 0 \pmod{p}$
- Therefore, $p$ divides $a^{p-1} - 1$
- The square root of $a^{p-1}$ is $a^{(p-1)/2}$, so by the difference of squares we can rewrite $a^{p-1} - 1$ as $(a^{(p-1)/2} + 1)(a^{(p-1)/2} - 1)$
- By Euclid, we have that if $p$ is prime, then $p$ divides at least one of the terms $(a^{(p-1)/2} + 1)$ or $(a^{(p-1)/2} - 1)$
- Therefore, the square root of $a^{p-1}$, or $a^{(p-1)/2}$, is congruent to either $1$ or $-1$ modulo $p$

Stated generally, if $p$ is prime, then the square root of $a^{p-1}$ (which by Fermat we know to be congruent to $1$ modulo $p$) must either also be congruent to $1$ modulo $p$ or, if it is not, then it must be congruent to $-1$ modulo $p$.

Specifically, with regard to the Miller&ndash;Rabin algorithm, if the square root of $a^{p-1}$ is _not_ congruent to either $1$ or $-1$ modulo $p$, then $p$ must be composite. We can use this fact to test for the compositeness of an integer that runs in logarithmic time in the size of the input.

# [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem)

$a^{\phi(n)} \equiv 1 \pmod{n}$, where $a$ is an integer not divisible by $n$.

It therefore follows that $a^{\phi(n)+1} \equiv a \pmod{n}$ for the same $a$ and $n$.

Euler's theorem is a generalization of Fermat's little theorem, since $n$ can be either prime (Fermat) or the product of primes (Euler).

Recall that $\phi(n)$ gives the number of integers between 1 and $n$ that are coprime with $n$. Therefore, if $n$ is prime, then $\phi(n) = n - 1$, and we have $a^{n-1} \equiv 1 \pmod{n}$ (Fermat).

Euler's totient function is _multiplicative_, meaning that if two integers $p$ and $q$ are relatively prime, then $\phi(pq) = \phi(p) \times \phi(q) = (p-1)(q-1)$.

A corollary to Euler's theorem&mdash;and one that is crucial to understanding the RSA algorithm&mdash;is that for any integers $x$ and $y$, $x \equiv y \pmod{\phi(n)}$ implies $a^x \equiv a^y \pmod{n}$, if $a$ is coprime to $n$. This is proven as follows:

- $x \equiv y \pmod{\phi(n)}$
- $x - y = \phi(n)k$, for some integer $k$
- $x = y + \phi(n)k$
- $a^x = a^{y+\phi(n)k} = a^y(a^{\phi(n)})^{k} \equiv a^y1^k \equiv a^y \pmod{n}$

There are many proofs of Euler's theorem. The following is a generalization of the proof of [Fermat's little theorem](#fermats-little-theorem) presented above.

## Proof:
- Let $n$ be a positive integer (that is not necessarily prime)
- Let $G$ be the set $\lbrace 1 \le a \le n-1 : gcd(a,n) = 1\rbrace$ (which in group theory is called _the multiplicative group modulo_ $n$).
- Let $a$ be a member of this group
- Let $k$ be the order $a$; i.e., the smallest integer such that $a^k \equiv 1 \pmod{n}$
- Then the numbers $a, a^2, ..., a^k$ modulo $n$ form a subgroup of $G$ whose order is $k$
- By LaGrange's theorem, $k$ divides the order of $G$, or $\phi(n)$
- Then $\phi(n) = km$ for some integer $m$
- Therefore, $a^{\phi(n)} = a^{km} = (a^{k})^m \equiv 1^m \equiv 1 \pmod n$

# [Lagrange's Theorem](<https://en.wikipedia.org/wiki/Lagrange%27s_theorem_(group_theory)>)

For any group $G$, the order of every subgroup of $G$ divides the order of $G$.

More specifically, the order of any element $a$ in group $G$ is the smallest integer $k$ such that $a^k = e$, where $e$ is the identity element of the group. $k$ thus divides the order of $G$.

It follows then that $a^n = e$, where $n$ is the order of a group.

If $n$ is prime, the group is _cyclic_ and _simple_; i.e., its only subgroups are $1$ and the group itself.

## Proof:
- Consider a finite multiplicative group $G$ modulo some prime $p$
- Then $a^{p-1} \equiv 1 \pmod{p}$ for some $a$ where $0 < a < p$ ([Fermat's Little Theorem](#fermats-little-theorem))
- Let $g$ be a primitive element of $G$; that is, $g$ generates every element in the group $G$
- Then $g^x = a$ for some integer $x$ (this must be true because $g$ generates the whole group)
- Therefore, $a^{p-1} = g^{x(p-1)} = g^{(p-1)x} = 1^x \equiv 1 \pmod{p}$

# [The Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)

For any number of integers that are pairwise coprime, if one knows the remainders of the division of those integers by $x$, one can identify $x$. A special case is that if one knows the pair of integers $(x \bmod{p}, x \bmod{q})$, where $p$ and $q$ are distinct odd primes, one can uniquely determine the value of $x \bmod{pq}$.

Stated another way, each $x$ in $\mathbb{Z}_{n}$ corresponds to a unique pair $(x \bmod{p}, x \bmod{q})$.

The Chinese Remainder Theorem (CRT) is used in RSA to accelerate the otherwise intolerably expensive operations of decryption and digital signature.

# Finite Fields

- Any integer taken modulo a prime $p$ is always in the range $0, ..., p - 1$.
- The set of integers modulo a prime $p$ is a [_finite field_](https://en.wikipedia.org/wiki/Finite_field).
- You can always add or subtract any multiple of $p$ without changing the result (see [_congruence relation_](https://en.wikipedia.org/wiki/Congruence_relation)).
- Results of binary operations (addition, subtraction, multiplication and division) are always in the range $0, 1, ..., p - 1$.
- The finite field of integers modulo $p$ is written $\mathbb{Z}_{p}$.

# Rings

- The numbers modulo a composite $n$, where $n$ is the product of exactly two distinct odd primes $p$ and $q$, are $0, 1, ..., n - 1$.
- This is not a finite field (as it would be if $n$ were prime), but rather a [_ring_](<https://en.wikipedia.org/wiki/Ring_(mathematics)>), and is denoted $\mathbb{Z}_{n}$.

# Groups

- A [_group_](<https://en.wikipedia.org/wiki/Group_(mathematics)>) is a finite field together with a single binary operation, such as addition or multiplication.
- The numbers in $\mathbb{Z}_{p}$ form a group together with addition; one can add or subtract any two numbers in the group and the result will be a number in the group.
- A group whose operator is multiplication cannot contain 0 (because one cannot divide by 0), and consists of the set $1, ..., p - 1$; this is known as the _muliplicative group_ modulo $p$, and is written $\mathbb{Z_p^*}$.
- A group can contain _subgroups_; a subgroup is a subset of the elements in the full group.
- If you apply the group operator to two elements in a subgroup, you again get an element in the subgroup.

# Muliplicative Groups Modulo a prime $p$

- Each member $g$ of a group $G$ has an [_order_](<https://en.wikipedia.org/wiki/Order_(group_theory)>), which is the smallest integer exponent $q$ such that $g^q \equiv 1 \pmod{p}$.
- The group $G$ and its subgroups are [_cyclic_](https://en.wikipedia.org/wiki/Cyclic_group).
- In the multiplicative group modulo $p$, there is at least one $g$ that generates the entire group $G$. Such a $g$ is called a _primitive element_, or _generator_, of the group.
- Other values of $g$ generate smaller sets, or _subgroups_, of $G$.
- Multiplication or division of any two elements in the group or subgroup generated by $g$ yield another element in that group or subgroup.
- For any element $g$, the order of $g$ is a divisor of $p - 1$ (Lagrange's theorem)
- Conversely, for any divisor $d$ of $p-1$, there is a single subgroup of size $d$.

# Multiplication Modulo a composite $n$

- The integers modulo $n$, where $n$ is the product of exactly two distinct odd primes $p$ and $q$, are $0, 1, ..., n - 1$.
- These integers do not form a finite field, but rather a [_ring_](<https://en.wikipedia.org/wiki/Ring_(mathematics)>).
- For any prime $p$, for all $x$ where $0 < x < p$, the congruence relation $x^{p-1} \equiv 1 \pmod{p}$ holds. This is [_Fermat's Little Theorem_](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem).
- For a composite $n$ that is the product of exactly two distinct odd primes $p$ and $q$, there is an exponent $t$ such that $x^t \equiv 1 \pmod{n}$ for _almost_ all $x$; the exceptions are values of $x$ that are multiples of either $p$ or $q$.
- The frequency of such exceptions is in the proportion $\displaystyle \frac{(p+q)}{pq}$, and diminishes quadratically in the size of $pq$.
- The smallest $t$ that is a multiple of $p - 1$ and $q - 1$ is their least common mulitple, or $lcm(p-1, q-1)$.

# Greatest Common Divisor

- The greatest common divisor (_GCD_) of two integers $a$ and $b$ is the largest integer $k$ such that $k|a$ and $k|b$.
- The [_Euclidean Algorithm_](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md) computes the GCD of two integers in logarithmic time.

# Least Common Multiple

- The least common multiple (_LCM_) of two integers $a$ and $b$ is smallest $k$ such that $k$ is a multiple of both $a$ and $b$; it is found by $\displaystyle \frac{ab}{gcd(a, b)}$.
- Whereas the original RSA whitepaper specifies that $\phi(pq)$&mdash;which recall is $(p-1)(q-1)$&mdash;be used to compute decryption and signature exponents, in practice $lcm(p-1, q-1)$ is used instead because it results in smaller, and therefore more efficient (albeit no less secure), exponents.

# The Extended Euclidean Algorithm

- Division is not possible in a multiplicative group, because division can produce fractional results.
- Therefore, to _simulate_ division in a multiplicative group, we use the [_Extended Euclidean
  Algorithm_](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md).
- This can be thought of as _multiplication by an inverse_ in the real numbers. For example, $\frac{5}{2}$ (division) is the same as $5 \times \frac{1}{2}$ (multiplication). In the latter, we multiply $5$ by the _inverse_ of $2$, or $\frac{1}{2}$. Both operations yield the same result, which is $2 \frac{1}{2}$.
- The extended euclidean algorithm finds two integers $u$ and $v$ such that $ua + vb = gcd(a, b)$, which allows one to compute the mulitiplicative inverse of an integer modulo $p$.
