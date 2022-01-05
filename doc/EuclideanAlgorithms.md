# Euclidean Algorithms
## Using the Euclidean Algorithm to Find the Greatest Common Divisor (<i>GCD</i>) of Two Natural Numbers

<i>For implementations of these algorithms in the Python programming language, see <a href=https://github.com/dchampion/crypto/blob/master/code/src/euclid.py>here</a>.</i>

In the procedure for RSA encryption described in <a href=https://raw.githubusercontent.com/dchampion/crypto/master/doc/TheElementsOfPublicKeyCryptography.pdf><i>The Elements of Public Key Cryptography</i></a>, step 5 requires Alice to compute an encryption exponent <i>e</i>.

Recall that the requirement for <i>e</i> is that it be a positive integer that is relatively prime to the totient of <i>n</i>, or <i>&phi;(n)</i>. Recall that <i>n</i> is the product of the two primes <i>p</i> and <i>q</i>, which in the example are 7 and 11, respectively, thus giving us <i>n</i>=77. And recall that <i>&phi;</i>(77)=60 (because there are 60 integers in the range 1 to 77 that are relatively prime to 77). Another way of saying this is that there are 60 integers in the range 1 to 77 whose <i>greatest common divisor</i> (<i>GCD</i>) with 77 is 1.

The Euclidean Algorithm gives us an efficient method for finding the GCD of two integers, which is especially useful for real-world, cryptographically strong (i.e. very large) numbers. We'll demonstrate it here, using the small numbers from the example, to compute a suitable encryption exponent <i>e</i>.

In the present case we must identify a value in the range 1 to 60 whose GCD with 60 is 1, expressed formulaically as <i>GCD(60,e)=1</i>. We must use such a value for <i>e</i> because it will have an inverse in the group of integers modulo 60 (values with GCDs greater than 1 will not have an inverse), and we need an inverse in order to decrypt messages.

We find the GCD of two integers by taking the larger integer modulo the smaller, recursively, until we reach 0. For example, let's randomly select the value 8 as a candidate for <i>e</i>. To find the GCD of 60 and 8, we do the following:
<pre>
GCD(60,8) = GCD(60 mod 8,8) -> 60 mod 8 = 4
          = GCD(4,8)        -> Result of previous operation
          = GCD(8,4)        -> Swap parameters
          = GCD(8 mod 4,4)  -> 8 mod 4 = 0
          = GCD(0,4)        -> Result of previous operation
          = 4               -> Stop when parameter reaches 0; remaining non-zero parameter is GCD
</pre>
When 0 is reached, the remaining non-zero parameter&mdash;4 in this case&mdash;is the GCD.

Of course, with small parameters, like 60 and 8, we can skip the ceremony and work out in our heads that 4 is the largest number that divides both. But for very large numbers we need the help of the Euclidean Algorithm. Because GCD(60,8) is greater than 1, 8 is not suitable for use as an encryption exponent.

Let's try again, this time with 7:
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
          = 1               -> Stop when parameter reaches 0; remaining non-zero parameter is GCD
</pre>
Here we have GCD(60,7)=1, because 1 is the largest remaining non-zero parameter when we reach 0. Since GCD(60,7)=1, Alice can use 7 as the encryption exponent <i>e</i> in her RSA parameter setup.

A second method of computing GCD&mdash;which will prove useful when we use an extended version the Euclidean Algorithm to find the inverse of <i>e</i>&mdash;is to express each step in terms of divisors, quotients and remainders.

To demonstrate, let's apply this second method to GCD(60,7):
<pre>
GCD(60,7) = 60 = 7(8) + 4 -> 60 is 7 (divisor) times 8 (quotient), plus 4 (remainder)
             7 = 4(1) + 3 -> Shift previous divisor and remainder left and repeat
             4 = 3(1) + 1 -> Shift previous divisor and remainder left and repeat
             3 = 3(1) + 0 -> Stop at 0
