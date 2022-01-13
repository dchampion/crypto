# Summary
The modules in this package comprise a fully-featured public-key cryptosystem, including protocols for symmetric key agreement, encryption, decryption, digital signature and signature verification.

To see examples of their usage, consult the unit tests in the [/test](https://github.com/dchampion/crypto/tree/master/code/test) folder of this repository; or, to run interactive sessions of them on a [*Jupyter*](https://jupyter.org/) server, load and run the files with .ipynb extensions in the [/doc](https://github.com/dchampion/crypto/tree/master/doc) folder.

# List of Modules

1. **dh.py** &mdash; An implementation of the Diffie-Hellman key agreement protocol.

2. **euclid.py** &mdash; Algorithms for computing the greatest common divisor (GCD), least common multiple (LCM) and modular multiplicative inverses of positive integers.

3. **primes.py** &mdash; Algorithms for primality testing and random prime number generation.

4. **rsa.py** &mdash; Implementations of the Rivest-Shamir-Adleman encryption/decryption and digital signature/verification protocols.

5. **util.py** &mdash; Algorithms for efficient exponentiation of bases to very large exponents.