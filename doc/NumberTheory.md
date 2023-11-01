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

The symbol $\phi$ (the letter _phi_ in the Greek alphabet) denotes [Euler's Totient Funtion](https://en.wikipedia.org/wiki/Euler%27s_totient_function), as in $\phi(n)$, where $n$ is some integer. For any integer $n$, $\phi(n)$ gives the number of integers between $1$ and $n$ that are [coprime](https://en.wikipedia.org/wiki/Coprime_integers), or [relatively prime](https://en.wikipedia.org/wiki/Coprime_integers), to $n$.

# Transitivity of Divisors

If $a|b$ and $b|c$, then $a|c$.

## Proof:

- If $a|b$, then there is an integer $k$ such that $ak = b$
- If $b|c$, then there is an integer $l$ such that $bl = c$
- Therefore, $c = bl = (ak)l = a(kl)$

# Prime Factors

Let $n$ be an integer greater than $1$. Let $d$ be the smallest divisor of $n$ that is greater than $1$. Then $d$ is prime.

## Proof (by contradiction):

- $n$ is a divisor of $n$, and $n > 1$; therefore, there is at least one divisor of $n$ that is greater than $1$, and there must also be a smallest divisor of $n$ that is greater than $1$
- Assume $d$ is _not_ a prime
- If $d$ is not a prime, it has a divisor $e$ such that $1 < e < d$
- If $e|d$ and $d|n$, then $e|n$ (see [Transitivity of Divisors](#transitivity-of-divisors))
- So $e$ is a divisor of $n$, and $e$ is also smaller than $d$; but $d$ is the smallest divisor of $n$ (this is a contradiction)

# [Euclid's Lemma](https://en.wikipedia.org/wiki/Euclid%27s_lemma)

If $p$ is prime, and $p|ab$, where $ab$ is the product of two integers $a$ and $b$, then $p$ must divide either $a$ or $b$.

Conversely, if $p$ is composite, and $p|ab$, then $p$ may or may not divide $a$ or $b$. For example, if $p=10$, $a=4$ and $b=25$, then $p$ divides neither $a$ nor $b$ individually, but it divides $ab$.

## Proof

- Let $p$ be a prime, and $a$ an integer coprime with $p$
- Then there are integers $x$ and $y$ such that $ax + py = 1$ (this is given by [Bezout's identity](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity))
- Multiply both sides of this identity by $b$, giving $b(ax + py) = b$
- Distribute $b$ over addition, giving $bax + bpy = b$
- The term $bpy$ is self-evidently divisible by $p$
- The term $bax$ is also divisible $p$ (this is given by the [Transitivity of Divisors](#transitivity-of-divisors), because if $p|ab$, and $ab|bax$, then $p|bax$)
- Since $bpy$ and $bax$ are both divisible by $p$, their sum must also be divisible by $p$
- Therefore, since $b$ equals the sum of $bax$ and $bpy$, and the sum of $bax$ and $bpy$ is divisible by $p$, then $b$ must also be divisible by $p$

In summary, if a prime $p$ divides $ab$, and $p$ does not divide $a$ (which is another way of stating that $a$ is coprime with $p$, as given in the first step of the proof), then $p$ must divide $b$.

## Corollary to Euclid's Lemma

If $p$ is prime, then the only possible square roots of $1$ modulo $p$ are $1$ and $-1$.

This is useful because it is used to test very large integers for primality (see subsection [Finding Large Primes](#finding-large-primes) for a more thorough discussion).

## Proof
- Let $a^2 \equiv 1 \pmod{p}$, giving that $a$ is the square root of $1$ modulo $p$
- Subtract $1$ from both sides of the relation, giving $a^2 - 1 \equiv 0 \pmod{p}$
- Thus, $p$ divides $a^2-1$
- Factor the term $a^2 - 1$ into $(a+1)(a-1)$
- Thus, $p$ divides $(a+1)(a-1)$
- Since $p$ is prime, then $p$ divides either $(a+1)$ or $(a-1)$ (given by [Euclid's lemma](#euclids-lemma))
- Therefore, $a$ is congruent to either $1$ or $-1$ modulo $p$


# [Fundamental Theorem of Arithmetic](https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic)

All integers greater than $1$ are the product of a unique set of primes.

For example, $3$ and $5$ are the unique prime factors of $15$; and $2$, $2$, $3$ and $5$ are the unique prime factors $60$.

## Proof (by contradiction)

- Let $n$ be the smallest integer with two distinct prime factorizations, such that $n = p_{1} \times p_{2} \times p_{3} \times ... \times p_{j} = q_{1} \times q_{2} \times q_{3} \times ... \times q_{k}$
- Since $p_{1}$ divides $q_{1} \times q_{2} \times q_{3} \times ... \times q_{k}$, $p_{1}$ must divide some $q_{i}$ (given by [Euclid's Lemma](#euclids-lemma))
- Suppose $p_{1}$ divides $q_{1}$
- Since $p_{1}$ and $q_{1}$ are both prime, it must be the case that $p_{1} = q_{1}$
- Cancel these factors to produce $p_{2} \times p_{3} \times ... \times p_{j} = q_{2} \times q_{3} \times ... \times q_{k}$
- We now have two distinct factorizations of an integer smaller than $n$, but $n$ is the smallest integer with two distinct factorizations (this is a contradiction)

# [Euclid's Theorem](https://en.wikipedia.org/wiki/Euclid%27s_theorem)

There are an infinite number of primes.

## Proof (by contradiction)

- Assume the number of primes is finite
- Let $n$ be the product of the following set, plus $1$; that is, $p_{1} \times p_{2} \times p_{3} \times ... \times p_{k} + 1$, where $k$ is the number of primes
- Let $d$ be the smallest divisor of $n$, which must be prime (given by [Prime Factors](#prime-factors))
- None of the primes in the set is a divisor of $n$ (they are instead divisors of $n - 1$); therefore, dividing $n$ by any $p$ in the set leaves a remainder of $1$
- Therefore, $d$ is prime and it is not in the set (this is a contradiction)

# [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem)

If $a$ and $p$ are integers, and $p$ is prime, then $a^p - a$ is an integer multiple of $p$. Algebraically, this can be expressed as follows:

$a^p \equiv a \pmod{p}$

Further, if $a$ is not a multiple of $p$, then the following also holds:

$a^{p-1} \equiv 1 \pmod{p}$

This is because if $a$ is not a multiple of $p$, then $a$ and $p$ are coprime, and by the [rule of cancellation](#rule-of-cancellation) the first relation can be transformed to the second in the following way:

- $a^p \equiv a \pmod{p}$
- $a^p \times a^{-1} \equiv a \times a^{-1} \pmod{p}$
- $a^{p-1} \equiv 1 \pmod{p}$

Conversely, $a^{p-1} \equiv 1 \pmod{p}$ does _not_ hold if $a$ is a multiple of $p$. In that case, $a^{p-1} \equiv 0 \pmod{p}$.

To summarize, $a^{p-1} \equiv 1 \pmod{p}$ holds if $a$ and $p$ are integers, $p$ is prime, $0 < a < p$ or, if $a > p$, $p$ does not divide $a$.

## Proof:
Consider the set of integers modulo a prime $p$ that are also coprime with $p$ (recall for a prime $p$, this is every postitive integer that is _not_ a multiple of $p$). This set consists of the integers $1, 2, 3, ..., p-1$, and forms a [_group_](#groups) under multiplication. Consider a second set $1a, 2a, 3a, ..., (p-1)a$, where $a$ is some element from the first set. Since all integers modulo $p$ (and coprime with $p$) are in the set $1, 2, 3, ..., (p-1)$, all elements of the second set, when reduced modulo $p$, must exist in the first set. Further, if we assume that the elements of the second set are a [_rearrangement_](#rearrangement) of the elements of first set, then we have:

- $a \times 2a \times 3a \times ... \times (p-1)a \equiv 1 \times 2 \times 3 \times ... \times (p-1) \pmod{p}$
- $a^{p-1}(p-1)! \equiv (p-1)! \pmod{p}$
- $a^{p-1} \equiv 1 \pmod{p}$

This completes the proof. Note that it is permissible to remove the term $(p-1)!$ from both sides of the relation by the [rule of cancellation](#rule-of-cancellation).

### Rearrangement
Consider the set of integers modulo a prime $p$ and coprime with $p$; i.e., $1, 2, 3, ..., p-1$. Consider a  second set modulo $p$ that consists of the elements $1a, 2a, 3a, ..., (p-1)a$, where $a$ is some element from the first set. Then the elements of the second set are a _rearrangement_ of the elements of the first set.

First we must prove that all elements of the second set exist in the first set. Let $k$ be some element of the first set, which by definition is coprime with $p$ (because it is less than $p$ and the only divisors of $p$ are $1$ and $p$ itself). Since $a$ also comes from the first set, it too is coprime with $p$ . By [Euclid's lemma](#euclids-lemma), the product of $k$ and $a$ must also be coprime with $p$. Therefore, all elements from the second set, when reduced modulo $p$, must exist in the first set.

Second, we must prove that all elements of the second set are _distinct_. Let $k$ and $m$ be elements from the first set. Then we can write:

- $ka \equiv ma \pmod{p}$
- $k \equiv m \pmod{p}$ (by the [rule of cancellation](#rule-of-cancellation))
- $k = m$

Since $k$ and $m$ are both members of the first set, then $k$ must equal $m$. Therefore, all elements of the second set must be distinct.

### Rule of Cancellation
Given integers $u$, $x$, $y$ and $z$, and $ux \equiv uy \pmod{z}$, if $u$ and $z$ are coprime, then the term $u$ can be _cancelled_ from both sides of the relation:

- $ux \equiv uy \pmod{z}$
- $ux \times u^{-1} \equiv uy \times u^{-1} \pmod{z}$
- $x \equiv y \pmod{z}$

Multiplication by $u^{-1}$ is permissible because $u$ and $z$ are coprime, and therefore $u$ has an inverse modulo $z$. A notable consequence of this rule is that if $z$ is prime, then $z$ must divide $x-y$.

- $x \equiv y \pmod{z}$
- $x - y \equiv y - y \pmod{z}$
- $x - y \equiv 0 \pmod{z}$

Stated another way, if $z$ is prime, and $z$ does not divide $u$, then it must divide $x-y$.

- $ux \equiv uy \pmod{z}$
- $ux - uy \equiv 0 \pmod{z}$
- $u(x-y) \equiv 0 \pmod{z}$

By [Euclid's Lemma](#euclids-lemma), since $z$ is prime, it must divide either $u$ or $x-y$, and since it does not divide $u$ (recall $u$ and $z$ are coprime), $z$ must therefore divide $x-y$.

# [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem)

If $a$ and $n$ are integers, then $a^{\phi(n)+1} - a$ is an integer multiple of $n$. Algebraically, this can be expressed as follows:

$a^{\phi(n)+1} \equiv a \pmod{n}$

Further, if $a$ and $n$ are coprime, then the following also holds:

$a^{\phi(n)} \equiv 1 \pmod{n}$

This is because if $a$ and $n$ are coprime, by the [rule of cancellation](#rule-of-cancellation) the first relation can be transformed to the second in the following way:

- $a^{\phi(n)+1} \equiv a \pmod{n}$
- $a^{\phi(n)+1} \times a^{-1} \equiv a \times a^{-1} \pmod{n}$
- $a^{\phi(n)} \equiv 1 \pmod{n}$

Conversely, $a^{\phi(n)} \equiv 1 \pmod{n}$ does _not_ hold if $a$ and $n$ are not coprime.

To summarize, $a^{\phi(n)} \equiv 1 \pmod{n}$ holds if $a$ and $n$ are coprime integers.

Euler's theorem is a generalization of Fermat's little theorem, since $n$ can be either prime (Fermat) or the product of primes (Euler).

Recall that $\phi(n)$ gives the number of integers between $1$ and $n$ that are coprime with $n$. Therefore, if $n$ is prime, then $\phi(n) = n - 1$, and we have $a^{n-1} \equiv 1 \pmod{n}$ (Fermat).

Euler's totient function is _multiplicative_, meaning that if two integers $p$ and $q$ are relatively prime, then $\phi(pq) = \phi(p) \times \phi(q) = (p-1)(q-1)$.

There are many proofs of Euler's theorem, including a generalized version of the proof of [Fermat's little theorem](#fermats-little-theorem) presented above. The following proof uses [Lagrange's theorem](#lagranges-theorem).

## Proof:
- Let $n$ be a positive integer (that is not necessarily prime)
- Let $G$ be the set $\lbrace 1 \le a \le n-1 : gcd(a,n) = 1\rbrace$ (which in group theory is called _the multiplicative group modulo_ $n$).
- Let $a$ be a member of this group
- Let $k$ be the order $a$; i.e., the smallest integer such that $a^k \equiv 1 \pmod{n}$
- Then the numbers $a, a^2, ..., a^k$ modulo $n$ form a subgroup of $G$ whose order is $k$
- By Lagrange's theorem, $k$ divides the order of $G$, or $\phi(n)$
- Then $\phi(n) = km$ for some integer $m$
- Therefore, $a^{\phi(n)} = a^{km} = (a^{k})^m \equiv 1^m \equiv 1 \pmod n$

A corollary to Euler's theorem&mdash;and one that is crucial to understanding the RSA algorithm&mdash;is that for any integers $x$ and $y$, $x \equiv y \pmod{\phi(n)}$ implies $a^x \equiv a^y \pmod{n}$, if $a$ is coprime to $n$. This is proven as follows:

- $x \equiv y \pmod{\phi(n)}$
- $x - y = \phi(n)k$, for some integer $k$
- $x = y + \phi(n)k$
- $a^x = a^{y+\phi(n)k} = a^y(a^{\phi(n)})^{k} \equiv a^y1^k \equiv a^y \pmod{n}$

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

The Chinese Remainder Theorem (CRT) is used in RSA to accelerate otherwise intolerably expensive exponentiations.

# Finding Large Primes
Primality&ndash;testing algorithms based on trial division are not feasible for primes of the size necessary for use in cryptographic applications. Even though the time complexity of these algorithms is linear, their candidate inputs are so large that even linear&ndash;time algorithms are too slow. (How slow? they would require many millions of years to complete on a classical computer.)

However, combining some theorems and lemmas from above, we can identify very large, cryptographically suitable primes using an algorithm of logarithmic time complexity. Perhaps the most widely utilized of these is the [Miller&ndash;Rabin](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test) algorithm, which in its accepted form was developed by Michael Rabin in 1980 (Rabin's variant is probabalistic, and builds on a deterministic version of the algorithm established by Gary Miller in 1976; hence _Miller&ndash;Rabin_ algorithm).

There is another very well&ndash;known primality test known as the [Fermat primality test](https://en.wikipedia.org/wiki/Fermat_primality_test) (because it is based on [Fermat's little theorem](#fermats-little-theorem)). This test is inferior to Miller&ndash;Rabin, however, due to the existence  _Carmichael_ numbers which, although rare, defeat the Fermat test.

## Lemmas Used in The Miller&ndash;Rabin Algorithm

- [Fermat's little theorem](#fermats-little-theorem), which states that if $p$ is prime, then $a^{p-1} \equiv 1 \pmod{p}$, where $1 < a < p$.
- [Euclid's lemma](#euclids-lemma), which states that if $p$ is prime, and $p|ab$, where $ab$ is the product of two integers $a$ and $b$, then $p$ must divide either $a$ or $b$.

## Miller&ndash;Rabin Algorithm

The Miller&ndash;Rabin algorithm leverages the fact that if $p$ is prime, then the square root of $1$ modulo $p$ is either $1$ or $-1$. Conversely, if the square root of $p$ modulo $1$ is neither $1$ nor $-1$, then $p$ must be composite (see [corollary to Euclid's Lemma](#corollary) for a more general proof).

### Proof

- By Fermat, we have that if $p$ is prime, then $a^{p-1} \equiv 1 \pmod{p}$
- If we subtract $1$ from both sides of this relation, we get $a^{p-1} - 1 \equiv 0 \pmod{p}$
- Therefore, $p$ divides $a^{p-1} - 1$
- The square root of $a^{p-1}$ is $a^{(p-1)/2}$, so by the [difference of squares](#difference-of-two-squares) we can rewrite $a^{p-1} - 1$ as $(a^{(p-1)/2} + 1)(a^{(p-1)/2} - 1)$
- By [Euclid's lemma](#euclids-lemma), we have that if $p$ is prime, then $p$ divides at least one of the terms $(a^{(p-1)/2} + 1)$ or $(a^{(p-1)/2} - 1)$
- Therefore, the square root of $a^{p-1}$ (or $a^{(p-1)/2}$) is congruent to either $1$ or $-1$ modulo $p$

Stated generally, if $p$ is prime, then the square root of $a^{p-1}$ (which by Fermat we know to be congruent to $1$ modulo $p$) must either also be congruent to $1$ modulo $p$ or, if it is not, then it must be congruent to $-1$ modulo $p$.

Specifically, with regard to the Miller&ndash;Rabin algorithm, if the square root of $a^{p-1}$ is _not_ congruent to either $1$ or $-1$ modulo $p$, then $p$ must be composite. We can use this fact to test for the compositeness of an integer that runs in logarithmic time in the size of the input.

# [Difference of Two Squares](https://en.wikipedia.org/wiki/Difference_of_two_squares)

Every odd number $n$ can be expressed as the difference of two squares, such that $n=b^2-a^2$ for two integers $a$ and $b$.

## Proof
- If $n$ is an odd integer, then $n = 2k+1$ trivially for some integer $k$
- Let $a=k$
- Let $b=k+1$
- Then $n = (k+1)^2 - k^2$
- $n = (k+1)(k+1) - k^2$
- $n = k^2 + 2k+1 - k^2$
- $n = 2k+1$

# [Fermat's Factorization Algorithm](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method)

Attempts to factor a composite odd integer $n$, where $n$ is the product of exactly two distinct prime factors $p$ and $q$ (e.g., an RSA modulus). If $n$ can be factored using this algorithm, then the difference of its factors is too small, and the factors therefore cryptographically weak. Suitable factors of an RSA modulus should be distant enough to defeat this algorithm.

Note that if $n$ is an RSA modulus it cannot be even; otherwise one of its factors would be $2$.

1. Set $i$ to the integer floor of the square root of $n$
2. Set $a=i+1$
3. Set $b=a^2 - n$
4. If $b$ is _not_ a perfect square, set $a=a+1$ and go to step 3; otherwise, $(a+b)$ and $(a-b)$ are the factors of $n$ and we're done
5. Repeat steps 3 and 4 until $b$ is a perfect square, or a sensible number of attempts has been made.

Fermat's factorization algorithm is based on the fact that any odd integer $n$ can be expressed as the [difference of two squares](#difference-of-two-squares), i.e., $n = b^2 - a^2$ for two integers $a$ and $b$. The right&ndash;hand side of this equation can be factored into $(b+a)(b-a)$. And if $(b+a) \ne 1$ and $(b-a) \ne 1$, then $(b+a)(b-a)$ is a nontrivial factorization of $n$.

# [Shor's Factorization Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)

Attempts to factor a composite odd integer $n$, where $n$ is the product of exactly two distinct prime factors $p$ and $q$ (e.g., an RSA modulus).

In 1994, Peter Shor proposed an algorithm that would run in polynomial time on a sufficiently powerful quantum computer. As of the time of this writing, no such computer is known to exist. Though purely theoretical, the algorithm can nevertheless be executed on a classical computer (albeit with exponential time complexity).

The algorithm reduces the problem of factoring to one of _order&ndash;finding_, and leverages the fact that the order of any element in the finite multiplicative group of integers modulo $n$ divides the order of $n$.

The classical (i.e., non-quantum) variant runs as follows:

1. Set $a$ to a value randomly selected from the range $[2..n-1]$
2. Set $g = gcd(a,n)$
3. If $g \ne 1$, then $g$ and $n/g$ are the nontrivial factors of $n$ and we are done
4. Set $r = 1$
5. While $a^r \bmod n \ne 1$, set $r = r+1$
6. If $r$ is even, set $s$ = $a^{r/2} \bmod n$; otherwise, if $r$ is odd, return to step 1
7. If $s \ne n-1$, then $gcd(s-1, n)$ and $gcd(s+1,n)$ are the nontrivial factors of $n$ and we are done; otherwise, return to step 1.

Step 5&mdash;which is the order&ndash;finding part of the algorithm&mdash;is the bottleneck, and would take millions of years to run against a proper RSA modulus on even the most powerful classical computer. On a sufficiently large quantum computer, however, the order of $a$ can be identified in polynomial time using a [quantum fourier transform](https://en.wikipedia.org/wiki/Quantum_Fourier_transform).

## Proof

* Let $n$ be a semiprime integer
* Let $r$ be the smallest integer such that $a^r \equiv 1 \pmod n$ for some integer $a$, where $1 < a < n$ (if $r$ is odd, start over with another $a$)
* Therefore, $n$ divides $a^r - 1$ (also note that $r$ divides $\phi(n)$)
* Let $s = a^{r/2}$ (this is the square root of $a^r$)
* It cannot be the case that $s \equiv 1 \pmod n$, because $a^r \equiv 1 \pmod n$, and $r$ is the smallest integer such that $a^r \equiv 1 \pmod n$
* If it is instead the case that $s \equiv -1 \pmod n$, then $n$ divides $s+1$, and $s+1$ is a trivial factor of $n$
* Otherwise, $s \not \equiv 1 \pmod n$ _and_ $s \not \equiv -1 \pmod n$, and therefore neither $s-1$ nor $s+1$ is a multiple of $n$, but their product is; i.e., $a^r-1 = (a^{r/2}-1)(a^{r/2}+1) = (s-1)(s+1) \equiv 0 \pmod n$ (see [Euclid's lemma](#euclids-lemma))
* Therefore, the prime factors of $n$ must share factors with $(s-1)$ and $(s+1)$
* Let $p=gcd(n,s-1)$ and $q=gcd(n,s+1)$
* Then $p$ and $q$ are the prime factors of $n$

# Finite Fields

- Any integer taken modulo a prime $p$ is always in the range $0, ..., p - 1$.
- The set of integers modulo a prime $p$ is a [_finite field_](https://en.wikipedia.org/wiki/Finite_field).
- You can always add or subtract any multiple of $p$ without changing the result (see [_congruence relation_](https://en.wikipedia.org/wiki/Congruence_relation)).
- Results of the binary operations of addition subtraction and are always in the range $0, 1, ..., p - 1$.
- The finite field of integers modulo $p$ is written $\mathbb{Z}_{p}$.

# Groups

- A [_group_](<https://en.wikipedia.org/wiki/Group_(mathematics)>) is a [finite field](#finite-fields) together with a single binary operation (such as addition or multiplication).
- The numbers in $\mathbb{Z}_{p}$ form a group together with addition; one can add or subtract any two numbers in the group and the result will be a number in the group.
- There is another group whose operator is multiplication. However, this group cannot contain 0 (because division by 0 is undefined). It consists of the set $1, ..., p - 1$. This group is known as the _muliplicative group_ modulo $p$, and is written $\mathbb{Z_p^*}$.
- A group can contain one or more _subgroups_, which are subsets of the elements in the full group.
- If you apply the group operator to two elements in a subgroup, you again get an element in the subgroup.

# Muliplicative Groups Modulo a prime $p$

- Each member $g$ of a group $G$ has an [_order_](<https://en.wikipedia.org/wiki/Order_(group_theory)>), which is the smallest integer exponent $q$ such that $g^q \equiv 1 \pmod{p}$.
- The group $G$ and its subgroups are [_cyclic_](https://en.wikipedia.org/wiki/Cyclic_group).
- In the multiplicative group modulo $p$, there is at least one $g$ that generates the entire group $G$. Such a $g$ is called a _primitive element_, or _generator_, of the group.
- Other values of $g$ generate smaller sets, or _subgroups_, of $G$.
- Multiplication or division of any two elements in the group or subgroup generated by $g$ yield another element in that group or subgroup.
- For any element $g$, the order of $g$ is a divisor of $p - 1$ (see [Lagrange's theorem](#lagranges-theorem))

# Multiplication Modulo a composite $n$

- The integers modulo a composite $n$ are $0, 1, ..., n - 1$.
- These integers do not form a finite field, but rather a [_ring_](<https://en.wikipedia.org/wiki/Ring_(mathematics)>).
- For a composite $n$ that is the product of exactly two distinct odd primes $p$ and $q$ (e.g., an RSA modulus), there is an exponent $t$ such that $x^t \equiv 1 \pmod{n}$ for _almost_ all $x$; the exceptions are values of $x$ that are multiples of either $p$ or $q$.
- The frequency of such exceptions is in the proportion $\displaystyle \frac{(p+q)}{pq}$, and diminishes quadratically in the size of $pq$.
- The smallest $t$ that is a multiple of $p - 1$ and $q - 1$ is their least common mulitple, or $lcm(p-1, q-1)$.

# Greatest Common Divisor

- The greatest common divisor (GCD) of two integers $a$ and $b$ is the largest integer $k$ such that $k|a$ and $k|b$.
- The [Euclidean Algorithm](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md) computes the GCD of two integers in logarithmic time.

# Least Common Multiple

- The least common multiple (LCM) of two integers $a$ and $b$ is smallest $k$ such that $k$ is a multiple of both $a$ and $b$; it is found by $\displaystyle \frac{ab}{gcd(a, b)}$.
- Whereas the original RSA whitepaper specifies that $\phi(pq)$&mdash;which recall is $(p-1)(q-1)$&mdash;be used to compute private exponents, in practice $lcm(p-1, q-1)$ is used instead because it results in smaller, and therefore more efficient (albeit no less secure), exponents.

# The Extended Euclidean Algorithm

- Division is not possible in a multiplicative group, because division can produce fractional results.
- Therefore, to _simulate_ division in a multiplicative group, we use the [Extended Euclidean
  Algorithm](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md).
- This can be thought of as _multiplication by an inverse_ in the real numbers. For example, $\frac{5}{2}$ (division) is the same as $5 \times \frac{1}{2}$ (multiplication). In the latter, we multiply $5$ by the _inverse_ of $2$, or $\frac{1}{2}$. Both operations yield the same result, which is $2 \frac{1}{2}$.
- The extended euclidean algorithm finds two integers $u$ and $v$ such that $ua + vb = gcd(a, b)$, which allows one to compute the mulitiplicative inverse of an integer modulo $p$.
