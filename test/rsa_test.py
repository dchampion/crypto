import path_resolver
import rsa
import primes
import euclid
import sym

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
        n = rsa._generate_rsa_prime(rsa._factor_min_bit_len)
        assert primes.is_prime(n), "n is not prime"
        assert n.bit_length() == rsa._factor_min_bit_len,\
            f"expected bit length {rsa._factor_min_bit_len}, got {n.bit_length()}"
        assert n % rsa.VERIFICATION_EXPONENT != 1, "n-1 must not be a multiple of 3"
        assert n % rsa.ENCRYPTION_EXPONENT != 1, "n-1 must not be a multiple of 5"

    print(f"test_generate_rsa_prime passed 10 tests returning {rsa._factor_min_bit_len}-bit primes")

def test_generate_rsa_key():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa._modulus_min_bit_len)
        t = euclid.lcm(p-1, q-1)
        assert primes.is_prime(p), "p is not prime"
        assert primes.is_prime(q), "q is not prime"
        assert n == p*q, "n != p*q"
        assert euclid.inverse(d3, t) == rsa.VERIFICATION_EXPONENT,\
            f"expected inverse of {d3} and {t} is {rsa.VERIFICATION_EXPONENT}, got {euclid.inverse(d3, t)}"
        assert euclid.inverse(d5, t) == rsa.ENCRYPTION_EXPONENT,\
            f"expected inverse of {d5} and {t} is {rsa.ENCRYPTION_EXPONENT}, got {euclid.inverse(d5, t)}"

    print(f"test_generate_rsa_key passed 10 tests using {rsa._modulus_min_bit_len}-bit moduli")

def test_encrypt_decrypt():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa._modulus_min_bit_len)
        K1, c = rsa.encrypt_random_key(n, rsa.ENCRYPTION_EXPONENT)
        K2 = rsa.decrypt_random_key(d5, c, p, q)
        assert K1 == K2, "Keys don't match"

    print(f"test_encrypt_decrypt passed 10 tests using {rsa._modulus_min_bit_len}-bit moduli")

def test_sign_verify():
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa._modulus_min_bit_len)
        o = rsa.sign(d3, p, q, m)
        assert True == rsa.verify(n, rsa.VERIFICATION_EXPONENT, m, o)

    print(f"test_sign_verify passed multiple tests using {rsa._modulus_min_bit_len}-bit moduli")

