# Euclidean Algorithms
## Using the Euclidean Algorithm to Find the Greatest Common Divisor of Two Positive Integers

_Implementations of these algorithms in the Python programming language can be found [here](https://github.com/dchampion/crypto/blob/master/src/core/euclid.py)._

In the procedure for RSA encryption described in [_The Elements of Public Key Cryptography_](https://raw.githubusercontent.com/dchampion/crypto/master/doc/TheElementsOfPublicKeyCryptography.pdf), step 5 requires Alice to compute an encryption exponent $e$.

Recall that the requirement for $e$ is that it be a positive integer that is relatively prime to the totient of $n$, or $\phi(n)$. Recall that $n$ is the product of the two primes $p$ and $q$, which in the example are $7$ and $11$, respectively, thus giving us $n=77$. And recall that the totient of $77$, or $\phi(77)$, is $60$ (because there are $60$ integers in the range $1$ to $77$ that are relatively prime to $77$). Another way of saying this is that there are $60$ integers in the range $1$ to $77$ whose _greatest common divisor_ (shortened hereafter to $gcd$) with $77$ is $1$.

The Euclidean Algorithm gives us an efficient method for finding the $gcd$ of two integers, which is especially useful for real&ndash;world, cryptographically strong (i.e., very large) numbers. We'll demonstrate it here, using the small numbers from the example, to compute a suitable encryption exponent $e$.

In the present case we must identify a value in the range $1$ to $60$ whose $gcd$ with $60$ is $1$, expressed algebraically as $gcd(60,e)=1$. We must use such a value for $e$ because it will have an inverse in the group of integers modulo $60$ (values with a $gcd$ greater than $1$ will not have an inverse), and we need an inverse in order to decrypt messages.

We find the $gcd$ of two integers by taking the larger integer modulo the smaller, recursively, until we reach $0$. For example, let's randomly select the value $8$ as a candidate for $e$. To find the $gcd$ of $60$ and $8$, we do the following:

<pre>
gcd(60,8) = gcd(60 mod 8,8) -> 60 mod 8 = 4
          = gcd(4,8)        -> Result of previous operation
          = gcd(8,4)        -> Swap parameters
          = gcd(8 mod 4,4)  -> 8 mod 4 = 0
          = gcd(0,4)        -> Result of previous operation
          = 4               -> Stop when parameter reaches 0; remaining non-zero parameter is gcd
</pre>

When $0$ is reached, the remaining non&ndash;zero parameter&mdash;$4$ in this case&mdash;is the $gcd$.

Of course, with small parameters, like $60$ and $8$, we can skip the ceremony and work out in our heads that $4$ is the biggest number that divides both. But for very large numbers we need the help of the Euclidean Algorithm. Because $gcd(60,8)>1$, $8$ is not suitable for use as an encryption exponent.

Let's try again, this time with $7$:

<pre>
gcd(60,7) = gcd(60 mod 7,7) -> 60 mod 7 = 4
          = gcd(4,7)        -> Result of previous operation
          = gcd(7,4)        -> Swap parameters
          = gcd(7 mod 4,4)  -> 7 mod 4 = 3
          = gcd(3,4)        -> Result of previous operation
          = gcd(4,3)        -> Swap parameters
          = gcd(4 mod 3,3)  -> 4 mod 3 = 1
          = gcd(1,3)        -> Result of previous operation
          = gcd(3,1)        -> Swap parameters
          = gcd(3 mod 1,1)  -> 3 mod 1 = 0
          = gcd(0,1)        -> Result of previous operation
          = 1               -> Stop when parameter reaches 0; remaining non-zero parameter is gcd
</pre>

Here we have $gcd(60,7)=1$, because $1$ is the largest remaining non&ndash;zero parameter when we reach $0$. Since $gcd(60,7)=1$, Alice can use $7$ as the encryption exponent $e$ in her RSA parameter setup.

A second method of computing $gcd$&mdash;which will prove useful when we use an extended version the Euclidean Algorithm to find the inverse of $e$&mdash;is to express each step in terms of divisors, quotients and remainders.

To demonstrate, let's apply this second method to $gcd(60,7)$:

<pre>
gcd(60,7) = 60 = 7(8) + 4 -> 60 is 7 (divisor) times 8 (quotient), plus 4 (remainder)
             7 = 4(1) + 3 -> Shift previous divisor and remainder left and repeat
             4 = 3(1) + 1 -> Shift previous divisor and remainder left and repeat
             3 = 3(1) + 0 -> Stop at 0
</pre>

The last non&ndash;zero remainder is $1$, which is the $gcd$ of $60$ and $7$.

## Using the _Extended_ Euclidean Algorithm to Find the Inverse of the Encryption Exponent
Now that Alice has identified her encryption exponent $e$, she must next find a suitable decryption exponent $d$. This number must be the inverse of $e$ (which is $7$ in the present example) in the group of integers modulo $\phi(77)$. This exponent will be used by Alice to recover the plaintext from a message $M$ encrypted with the procedure $M^e \bmod n$ (where $M$ is a natural number in the range 1 to $n-1$, $e=7$ and $n=77$).

That is, we are looking for a decryption exponent $d$  that satisfies the equation $ed \bmod \phi(n) = 1$ or, plugging in the values we know so far, $7d \bmod 60 = 1$. Soving for $d$ in this equation will tell us by what integer $e$ must be multiplied to produce $1 \bmod \phi(n)$.

To find the answer, we'll use the divisors, quotients and remainders version of the Euclidean Algorithm presented in the previous section, but with a small enhancement.

To preface a bit, we'll start with a short discussion of B&eacute;zout's identity, from which the enhanced method derives.

B&eacute;zout's identity asserts the following:

$ax + by = gcd(a,b)$

In English, B&eacute;zout's identity asserts that for any given positive integers $a$ and $b$, there are integer solutions $x$ and $y$ such that $ax + by = gcd(a,b)$. In the present example, since we know that $gcd(a,b)=1$ (where $a=60$ and $b=7$), we can rewrite the identity as follows:

$ax + by = 1$

And since we are looking for the inverse of $7$ in the group of integers modulo $60$, we can substitute $60$ for $a$ and $7$ for $b$, thus further fleshing out the identity as follows:

$60x + 7y = 1$

Specifically, we are interested in the value $y$ that, when mulitplied by $7$, and added to some multiple of $60$ (i.e., $60x$, for some integer $x$), results in $1$ modulo $60$. This value will be the inverse of $7$ in the group of integers modulo $60$ or, expressed algebraically, $7y = 1 \pmod{60}$.

First, we repeat the divisors, quotients and remainders version of the Euclidean Algorithm demonstrated in the previous section to find $gcd(60,7)$:

<pre>
GCD(60,7) = 60 = 7(8) + 4
             7 = 4(1) + 3
             4 = 3(1) + 1 -> Last non-zero remainder is GCD
             3 = 3(1) + 0 -> Stop at 0
</pre>

Next, we rewrite each line of the previous procedure (except the stop&ndash;line in which the remainder is $0$), subtracting the divisor and quotient from both sides to isolate the remainder on the right&ndash;hand side of the equation:

<pre>
60 = 7(8) + 4 becomes 60 - 7(8) = 4
 7 = 4(1) + 3 becomes  7 - 4(1) = 3
 4 = 3(1) + 1 becomes  4 - 3(1) = 1
</pre>

Finally, starting from the bottom up, where the last remainder is $1$, we use backward substitution to work our way to a solution for $ax + by = 1$.

<pre>
1 = 4 - 3(1)          -> Start with last equation
  = 4 - 3             -> Simplify 3(1)
  = 4 - (7 - 4(1))    -> Substitute 3 with (7 - 4(1)) from previous equation
  = 4 - (7 - 4)       -> Simplify 4(1)
  = 4 - 7 + 4         -> Distribute
  = 2(4) - 7          -> Combine 4s
  = 2(60 - 7(8)) - 7  -> Substitute 4 with (60 - 7(8)) from previous equation
  = 2(60) - 16(7) - 7 -> Distribute
  = 2(60) - 17(7)     -> Combine 7s and we're done!
</pre>

To test the result, verify that $2(60) - 17(7) = 1$ (it does). In this case, $60$ and $7$ represent our givens $a$ and $b$, and $2$ and $-17$ our variables $x$ and $y$, respectively. This means that the value of $y$, or $-17$, is the inverse of $7$ in the group of integers modulo $60$.

But we're not quite done yet. Since we are working modulo $60$, we need to take $-17$ modulo $60$, and $-17 \bmod 60 = 43$. This means that $43$ is the inverse of $7$ in the group of integers modulo $60$. We can test this result by plugging it into the equation $ed \bmod 60 = 1$, where $e=7$ and $d=43$. Indeed, $7 \times 43 = 301$; and $301 \bmod 60 = 1$.

Therefore, $43$ is the value Alice must use for her decryption exponent $d$, in order to successfully decrypt messages encrypted with her encryption exponent $e$.