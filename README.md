# What's in This Repo?

This repository is divided into two sections. One of these, in the [doc](https://github.com/dchampion/crypto/tree/master/doc) folder, contains simple, comprehensible treatments of important topics in modern cryptography. The other, in the [src](https://github.com/dchampion/crypto/tree/master/src) folder, contains programmatic expressions of these concepts in the Python programming language.

Readers are encouraged to consult the READMEs in these folders, which present roadmaps to their contents.

# What is Cryptography?

The word _cryptography_ comes from the ancient Greeks. Translated literally, it means _secret writing_. For centuries, cryptography was concerned with the encryption of messages into coded ciphers, in order to keep them secret from the prying eyes (or ears) of adversaries. This is largely still the case. But, since the advent of the digital age, somewhere around the middle of the last century, cryptography began to emerge from the shadowy domains of governments and spies to provide privacy protections to anyone on the planet who uses a computer, smartphone or Internet&ndash;connected device.

Cryptography is a branch of _cryptology_ (in Greek, the _study_ of secrets), which concerns not only code&ndash;_making_ (the stuff of cryptography) but also code&ndash;_breaking_. The code&ndash;breaking branch of cryptology is called _cryptanalysis_. One might be tempted to think cryptanalysis is the domain of spies and hackers, and only the _good guys_ do cryptography.

This is only partially true. Cryptographers (code&ndash;makers) rely on cryptanalysts (code&ndash;breakers) to analyze the quality of the ciphers they invent; they do this by trying to break the cryptographers' ciphers. If the cryptanalysts can break the ciphers, then the cryptographers must go back to the drawing board to fix them before they are deployed in sensitive applications. This is a good thing if you are one of the good guys.

Cryptography is itself subdivided into two main branches. These are _symmetric&ndash;key_ cryptography and _public&ndash;key_ (also known as _asymmetric&ndash;key_) cryptography. The former is what most people think of when they hear the words _cryptography_, _encryption_ or _cipher_. Indeed, symmetric&ndash;key cryptography was (and still is) the standard for encryption for nearly four&ndash;thousand years, starting with hieroglyphs carved into cave walls by the ancient Egyptians.

Public&ndash;key cryptography is a much more recent&mdash;and arguably more interesting&mdash;invention. It emerged with the advent of the digital computer, and later the internet; technologies that demand encryption at a scale much greater than traditional, symmetric ciphers can provide.

It is with the subject of public&ndash;key cryptography that the artifacts in this repository are concerned.
