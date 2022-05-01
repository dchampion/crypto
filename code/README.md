# What This *Is*
The source code in this repository comprises two fully&ndash;featured public&ndash;key cryptosystems, and implements many public&ndash;key primitives one might expect to find in a cryptography library, such as key generation, encryption, decryption, digital signature and signature verification. Implementations include the [*Diffie-Hellman*](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) (DH) key agreement protocol, the [*Rivest-Shamir-Adleman*](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) (RSA) cryptosystem, and an elliptic curve cryptosystem based on the Standards for Efficient Cryptography (SEC) Group's [*secp256k1*](https://www.secg.org/sec2-v2.pdf#subsubsection.2.4.1) specification.

With very few exceptions, the code is free of dependencies on external, third&ndash;party modules and libraries (modules such as `math` and `os` could not be avoided, but the services they provide are so essential that they could not  be feasibly omitted).
I did this for two reasons: **(1)** As a learning excercise (it is more effective to learn by writing functions than it is by calling them) and **(2)** as a security measure (one can never be too sure about code in external libraries&mdash;see [SolarWinds](https://www.wired.com/story/solarwinds-hack-supply-chain-threats-improvements/) and [Log4j](https://www.pcmag.com/how-to/what-is-the-log4j-exploit-and-what-can-you-do-to-stay-safe) for elaboration).

# What This *Is Not*
The code in this repository is not intended to be an API, and was therefore not architected with that goal in mind. For example, it exposes low&ndash;level primitives (i.e., functions) that would otherwise be hidden to clients of a cryptography API.

This code should instead be regarded as a tool for learning, both for the programmer and the reader. As such, while it may be of academic interest to someone studying public&ndash;key cryptography, it should not be used to secure sensitive data in real applications.

# Unit Tests
To exercise the code in this repository, run the unit tests in the [test](https://github.com/dchampion/crypto/tree/master/code/test) folder of this repository. For every source code module `x.py` in the [src](https://github.com/dchampion/crypto/tree/master/code/src) folder, there is a corresponding unit test `test_x.py` in the [test](https://github.com/dchampion/crypto/tree/master/code/test) folder.

From your favorite operating system shell (e.g. `CMD` on Windows, `bash` on Linux or `zsh` on Mac), navigate to the root directory of the repository and type:

`python code/test/run_all_tests.py`

Alternatively, if `pytest` is installed, you can run the all the tests by typing `pytest` from the root directory of the repository (to install `pytest`, type `pip install pytest`).

Python (version 3.9.7 or greater) must be installed on your computer to execute the code in this repository.

# Documentation
The code is amply documented, both in the form of *docstrings* at the module and function level, which describe at a high level the behavior of the module or function; and inline comments embedded in the function implementations, which are intended to clarify the effect of a particular statement or group of statements immediately following the comment.

The unit tests also contain documentation, the most descriptive of which is embedded in the full&ndash;protocol tests inside [*dh_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/dh_test.py), [*rsa_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/rsa_test.py) and [*ec_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/ec_test.py), which exercise the highest&ndash;level primitives in this library. These tests simulate sessions from start to finish; from parameter&ndash;setup and key&ndash;negotiation to secure, authenticated message&ndash;exchange between parties over insecure channels.

For the best experience, the reader can load and run Jupyter notebooks (files with `.ipynb` extensions located in the [doc](https://github.com/dchampion/crypto/tree/master/doc) folder of this repository). In addition to describing the various cryptographic protocols in detail, these notebooks allow the reader to interact with the source code in real time (to run a Jupyter server consult the link at [*jupyter.org*](https://jupyter.org/)).

# Why Python?
Python has a built&ndash;in multiprecision libraray featuring large-integer support; a prerequisite for industrial&ndash;strength computational cryptography. Using a language such as C, C++ or Java, would have required the services of a third&ndash;party, external library, which I tried to avoid for the reason stated above.