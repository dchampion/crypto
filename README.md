# Background
Cryptography is a word given to us by the ancient Greeks. Translated literally, it means *secret writing*. For centuries, cryptography was concerned with the encryption of messages into coded ciphers, in order to keep them secret from the prying eyes of adversaries. This is largely still the case. But, since the advent of the digital age, somewhere around the middle of the last century, cryptography has come to involve so much more.

Modern cryptography is a branch of *cryptology* (in Greek, the *study* of secrets), which concerns not only code&ndash;*making* (the stuff of cryptography) but also code&ndash;*breaking*. The code&ndash;breaking branch of cryptology is called *cryptanalysis*. One might be tempted to think cryptanalysis is the domain of spies and hackers, and only the *good guys* do cryptography.

This is only partially true. Cryptographers (code&ndash;makers) rely on cryptanalysts (code&ndash;breakers) to vet the quality of the ciphers they design; cryptanalysts do this by trying to break the ciphers. If the cryptanalysts can break the ciphers, then the cryptographers can go back to the drawing board and fix the ciphers before deploying them in sensitive applications. This is a good thing if you are one of the good guys.

Cryptography is itself subdivided into two main branches. These are *symmetric&ndash;key* cryptography and *public&ndash;key* (also known as *asymmetric&ndash;key*) cryptography. The former is what most people think of when they hear the words *cryptography*, *encryption* or *cipher*. Indeed, symmetric&ndash;key cryptography was (and still is) the standard for encryption for nearly four&ndash;thousand years, starting with heiroglyphs carved into cave walls by the ancient Egyptians.

Public&ndash;key cryptography is a much more recent invention. It emerged in light of inventions like the digital computer, and later the internet; technologies that demanded encryption at a scale much larger than traditional, symmetric ciphers could provide.

It is with the subject of public&ndash;key cryptography that the artifacts in this repository are concerned.

# What's in This Repository?
The repository is divided into two sections. One section (contained in the [doc](https://github.com/dchampion/crypto/tree/master/doc) folder) contains notes I've compiled, and documents I've written, about various topics concerning public&ndash;key cryptography. The other section (contained in the [code](https://github.com/dchampion/crypto/tree/master/code) folder) contains source&ndash;code implementations of many public&ndash;key concepts.