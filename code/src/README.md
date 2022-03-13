# Summary
The modules in this package comprise two fully-featured public-key cryptosystems, including protocols for symmetric key agreement, encryption, decryption, digital signature and signature verification.

Implementations include the [*Diffie-Hellman*](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) (DH) key agreement protocol, the [*Rivest-Shamir-Adleman*](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) (RSA) cryptosystem, and a cryptosystem based on the Standards for Efficient Cryptography (SEC) Group's [*secp256k1*](https://www.secg.org/sec2-v2.pdf#subsubsection.2.4.1) elliptic curve.

To see examples of their usage, consult the unit tests in the [/test](https://github.com/dchampion/crypto/tree/master/code/test) folder of this repository; or, to run interactive sessions of them on a [*Jupyter*](https://jupyter.org/) server, load and run the files with .ipynb extensions in the [/doc](https://github.com/dchampion/crypto/tree/master/doc) folder.

# List of Modules

1. [dh.py](https://github.com/dchampion/crypto/blob/master/code/src/dh.py) &mdash; An implementation of the Diffie-Hellman (DH) key agreement protocol.

2. [ec.py](https://github.com/dchampion/crypto/blob/master/code/src/ec.py) &mdash; Implementations of the elliptic curve Diffie-Hellman (ECDH) and elliptic curve digital signture algorithms (ECDSA).

3. [euclid.py](https://github.com/dchampion/crypto/blob/master/code/src/euclid.py) &mdash; Efficient algorithms for computing the greatest common divisors (GCD), least common multiples (LCM) and modular multiplicative inverses of positive integers.

4. [primes.py](https://github.com/dchampion/crypto/blob/master/code/src/primes.py) &mdash; Efficient algorithms for primality testing, and random prime number generation.

5. [prng.py](https://github.com/dchampion/crypto/blob/master/code/src/prng.py) &mdash; A cryptographically secure pseudo-random number generator.

6. [rsa.py](https://github.com/dchampion/crypto/blob/master/code/src/rsa.py) &mdash; Implementations of the Rivest-Shamir-Adleman (RSA) cryptosystem, including encryption, decryption, digital signature and verification procedures.

7. [util.py](https://github.com/dchampion/crypto/blob/master/code/src/util.py) &mdash; Efficient algorithms for exponentiation of bases to powers of very large exponents.