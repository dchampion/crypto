# Definitions

## Theorem

A statement that has been proven to be true.

## Lemma

A minor statement of fact that can be used in the construction of a theorem.

## Proof

Argues why a lemma or theorem is true. A special case is a proof by contradiction, which proves a lemma or theorem by assuming it is not true and demonstrating that this is a contradiction.

# Notation

The symbol | means <i>divides</i>. For example, $a|b$ means <i>a</i> divides <i>b</i> without leaving a remainder.

The symbol $\equiv$ means _is equivalent to_, as in the congruence relation $a \equiv b \pmod{c}$. In such a relation, $a - b$ is a multiple of $c$.

The symbol $\phi$ (aka _phi_, a letter in the Greek alphabet) denotes [_Euler's Totient Funtion_](https://en.wikipedia.org/wiki/Euler%27s_totient_function), as in $\phi(n)$, where $n$ is some positive integer. For any positive integer $n$, $\phi(n)$ gives the number of integers between 1 and $n$ that are [_coprime_](https://en.wikipedia.org/wiki/Coprime_integers), or [_relatively prime_](https://en.wikipedia.org/wiki/Coprime_integers), to $n$.

# Transitivity of Divisors Lemma

If $a|b$ and $b|c$, then $a|c$.

## Proof:

- If $a|b$, then there is an integer $k$ such that $ak = b$
- If $b|c$, then there is an integer $l$ such that $bl = c$
- Therefore, $c = bl = (ak)l = a(kl)$

# Prime Factors Lemma

Let $n$ be a positive number greater than 1. Let $d$ be the smallest divisor of $n$ that is greater than 1. Then $d$ is prime.

## Proof (by contradiction):

- $n$ is a divisor of $n$, and $n > 1$; therefore, there is at least one divisor of $n$ that is greater than 1, and there must also be a smallest divisor of $n$ that is greater than 1
- Assume $d$ is not a prime
- If $d$ is not a prime, it has a divisor $e$ such that $1 < e < d$
- If $e|d$ and $d|n$ then $e|n$ (see transitivity of divisors lemma)
- So $e$ is a divisor of $n$ and $e$ is also smaller than $d$; but $d$ is the smallest divisor of $n$ (this is a contradiction)

# Infinite Primes Theorem

There are an infinite number of primes.

## Proof (by contradiction):

- Assume the number of primes is finite
- Let $n$ be the product of this finite set, plus one; that is, $p_{1} \times p_{2} \times p_{3} ...\times p_{k} + 1$, where $k$ is the finite number of primes.
- Let $d$ be the smallest divisor of $n$, which must be prime (see prime factors lemma)
- None of the primes in the set is a divisor of $n$ (they are instead divisors of $n - 1$); therefore, dividing $n$ by any $p$ in the set leaves a remainder of 1
- Therefore, $d$ is prime and it is not in the set (this is a contradiction)

# Fundamental Theorem of Aritmetic

All integers greater than 1 are the product of a unique set of primes. For example, 3 and 5 are the prime factors of 15, and only 15. Similarly, 2, 2, 3 and 5 are the prime factors 60, and only 60.

# [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem)

$a^p \equiv a \pmod{p}$, where $a$ is a positive integer not divisible by $p$, and $p$ is prime.

It therefore follows that $a^{p-1} \equiv 1 \pmod{p}$ for the same $a$ and $p$.

# [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem)

$a^{\phi(n)} \equiv 1 \pmod{n}$, where $a$ and $n$ are coprime positive integers.

It therefore follows that $a^{\phi(n)+1} \equiv a \pmod{n}$ for the same $a$ and $n$.

# Computations Modulo a Prime

## Finite Fields

- Any integer taken modulo a prime $p$ is always in the range $0, ..., p - 1$.
- The set of integers modulo a prime $p$ is a [_finite field_](https://en.wikipedia.org/wiki/Finite_field).
- You can always add or subtract any multiple of $p$ without changing the result (see [_congruence relation_](https://en.wikipedia.org/wiki/Congruence_relation)).
- Results are always in the range $0, 1, ..., p - 1$.
- The finite field of integers modulo $p$ is written $\mathbb{Z}_{p}$.

## Groups

- A [_group_](<https://en.wikipedia.org/wiki/Group_(mathematics)>) is a finite field together with a binary operation, such as addition or multiplication.
- The numbers in $\mathbb{Z}_{p}$ form a group together with addition; you can add or subtract any two numbers in the group and the result will be a number in the group.
- A group whose operator is multiplication cannot contain 0 (because you cannot divide by 0), and consists of the set $1, ..., p - 1$; this is known as the _muliplicative group_ modulo $p$, and is written $\mathbb{Z^*}_{p}$.
- A group can contain _subgroups_, which consist of a subset of the elements in the full group.
- If you apply the group operator to two elements in a subgroup, you again get an element in the subgroup.

## Greatest Common Divisor

- The greatest common divisor (_GCD_) of two positive integers $a$ and $b$ is the largest integer $k$ such that $k|a$ and $k|b$.
- The [_Euclidean Algorithm_](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md) computes the GCD of two integers in logarithmic time.

## Least Common Multiple

- The least common multiple (_LCM_) of two positive integers $a$ and $b$ is smallest $k$ such that $k$ is a multiple of both $a$ and $b$; it is found by $ab / gcd(a, b)$.

## The Extended Euclidean Algorithm

- Division is not possible in a multiplicative group, because division can produce fractional results.
- Therefore, to _simulate_ division in a multiplicative group, we use the [_Extended Euclidean Algorithm_](https://github.com/dchampion/crypto/blob/master/doc/EuclideanAlgorithms.md).
- This algorithm finds two integers $u$ and $v$ such that $gcd(a, b) = ua + vb = 1$, which allows us to compute the mulitiplicative inverse of an integer modulo $p$.
- This can be thought of as _multiplication by an inverse_ in the real numbers. For example, $5 / 2$ (division) is the same as $5 \times \frac{1}{2}$ (multiplication). In the latter, we multiply $5$ by the _inverse_ of $2$, or $\frac{1}{2}$. Both operations yield the same result, which is $2 \frac{1}{2}$.

## Muliplicative Groups Modulo a prime $p$

- Each member $g$ of a group $G$ has an [_order_](<https://en.wikipedia.org/wiki/Order_(group_theory)>), which is the smallest positive integer exponent $q$ such that $g^q \equiv 1 \pmod{p}$.
- The group $G$ and its subgroups are [_cyclic_](https://en.wikipedia.org/wiki/Cyclic_group).
- In the multiplicative group modulo $p$, there is at least one $g$ that generates the entire group $G$. Such a $g$ is called a _primitive element_, or _generator_, of the group.
- Other values of $g$ generate smaller sets, or _subgroups_, of $G$.
- Multiplication or division of any two elements in the group or subgroup generated by $g$ yield another element in that group or subgroup.
- For any element $g$, the order of $g$ is a divisor of $p - 1$.

## Multiplication Modulo a composite $n$

- The integers modulo $n$, where $n$ is the product of exactly two primes $p$ and $q$, are $0, 1, ..., n - 1$.
- These integers do not form a finite field, but rather a [_ring_](<https://en.wikipedia.org/wiki/Ring_(mathematics)>).
- For any prime $p$, for all $x$ where $0 < x < p$, the congruence relation $x^{p-1} \equiv 1 \pmod{p}$ holds. This is [_Fermat's Little Theorem_](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem).
- For a composite $n$ that is the product of exactly two primes $p$ and $q$, there is an exponent $t$ such that $x^t \equiv 1 \pmod{n}$ for _almost_ all $x$
- The exceptions to this are values of $x$ that are multiples of either $p$ or $q$.
- The frequency of such exceptions is in the proportion $(p + q) / pq$, and diminishes quadratically in the size of $pq$.
- The smallest $t$ that is a multiple of $p - 1$ and $q - 1$ is their least common mulitple, or $lcm(p - 1, q - 1)$.

## The Chinese Remainder Theorem

- The numbers modulo a composite $n$, where $n$ is the product of exactly two primes $p$ and $q$, are $0, 1, ..., n - 1$.
- This is not a finite field (as it would be if $n$ were prime), but rather a [_ring_](<https://en.wikipedia.org/wiki/Ring_(mathematics)>), and is denoted $\mathbb{Z}_{n}$.
- Each $x$ in $\mathbb{Z}_{n}$ corresponds to a unique pair ($x \bmod{p}, x \bmod{q}$).
- Given the pair ($x \bmod{p}, x \bmod{q}$), you can efficiently compute $x$.
- This efficiency can be leveraged in RSA to speed up the expensive operations of decryption and digital signature.
