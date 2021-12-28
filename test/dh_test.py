import sys
sys.path.append("../src")

import dh

def main():
    print("Running dh tests...")
    test_dh_setup()
    test_setup_encrypt_decrypt()
    print("dh tests passed")
    
def test_dh_setup():
    p, q, g = dh.generate_parameters(2048)
    dh.validate_parameters(p, q, g)
    
    kPriv1, kPub1 = dh.generate_keypair(g, q, p)
    dh.validate_pub_key(kPub1, q, p)

    kPriv2, kPub2 = dh.generate_keypair(g, q, p)
    dh.validate_pub_key(kPub2, q, p)

    kSession1 = dh.generate_session_key(kPub2, kPriv1, p)
    kSession2 = dh.generate_session_key(kPub1, kPriv2, p)
    assert kSession1 == kSession2, "Secrets don't match"

    print("dh setup passed")

def test_setup_encrypt_decrypt():
    # Alice generates the public parameters for a DH session with Bob; these are the public
    # (and prime) modulus [p], the size of the subgroup modulo p within which generated
    # values will fall [q], and the generator of the subgroup [g].
    p, q, g = dh.generate_parameters(dh.min_p_bit_len)

    # Alice must validate these parameters before transmitting them to Bob; Bob will run
    # the same validation of these values when he receives them from Alice.
    dh.validate_parameters(p, q, g)

    # Alice generates her private and public keys [kA, KA], using g, q and p as inputs.
    kA, KA = dh.generate_keypair(g, q, p)
    # Alice validates her public key [KA].
    dh.validate_pub_key(KA, q, p)

    ####################################################################################
    # Alice, having generated the public parameters p, q and g, and her public key KA, #
    # transmits all of these to Bob.                                                   #
    ####################################################################################

    # Bob repeats the same validation on the public parameters that Alice did before
    # transmitting them to him.
    dh.validate_parameters(p, q, g)

    # Bob generates his private and public keys [kB, KB], using as inputs the same g, q
    # and p that Alice used.
    kB, KB = dh.generate_keypair(g, p, p)
    # Bob validates his public key [KB].
    dh.validate_pub_key(KB, q, p)

    ####################################################################################
    # Bob transmits his public key [KB] to Alice.                                      #
    ####################################################################################

    # Alice, having received Bob's public key [KB], uses it, along with her private key
    # [kA] to generate her session key; this must be kept secret (i.e., it must not be
    # transmitted to Bob, or otherwise revealed).
    kSessionA = dh.generate_session_key(KB, kA, p)

    # Bob, having received Alice's public key [KA], uses it, along with his private key
    # [kB] to generate his session key; this too must be kept secret. The session keys
    # [kSessionA, kSessionB] that Alice and Bob compute must be equal.
    kSessionB = dh.generate_session_key(KA, kB, p)
    assert kSessionA == kSessionB

    # Alice produces a message [mA], encrypts it using her session key [kSessionA], and
    # transmits the ciphertext [mAC] to Bob.
    mA = "8675309"
    mAC = sym_encrypt(kSessionA, mA)

    # Bob receives the ciphertext [mAC], and decrypts it using his session key [kSessionB].
    # The message Bob decrypts [mB] must equal the message Alice encrypted [mA].
    mB = sym_decrypt(kSessionB, mAC)
    assert mA == str(mB)

    print("full protocol (setup-encrypt-decrypt) passed")

def sym_encrypt(key, msg):
    return int.from_bytes(key, byteorder="little") ^ int(msg)

def sym_decrypt(key, msg):
    return sym_encrypt(key, msg)

if __name__ == "__main__":
    main()