</pre>
The last non-zero remainder is 1, which is the GCD of 60 and 7.
## Using the <i>Extended</i> Euclidean Algorithm to Find the Inverse of the Encryption Exponent
Now that Alice has identified her encryption exponent <i>e</i>, she must next find a suitable decryption exponent <i>d</i>. This number must be the inverse of <i>e</i> (which is 7 in the present example) in the group of integers modulo <i>&phi;</i>(77). This exponent will be used by Alice to recover the plaintext from a message <i>M</i> encrypted with the procedure <i>M<sup>e</sup> mod n</i> (where <i>M</i> is a natural number in the range 1 to <i>n</i>-1, <i>e</i>=7 and <i>n</i>=77).

That is, we are looking for a decryption exponent <i>d</i>  that satisfies the equation <i>ed mod &phi;(n) = 1</i> or, plugging in the values we know so far, <i>7d mod 60 = 1</i>. Soving for <i>d</i> in this equation will tell us by what integer <i>e</i> must be multiplied to produce 1 mod <i>&phi;</i>(n).

To find the answer, we'll use the divisors, quotients and remainders version of the Euclidean Algorithm presented in the previous section, but with a small enhancement.

To preface a bit, we'll start with a short discussion of B&eacute;zout's identity, from which the enhanced method derives.

B&eacute;zout's identity asserts the following:
<pre>
ax + by = gcd(a,b)
</pre>
In English, B&eacute;zout's identity asserts that for any given natural numbers <i>a</i> and <i>b</i>, there are integer solutions <i>x</i> and <i>y</i> such that <code>ax + by = gcd(a,b)</code>. In the present example, since we know that <code>gcd(a,b)=1</code> (where <i>a</i>=60 and <i>b</i>=7), we can rewrite the identity as follows:
<pre>
ax + by = 1
</pre>
And since we are looking for the inverse of 7 in the group of integers modulo 60, we can substitute 60 for <i>a</i> and 7 for <i>b</i>, thus further fleshing out the identity as follows:
<pre>
60x + 7y = 1
</pre>
Specifically, we are interested in the value <i>y</i> that, when mulitplied by 7, and added to some multiple of 60 (i.e. 60<i>x</i>), results in 1 modulo 60. This value will be the inverse of 7 in the group of integers modulo 60 or, expressed algebraically, <code>7y = 1 (mod 60)</code>.

First, we repeat the divisors, quotients and remainders version of the Euclidean Algorithm demonstrated in the previous section to find GCD(60,7):
<pre>
GCD(60,7) = 60 = 7(8) + 4
             7 = 4(1) + 3
             4 = 3(1) + 1 -> Last non-zero remainder is GCD
             3 = 3(1) + 0 -> Stop at 0
</pre>
Next, we rewrite each line of the previous procedure (except the stop-line in which the remainder is 0), subtracting the divisor and quotient from both sides to isolate the remainder on the right-hand side of the equation:
<pre>
60 = 7(8) + 4 becomes 60 - 7(8) = 4
 7 = 4(1) + 3 becomes  7 - 4(1) = 3
 4 = 3(1) + 1 becomes  4 - 3(1) = 1
</pre>
Finally, starting from the bottom up, where the last remainder is 1, we use backward substitution to work our way to a solution for <code>ax + by = 1</code>.
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
To test the result, verify that 2(60) - 17(7) = 1 (it does). In this case, 60 and 7 represent our givens <i>a</i> and <i>b</i>, and 2 and -17 our variables <i>x</i> and <i>y</i>, respectively. This means that the value of <i>y</i>, or -17, is the inverse of 7 in the group of integers modulo 60.

But we're not quite done yet. Since we are working modulo 60, we need to take -17 modulo 60, and -17 mod 60 = 43. This means that 43 is the inverse of 7 in the group of integers modulo 60. We can test this result by plugging it into the equation <code>ed mod 60 = 1</code>. Indeed, 7 x 43 = 301; and 301 mod 60 = 1.

Therefore, 43 is the value Alice must use for her decryption exponent <i>d</i>, in order to successfully decrypt messages encrypted with her encryption exponent <i>e</i>.