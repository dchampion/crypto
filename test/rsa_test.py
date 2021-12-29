import sys
sys.path.append("../src")

import rsa
import primes
import euclid

def main():
    print("Running rsa tests...")
    test_generate_rsa_prime()
    test_generate_rsa_key()
    test_encrypt_decrypt()
    test_sign_verify()
    test_full_protocol()
    print("all rsa tests passed")

def test_generate_rsa_prime():
    for _ in range(10):
        n = rsa.generate_rsa_prime(rsa.factor_min_bit_len)
        assert primes.is_prime(n), "n is not prime"
        assert n.bit_length() == rsa.factor_min_bit_len,\
            f"expected bit length {rsa.factor_min_bit_len}, got {n.bit_length()}"
        assert n % 3 != 1, "n-1 must not be a multiple of 3"
        assert n % 5 != 1, "n-1 must not be a multiple of 5"

    print(f"test_generate_rsa_prime passed 10 tests returning {rsa.factor_min_bit_len}-bit primes")

def test_generate_rsa_key():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        t = euclid.lcm(p-1, q-1)
        assert primes.is_prime(p), "p is not prime"
        assert primes.is_prime(q), "q is not prime"
        assert n == p*q, "n != p*q"
        assert euclid.inverse(d3, t) == 3,\
            f"expected inverse of {d3} and {t} is 3, got {euclid.inverse(d3, t)}"
        assert euclid.inverse(d5, t) == 5,\
            f"expected inverse of {d5} and {t} is 5, got {euclid.inverse(d5, t)}"

    print(f"test_generate_rsa_key passed 10 tests using {rsa.modulus_min_bit_len}-bit moduli")

def test_encrypt_decrypt():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        K1, c = rsa.encrypt_random_key(n, 5)
        K2 = rsa.decrypt_random_key(d5, c, p, q)
        assert K1 == K2, "Keys don't match"

    print(f"test_encrypt_decrypt passed 10 tests using {rsa.modulus_min_bit_len}-bit moduli")

def test_sign_verify():
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        o = rsa.sign(n, d3, p, q, m)
        assert True == rsa.verify(n, 3, m, o)

    print(f"test_sign_verify passed multiple tests using {rsa.modulus_min_bit_len}-bit moduli")

def test_full_protocol():
    # Alice generates her RSA parameters, and sends the public component (the modulus nA)
    # to Bob. In this simulated protocol, we assume that Bob knows Alice's encryption
    # and signature-verification components--the exponents 3 and 5--respectively, because
    # they are part of Alice's public key.
    pA, qA, nA, d3A, d5A = rsa.generate_rsa_key(rsa.modulus_min_bit_len)

    # Bob generates his own RSA parameters, and sends the public component (the modulus nB)
    # to Alice. Alice, too, knows Bob's public encryption and signature-verification components
    # (also 3 and 5).
    pB, qB, nB, d3B, d5B = rsa.generate_rsa_key(rsa.modulus_min_bit_len)

    # Alice produces a message [mA], and signs it using her private signing key [d3A].
    # The resulting signature is stored in oA.
    mA = "8675309"
    oA = rsa.sign(nA, d3A, pA, qA, mA)

    # Alice computes and encrypts a symmetric key, using Bob's public key [nB, 5], and
    # stores it in KA; this she must keep private. cA is the ciphertext of the symmetric
    # key input material, which Alice will transmit to Bob, and which Bob will use to
    # reconstruct the symmetric key [KA].
    KA, cA = rsa.encrypt_random_key(nB, 5)

    # Using the symmetric key [KA], Alice encrypts the message [mA] using a symmetric
    # scheme. For the purposes of this example, that scheme is a bitwise xor of the
    # symmetric key [KA] with an integer representation of the message [mA].
    mAC = sym_encrypt(KA, mA)

    ################################################################################
    # Alice transmits to Bob everything he will need to decrypt, verify and read   #
    # her message. She does this without revealing any information about the       #
    # contents of the message, nor how to decrypt or verify it, to a passive       #
    # eavesdropper.                                                                #
    #                                                                              #
    # Alice transmits to to Bob (1) the signature of the message [oA], (2) the     #
    # ciphertext of the message [mAC] (which was encrypted using the symmetric     #
    # key [KA]), and (3) the ciphertext of the key input material [cA] (which      #
    # was encrypted using Bob's RSA public key [nB, 5]).                           #
    ################################################################################

    # From the ciphertext [cA], Bob decrypts Alice's symmetric key [KA] using his
    # private RSA decryption key [d5B, pB, qB]. He stores the result in KB (KB
    # should be identical to KA).
    KB = rsa.decrypt_random_key(d5B, cA, pB, qB)
    assert KA == KB

    # Bob decrypts Alice's ciphertext message [mAC] using the same symmetric scheme
    # (bitwise xor of KB and mAC) Alice used to encrypt the message. He stores the
    # result in mB (mB should be identical to mA). Bob can be confident the message
    # Alice sent to him can only be read by him, and not by an eavesdropper who may
    # have intercepted it.
    mB = sym_decrypt(KB, mAC)
    assert mA == str(mB)

    # Bob verifies Alice's signature [oA] of the original message [mA] (or, more
    # precisely, his version of it, which he has decrypted and stored in mB).
    # This verification guarantees both the message's authenticity (it was signed
    # with Alice's private key) and integrity (it was not altered, or otherwise
    # corrupted, in any way after it was signed by Alice). We have thus acheived
    # the three key characteristics required for a public-key scheme: confidentiality
    # (via encryption), authenticity and integrity (via signature and verification).
    verified = rsa.verify(nA, 3, mB, oA)
    assert verified == True

    print("full protocol test passed")

def sym_encrypt(key, msg):
    # Poor man's symmetric cipher.
    return int.from_bytes(key, byteorder="little") ^ int(msg)

def sym_decrypt(key, msg):
    return sym_encrypt(key, msg)

if __name__ == "__main__":
    main()