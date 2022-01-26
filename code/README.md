# Summary
The modules in this package implement many of the public&ndash;key primitives one might expect to find in a cryptography library, such as key generation, encryption, decryption, digital signature and signature verification; they do not implement higher&ndash;level services (e.g. interoperability protocols, third&ndash;party authentication) which, in addition to the primitives just mentioned, would be provided in a fully&ndash;featured cryptography library.

As such, while the code in this library may be of academic interest to someone studying public&ndash;key cryptography, it should not be used to secure sensitive data in real applications.

## Source Code
Source code, which is located in the [/src](https://github.com/dchampion/crypto/tree/master/code/src) folder of this repository, is well documented, both in *docstrings* at the module and function level, which describe at a high level the behavior of the module or function; and inline comments embedded in the function implementations, which are intended to clarify the effect of a particular statement or group of statements immediately following the comment.

With very few exceptions, the source code is free of dependencies on external, third&ndash;party modules and libraries (modules such as `math` and `os` could not be avoided, but the services they provide are so essential that they could not  be feasibly omitted).

I did this for two reasons: *1)* As a learning excercise (it is more effective to learn by writing functions than it is by calling them) and *2)* as a security measure (one can never be too sure about code in external libraries&mdash;see [SolarWinds](https://www.wired.com/story/solarwinds-hack-supply-chain-threats-improvements/) and [Log4j](https://www.pcmag.com/how-to/what-is-the-log4j-exploit-and-what-can-you-do-to-stay-safe) for elaboration).

## Test Code
For every source code module `x.py` in the [/src](https://github.com/dchampion/crypto/tree/master/code/src) folder, there is a corresponding unit test `test_x.py` in the [/test](https://github.com/dchampion/crypto/tree/master/code/test) folder.

The code in these tests also contains documentation, the most useful of which is embedded in the full&ndash;protocol tests inside [*dh_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/dh_test.py), [*rsa_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/rsa_test.py) and [*ec_test.py*](https://github.com/dchampion/crypto/blob/master/code/test/ec_test.py), which exercise the highest&ndash;level primitives in this library. These tests simulate sessions from start to finish; from parameter&ndash;setup and key&ndash;negotiation to secure, authenticated message&ndash;exchange between parties over insecure channels.

## Documentation
Finally, the [*Jupyter*](https://jupyter.org/) notebooks located in the [/doc](https://github.com/dchampion/crypto/tree/master/doc) folder (files with *.ipynb* extensions), go even further, inviting the reader to interact in real time with these cryptosystems.