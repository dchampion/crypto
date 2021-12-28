# Disclaimer
The modules in this folder implement many of the public-key primitives one might expect to find in a cryptography library, such as key generation, encryption, decryption, digital signature and signature verification; they do not implement protocol-layer (or any other higher-level) services which, in addition to the primitives just mentioned, would be provided in a fully-featured cryptography library.

Further, although the author believes the features of this library to provide security equal to that of reputable, industrial-strength implementations, he makes no warranties to that effect.

As such, while this library may be of academic interest to someone studying public-key cryptography, it should probably not be used to secure sensitive data in real applications.

# Unit Tests
To exercise all of the code in this library, switch to the test folder in your favorite operating system shell and type:
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