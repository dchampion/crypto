# Summary and Disclaimer
The source code in this repository comprises two fully&ndash;featured public&ndash;key cryptosystems, and implements many public&ndash;key primitives one might expect to find in a cryptography library, such as key generation, encryption and digital signature. Implementations include the classic [*Diffie-Hellman*](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) (DH) key agreement protocol, the [*Rivest-Shamir-Adleman*](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) (RSA) cryptosystem, and an elliptic curve cryptosystem based on the Standards for Efficient Cryptography (SEC) Group's [*Recommended Curve Domain Parameters*](https://www.secg.org/sec2-v2.pdf).

With very few exceptions, this code is free of dependencies on external, third&ndash;party modules and libraries (modules such as `math` and `os` could not be avoided, but the services they provide are so essential that they could not  be feasibly omitted).
I did this for two reasons: *(1)* As a learning exercise (it is more effective to learn by writing functions than it is by calling them) and *(2)* as a security measure (one can never be too sure about code in external libraries&mdash;see [SolarWinds](https://www.wired.com/story/solarwinds-hack-supply-chain-threats-improvements/) and [Log4j](https://www.pcmag.com/how-to/what-is-the-log4j-exploit-and-what-can-you-do-to-stay-safe) for elaboration).

The source code in this folder should not be regarded as an API, but rather as a tool for learning, both for the author and the reader. As such, while it may be of academic interest to someone studying public&ndash;key cryptography, it should not be used to secure sensitive data in real applications.

# How to Run the Code
There are three principal ways to exercise the source code in this repository, with instructions for each to follow:

1. Run the unit tests (ok)

2. Run and interact with the code in a Python REPL (better)

3. Run and interact with the code in the Jupyter notebooks (best)

For any of these to work, Python (version 3.9.7 or greater) must be installed on your computer.

## 1. Unit Tests
For every source code module (e.g., *rsa.py*) in the [src](https://github.com/dchampion/crypto/tree/master/src) folder, there is a corresponding unit test (e.g., *rsa_test.py*) in the [tests](https://github.com/dchampion/crypto/tree/master/tests) folder.

To run a test on a single module (e.g., *rsa.py*), start a Python REPL in the root folder of this repository and type:

<pre>
>>> from tests import rsa_test
>>> rsa_test.main()
Running rsa tests...
...
all rsa tests passed
>>>
</pre>

Alternatively, to run *all* the tests in the [tests](https://github.com/dchampion/crypto/tree/master/tests) folder, type:

<pre>
>>> from tests import all_tests
>>> all_tests.main()
Running all tests...
...
all tests passed
>>>
</pre>

Or, if *pytest* is installed, you can achieve the same result by typing `pytest` from a command&ndash;line shell in the root folder of the repository (to install *pytest*, type `pip install pytest`).

## 2. Python REPL
For a better experience, start a Python REPL in the root folder of this repository to interact with the source code directly.

For example, in the following example, the elliptic curve cryptosystem is used to generate a keypair, sign a message with the private key, and then verify the signature with the public key:

<pre>
>>> from src import ec
>>> private_key, public_key = ec.generate_keypair()
>>> signature = ec.sign(private_key, "When in the course of human events...")
>>> ec.verify(public_key, "When in the course of human events...", signature)
True
>>> ec.verify(public_key, "When in the course of bovine events...", signature)
False
</pre>

## 3. Jupyter Notebooks
For the best experience, you can load and run Jupyter notebooks (files with *.ipynb* extensions located in the [doc](https://github.com/dchampion/crypto/tree/master/doc) folder of this repository). In addition to describing the various cryptographic protocols in detail, these notebooks allow the reader to interact with the source code in real time (to run a Jupyter server consult the link at [*jupyter.org*](https://jupyter.org/)).

# Documentation
The code is thoroughly documented, both in the form of *docstrings* at the module and function level, which describe at a high level the behavior of the module or function; and inline comments embedded in the function implementations, which are intended to clarify the effect of a particular statement or group of statements immediately following the comment.

The unit tests also contain documentation, the most descriptive of which is embedded in the full&ndash;protocol tests inside [*dh_test.py*](https://github.com/dchampion/crypto/blob/master/tests/dh_test.py), [*rsa_test.py*](https://github.com/dchampion/crypto/blob/master/tests/rsa_test.py) and [*ec_test.py*](https://github.com/dchampion/crypto/blob/master/tests/ec_test.py), which exercise the highest&ndash;level primitives in this library. These tests simulate sessions from start to finish; from parameter&ndash;setup and key&ndash;negotiation to secure, authenticated message&ndash;exchange between parties over insecure channels.

# Why Python?
Python has a built&ndash;in multiprecision library featuring large-integer support; a prerequisite for industrial&ndash;strength computational cryptography. Using a language such as C, C++ or Java, would have required the services of a third&ndash;party, external library, which I tried to avoid for the reason stated above.

# Description of Source Files
[curves.py](https://github.com/dchampion/crypto/blob/master/src/curves.py) &mdash; The collection of elliptic curves specified in the Standards for Efficient Cryptography Group's (SECG) [*Recommended Elliptic Curve Domain Parameters*](https://www.secg.org/sec2-v2.pdf).

[dh.py](https://github.com/dchampion/crypto/blob/master/src/dh.py) &mdash; An implementation of the classic, multiplicative-group based Diffie-Hellman (DH) key agreement protocol.

[ec.py](https://github.com/dchampion/crypto/blob/master/src/ec.py) &mdash; Implementations of the elliptic curve Diffie-Hellman (ECDH) and elliptic curve digital signature algorithms (ECDSA).

[euclid.py](https://github.com/dchampion/crypto/blob/master/src/euclid.py) &mdash; Efficient algorithms for computing the greatest common divisors (GCD), least common multiples (LCM) and modular multiplicative inverses of positive integers.

[primes.py](https://github.com/dchampion/crypto/blob/master/src/primes.py) &mdash; Efficient algorithms for primality testing and prime number generation.

[prng.py](https://github.com/dchampion/crypto/blob/master/src/prng.py) &mdash; A cryptographically secure pseudo-random number generator.

[rsa.py](https://github.com/dchampion/crypto/blob/master/src/rsa.py) &mdash; Implementations of the Rivest-Shamir-Adleman (RSA) cryptosystem, including encryption, decryption, digital signature and verification procedures.

[util.py](https://github.com/dchampion/crypto/blob/master/src/util.py) &mdash; Efficient algorithms for exponentiation of bases to powers of very large exponents.