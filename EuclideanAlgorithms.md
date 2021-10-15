# Euclidean Algorithms
## Using the Euclidean Algorithm to Find the Greatest Common Divisor (<i>GCD</i>) of Two Natural Numbers
In the procedure for RSA encryption described in <a href=https://raw.githubusercontent.com/dchampion/crypto/master/TheElementsOfPublicKeyCryptography.pdf><i>The Elements of Public Key Cryptography</i></a>, step 5 of the procedure requires Alice to compute an encryption exponent <i>e</i>.

Recall that the requirement for <i>e</i> is that it be a positive integer that is relatively prime to the totient of <i>n</i>, or <i>&phi;(n)</i>. Recall that <i>n</i> is the product of two primes <i>p</i> and <i>q</i>, which in the example are 7 and 11, respectively, thus giving us <i>n</i>=77. And recall that &phi;(77)=60 (because there are 60 integers in the range 1 to 77 that are relatively prime to 77). Another way of saying this is that there are 60 integers in the range 1 to 77 whose greatest common divisor (<i>GCD</i>) with 77 equals 1.

The Euclidean Algorithm gives us an efficient method of finding the GCD of two integers, which is especially useful for real-world, cryptographically strong (i.e. very large) numbers. We'll use it here, using small numbers to demonstrate its use, to compute a suitable encryption exponent <i>e</i>.

In the present case we are looking for an encryption exponent <i>e</i> whose GCD with 60 is 1, written formulaically as <i>GCD(60,e)=1</i>. We find the GCD of two integers by taking the larger integer modulo the smaller, recursively, until we reach 0. For example, to find the GCD of 60 and 8, we do the following:
<pre>
GCD(60,8) = GCD(60 mod 8,8) -> 60 mod 8 = 4
          = GCD(4,8)        -> Result of previous operation
          = GCD(8,4)        -> Swap parameters
          = GCD(8 mod 4,4)  -> 8 mod 4 = 0
          = GCD(0,4)        -> Result of previous operation
          = 4               -> Stop when argument reaches 0
</pre>
When 0 is reached, the largest remaining parameter&mdash;4 in this case&mdash;is the GCD.

Of course, with small parameters, like 60 and 8, we can skip the ceremony and work out in our heads that 4 is the largest number that divides both. But for very large numbers we need the help of the Euclidean Algorithm. Because GCD(60,8) is greater than 1, it is not suitable for use as an encryption exponent.

Next, let's try GCD(60,7):
<pre>
GCD(60,7) = GCD(60 mod 7,7) -> 60 mod 7 = 4
          = GCD(4,7)        -> Result of previous operation
          = GCD(7,4)        -> Swap parameters
          = GCD(7 mod 4,4)  -> 7 mod 4 = 3
          = GCD(3,4)        -> Result of previous operation
          = GCD(4,3)        -> Swap parameters
          = GCD(4 mod 3,3)  -> 4 mod 3 = 1
          = GCD(1,3)        -> Result of previous operation
          = GCD(3,1)        -> Swap parameters
          = GCD(3 mod 1,1)  -> 3 mod 1 = 0
          = GCD(0,1)        -> Result of previous operation
          = 1               -> Stop when argument reaches 0
</pre>
Here the GCD is 1, because that is the largest remaining parameter when we reach 0. Since GCD(60,7)=1, Alice can use the value 7 to serve as the encryption exponent <i>e</i> in her RSA parameter setup.

A second method of computing GCD&mdash;which will prove useful when we use an extended version the Euclidean Algorithm to find the inverse of <i>e</i>&mdash;is to express each step in terms of divisors, quotients and remainders.

To demonstrate, let's apply this method to GCD(60,7) again:
<pre>
GCD(60,7) = 60 = 7(8) + 4 -> 60 is 7 times 8, plus a remainder of 4
             7 = 4(1) + 3 -> Shift previous divisor and remainder left
             4 = 3(1) + 1 -> Shift previous divisor and remainder left
             3 = 3(1) + 0 -> Stop at 0