def test_full_protocol():
    ########################################################################################
    # The following diagram illustrates the protocol simulated in this test graphically.   #
    # Values surrounded in square brackets [] are public (i.e., they can be transmitted    #
    # over an insecure channel with no compromise to the integrity of the system if they   #
    # are intercepted by an adversary), and those that are not private (i.e., they must be #
    # kept secret). The direction arrows ---> and <--- indicate an exchange of information #
    # between Alice and Bob on an insecure channel.                                        #
    #                                                                                      #
    # Alice                                       Bob                                      #
    # ----------------------------                ----------------------------             #
    # pA, qA, [nA], d3A, d5A =                    pB, qB, [nB], d3B, d5B =                 #
    #   generate_rsa_key(modulus_bit_length)         generate_rsa_key(modulus_bit_length)  #
    #                                                                                      #
    # [nA]                                --->    [nA] (v=3 and e=5 are known.)            #
    #                                                                                      #
    # [nB] (v=3 and e=5 are known.)       <---    [nB]                                     #
    #                                                                                      #
    # mA = "8675309" (Message to be                                                        #
    #         signed and encrypted.)                                                       #
    #                                                                                      #
    # [oA] =                                                                               #
    #   rsa_sign(d3A, pA, qA, mA)                                                          #
    #                                                                                      #
    # KA, [cA] =                                                                           #
    #   rsa_encrypt_key([nB], [e=5])                                                       #
    #                                                                                      #
    # [mAC] = sym_encrypt_message(KA, mA)                                                  #
    #                                                                                      #
    # [oA, mAC, cA]                       --->      [oA, mAC, cA] (Bob receives message    #
    #                                                        signature, encrypted message, #
    #                                                        and encrypted key material    #
    #                                                        from Alice.)                  #
    #                                                                                      #
    #                                               KB                                     #
    #                                                 = rsa_decrypt_key(d5B, [cA], pB, qB) #
    #                                                                                      #
    #                                               mB = sym_decrypt_message(KB, [mAC])    #
    #                                                                                      #
    #                                               result                                 #
    #                                                 = rsa_verify([nA], [v=3], mB, [oA])  #
    #                                                                                      #
    # If, in the very last step, the result of the rsa_verify() operation performed by Bob #
    # returns True, Bob can be sure the message mB he decrypts and verifies was signed by  #
    # Alice's private key; and is therefore identical to the message mA that Alice signed  #
    # and encrypted.                                                                       #
    ########################################################################################

    # Alice generates her RSA parameters, and sends the public component (the modulus [nA])
    # to Bob. In this simulated protocol, we assume that Bob knows Alice's signature-
    # verification and encryption exponents (the numbers 3 and 5, respectively); these,
    # together with [nA], comprise Alice's public key.
    pA, qA, nA, d3A, d5A = rsa.generate_rsa_key(rsa._modulus_min_bit_len)

    # Bob generates his own RSA parameters, and sends the public component (the modulus
    # [nB]) to Alice. Alice, too, knows Bob's public signature-verification and encryption
    # exponents (again, v=3 and e=5).
    pB, qB, nB, d3B, d5B = rsa.generate_rsa_key(rsa._modulus_min_bit_len)

    # Alice produces a message mA, and signs it using her private signing key d3A. The
    # resulting signature is stored in [oA]. Note that, although it is unclear from this
    # interface, the message mA is not signed directly; rather, it is hashed first, to the
    # full domain of the modulus nA, and then signed.
    mA = "8675309"
    oA = rsa.sign(d3A, pA, qA, mA)

    # Alice computes and encrypts a symmetric key, using Bob's public key [nB, 5], and
    # stores it in KA; this she must keep private. [cA] is the ciphertext of the symmetric
    # key input material, which Alice will transmit to Bob, and which Bob will use to
    # reconstruct the symmetric key KA.
    KA, cA = rsa.encrypt_random_key(nB, rsa.ENCRYPTION_EXPONENT)

    # Using the symmetric key KA, Alice encrypts the message mA using a symmetric
    # scheme. For the purposes of this example, that scheme is a simple bitwise xor of
    # the symmetric key KA with an integer representation of the message mA. In a real-
    # world application, the symmetric scheme should be an industry standard (e.g., AES).
    mAC = sym.encrypt(KA, mA)

    # From the ciphertext [cA], Bob decrypts Alice's symmetric key KA using his
    # private RSA decryption key (d5B, pB, qB). He stores the result in KB (KB
    # should be identical to KA).
    KB = rsa.decrypt_random_key(d5B, cA, pB, qB)
    assert KA == KB

    # Bob decrypts Alice's ciphertext message [mAC] using the same symmetric scheme
    # (bitwise xor of KB and mAC) Alice used to encrypt the message. He stores the
    # result in mB (mB should be identical to mA). Bob can be confident the message
    # Alice sent to him can only be read by him, and not by an eavesdropper who may
    # have intercepted it.
    mB = sym.decrypt(KB, mAC)
    assert mA == mB

    # Bob verifies Alice's signature [oA] of the original message mA (or, more
    # precisely, his version of the message mB). This verification guarantees both
    # the message's authenticity (it was signed with Alice's private key) and
    # integrity (it was not altered, or otherwise corrupted, in any way after it
    # was signed by Alice). We have thus acheived the three key characteristics
    # required for a public-key scheme: confidentiality (via encryption),
    # authenticity and integrity (via signature and verification).
    verified = rsa.verify(nA, rsa.VERIFICATION_EXPONENT, mB, oA)
    assert verified == True

    print("full protocol test passed")

if __name__ == "__main__":
    main()