# What's in This Repo?
This repository is divided into two sections. One of these, in the [doc](https://github.com/dchampion/crypto/tree/master/doc) folder, contains notes and documents on various topics concerning public&ndash;key cryptography. The other, in the [code](https://github.com/dchampion/crypto/tree/master/code) folder, contains programmatic expressions of these concepts implemented in the Python programming language.

# What is Cryptography?
Cryptography is a word given to us by the ancient Greeks. Translated literally, it means *secret writing*. For centuries, cryptography was concerned with the encryption of messages into coded ciphers, in order to keep them secret from the prying eyes of adversaries. This is largely still the case. But, since the advent of the digital age, somewhere around the middle of the last century, cryptography has come to involve much more than the encryption of messages.

Cryptography is a branch of *cryptology* (in Greek, the *study* of secrets), which concerns not only code&ndash;*making* (the stuff of cryptography) but also code&ndash;*breaking*. The code&ndash;breaking branch of cryptology is called *cryptanalysis*. One might be tempted to think cryptanalysis is the domain of spies and hackers, and only the *good guys* do cryptography.

This is only partially true. Cryptographers (code&ndash;makers) rely on cryptanalysts (code&ndash;breakers) to analyze the quality of their ciphers; cryptanalysts do this by trying to break the ciphers. If the cryptanalysts can break the ciphers, then the cryptographers must go back to the drawing board to fix the ciphers before deploying them in sensitive applications. This is a good thing if you are one of the good guys.

Cryptography is itself subdivided into two main branches. These are *symmetric&ndash;key* cryptography and *public&ndash;key* (also known as *asymmetric&ndash;key*) cryptography. The former is what most people think of when they hear the words *cryptography*, *encryption* or *cipher*. Indeed, symmetric&ndash;key cryptography was (and still is) the standard for encryption for nearly four&ndash;thousand years, starting with heiroglyphs carved into cave walls by the ancient Egyptians.

Public&ndash;key cryptography is a much more recent invention. It emerged with the advent of the digital computer, and later the internet; technologies that demanded encryption at a scale much larger than traditional, symmetric ciphers could provide.

It is with the subject of public&ndash;key cryptography that the artifacts in this repository are concerned.