</pre>
The last nonzero remainder is 1, which is the GCD of 60 and 7.
## Using the <i>Extended</i> Euclidean Algorithm to Find the Inverse of the Encryption Exponent
Now that Alice has identified her encryption exponent <i>e</i>, she must next find a suitable decryption exponent <i>d</i>. This number must be the inverse of <i>e</i> (which we now know to be 7) in the group of integers modulo &phi;(77). This exponent will be used by Alice to recover the plaintext from a message <i>M</i> encrypted with the procedure <i>M<sup>e</sup> mod n</i> (where <i>M</i> is a natural number in the range 1 to <i>n</i>-1, <i>e</i> is 7, <i>n</i> is 77).

That is, we are looking for a decryption exponent <i>d</i>  that satisfies the equation <i>ed mod &phi;(n) = 1</i>; this tells us by what integer <i>e</i> must be multiplied to produce 1 mod &phi;(n).

To find the answer, we use the divisors, quotients and remainders version of the Euclidean Algorithm presented in the last part of the previous section, but with a small enhancement.

To understand the mechanics of this enhancement, we'll start with a discussion of B&eacute;zout's identity, from which it follows.

B&eacute;zout's identity asserts the following:
<pre>
ax + by = gcd(a,b)
</pre>
In English, B&eacute;zout's identity asserts that for any given natural numbers <code>a</code> and <code>b</code>, there are integer solutions <code>x</code> and <code>y</code> such that <code>ax + by = gcd(a,b)</code>. In the present example, since we know that <code>gcd(a,b)=1</code> (where <code>a</code>=60 and <code>b</code>=7), we can rewrite the identity as follows:
<pre>
ax + by = 1
</pre>
And since we are looking for the inverse of 7 in the group of integers modulo 60, we can substitute 60 for <code>a</code> and 7 for <code>b</code>, thus further fleshing out the identity as follows:
<pre>
60x + 7y = 1
</pre>
Specifically, we are interested in the value <code>y</code> that, when mulitplied by 7, and added to some multiple of 60 (i.e. 60<code>x</code>), results in 1. This value is the inverse of 7 in the group of integers modulo 60 or, algebraically, <code>7y = 1 (mod 60)</code>.

First, we repeat the divisors, quotients and remainders version of the Euclidean Algorithm demonstrated in the previous section to find GCD(60,7):
<pre>
GCD(60,7) = 60 = 7(8) + 4
             7 = 4(1) + 3
             4 = 3(1) + 1 -> Last nonzero remainder is GCD
             3 = 3(1) + 0 -> Stop at 0
</pre>
Next, we rewrite each line of the previous procedure (except the stop-line in which the remainder is 0), subtracting the dividend and quotient from both sides to isolate the remainder:
<pre>
60 = 7(8) + 4 becomes 4 = 60 - 7(8)
 7 = 4(1) + 3 becomes 3 = 7 - 4(1)
 4 = 3(1) + 1 becomes 1 = 4 - 3(1)
</pre>
Finally, starting from the bottom, where the last remainder is 1, we work our way backwards, using substitution to work our way to a solution for <code>ax + by = 1</code>.
<pre>
1 = 4 - 3(1)          -> Start with last line
  = 4 - 3             -> Simplify 3(1)
  = 4 - (7 - 4(1))    -> Substitute 3 with (7 - 4(1))
  = 4 - (7 - 4)       -> Simplify 4(1)
  = 4 - 7 + 4         -> Distribute
  = 2(4) - 7          -> Combine 4s
  = 2(60 - 7(8)) - 7  -> Substitute 4 with (60 - 7(8))
  = 2(60) - 16(7) - 7 -> Distribute
  = 2(60) - 17(7)     -> Done!
</pre>
To test the result, verify that 2(60) - 17(7) = 1 (it does). In this case, 60 and 7 represent our givens <code>a</code> and <code>b</code>, and <code>2</code> and <code>-17</code> our variables <code>x</code> and <code>y</code>, respectively. This means that the value of <code>y</code>, or -17, is the inverse of 7 in the group of integers modulo 60.

But we're not quite done yet. Since we are working modulo 60, we need to take -17 modulo 60. -17 mod 60 = 43, so 43 is the inverse of 7 in the group of integers modulo 60.

We can test this result by plugging it into the equation <code>ed mod 60 = 1</code>. Indeed, 7 x 43 mod 60 = 301 mod 60 = 1.