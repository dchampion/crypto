# Summary (and disclaimer)
The modules in this folder implement many of the public-key primitives one might expect to find in a cryptography library, such as key generation, encryption, decryption, digital signature and signature verification; they do not implement higher-level services (e.g. protocols, authentication) which, in addition to the primitives just mentioned, would be provided in a fully-featured cryptography library.

As such, while this library may be of academic interest to someone studying public-key cryptography, it should probably not be used to secure sensitive data in real applications.

# Documentation
The source code is well documented, both in <i>docstrings</i> at the module and function level, which describe at a high level the behavior of the module or function; and inline comments embedded in the function implementations, which are intended to clarify the effect of a particular statement or group of statements immediately following the comment.

The test code (in the <a href=https://github.com/dchampion/crypto/tree/master/test><code>/test</code></a> folder of this repository) is also documented. The most useful of this documentation is embedded in the full-protocol tests found in <a href=https://github.com/dchampion/crypto/blob/master/test/dh_test.py>dh_test.py</a> and <a href=https://github.com/dchampion/crypto/blob/master/test/rsa_test.py>rsa_test.py</a>. These walk the reader from start to finish through a simulated session, including a full parameter-setup and secure message-exchange.

# Unit Tests
To exercise all of the code in this library, clone this repository on your file system (or download and unzip it); then switch to the <code>/test</code> folder in your favorite operating system shell and type:
<p>
<code>
python run_all_tests.py
</code>
<p>
Alternatively, if <code>pytest</code> is installed, you can run the all the tests by typing:
<p>
<code>
pytest
</code>
</p>
Of course, Python (3.9.7+) must be installed on your computer to run this code.