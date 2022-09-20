import concurrent.futures
import os

from core import dh

from . import sym
from . import util


def main():
    print("Running dh tests...")
    test_dh_setup()
    test_full_protocol()
    print("all dh tests passed")


def test_dh_setup():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(
            dh_setup,
            util.get_random_bit_lengths(dh._P_MIN_BIT_LEN, dh._P_MAX_BIT_LEN // 2),
        )
        util.process_results(results)


def dh_setup(modulus_bit_len):
    print(f"testing dh setup with {modulus_bit_len}-bit modulus from pid={os.getpid()}")

    try:
        q, p, g = dh.generate_parameters(modulus_bit_len)
        dh.validate_parameters(q, p, g)

        k_prv_1, k_pub_1 = dh.generate_keypair(q, p, g)
        dh.validate_pub_key(k_pub_1, q, p)
        assert 1 <= k_prv_1 < q, "k_prv_1 is out of range"

        k_prv_2, k_pub_2 = dh.generate_keypair(q, p, g)
        dh.validate_pub_key(k_pub_2, q, p)
        assert 1 <= k_prv_2 < q, "k_prv_2 is out of range"
        assert k_prv_1 != k_prv_2, "k_prv_1 is equal to k_prv_2; bad PRNG?"

        k_sess_1 = dh.generate_session_key(k_pub_2, k_prv_1, q, p)
        k_sess_2 = dh.generate_session_key(k_pub_1, k_prv_2, q, p)
        assert k_sess_1 == k_sess_2, "Secrets don't match"

    except ValueError as ve:
        assert False, f"ValueError: {ve}"
    except Exception as e:
        assert False, f"Exception: {e}"

    print(f"dh setup passed with {modulus_bit_len}-bit modulus from pid={os.getpid()}")


def test_full_protocol():
    ##########################################################################################
    # The following diagram illustrates the protocol simulated in this test graphically.     #
    # Values surrounded in square brackets [] are public (i.e., they can be transmitted      #
    # over an insecure channel with no compromise to the integrity of the system if they     #
    # are intercepted by an adversary), and those that are not, private (i.e., they must     #
    # be kept secret). The direction arrows ---> and <--- indicate an exchange of            #
    # information between Alice and Bob on an insecure channel.                              #
    #                                                                                        #
    # Alice                                       Bob                                        #
    # ----------------------------                ----------------------------               #
    # [q, p, g] =                                                                            #
    #      generate_parameters(modulus_bit_length)                                           #
    #                                                                                        #
    # validate_parameters(q, p, g)                                                           #
    #                                                                                        #
    # kA, [KA] =                                                                             #
    #      generate_keypair(q, p, g)                                                         #
    #                                                                                        #
    # [p, q, g, KA]                     --->      [q, p, g, KA]                              #
    #                                             validate_parameters(q, p, g)               #
    #                                             validate_pub_key([KA], q, p)               #
    #                                                                                        #
    #                                             kB, [KB] =                                 #
    #                                                  generate_keypair(q, p, g)             #
    #                                                                                        #
    # [KB]                              <---      [KB]                                       #
    # validate_pub_key([KB], q, p)                                                           #
    #                                                                                        #
    # kSessionA =                                 kSessionB =                                #
    #      generate_session_key([KB], kA, q, p)         generate_session_key([KA], kB, q, p) #
    #                                                                                        #
    # [mAC] = sym_encrypt(kSessionA, mA)                                                     #
    #                                                                                        #
    # [mAC]                             --->      [mAC]                                      #
    #                                                                                        #
    #                                             mB = sym.decrypt(kSessionB, [mAC])         #
    #                                                                                        #
    # The message mB Bob decrypts must equal the message mA that Alice encrypted.            #
    ##########################################################################################

    print("testing full protocol")

    # Alice generates the public parameters for a DH session with Bob; these are the
    # public modulus [p] (a prime), the size of the subgroup modulo p within which
    # exchanged public keys must fall [q] (also a prime), and the generator of the
    # subgroup [g].
    q, p, g = dh.generate_parameters(dh._P_MIN_BIT_LEN)

    # Alice may optionally validate these parameters before transmitting them to Bob.
    # Bob, however, must validate them using the same funciton when he receives them
    # from Alice.
    dh.validate_parameters(q, p, g)

    # Alice generates her private and public keys kA and [KA], respectively, using
    # [g, q, p] as inputs. Alice transmits [q, p, g, KA] (but NOT her private key kA)
    # to Bob.
    kA, KA = dh.generate_keypair(q, p, g)

    # Bob MUST validate the public parameters [p, q, g] he receives from Alice.
    dh.validate_parameters(q, p, g)

    # Bob MUST ALSO validate Alice's public key [KA].
    dh.validate_pub_key(KA, q, p)

    # Bob generates his own private and public keys kB and [KB], using as inputs the
    # public parameters [p, q, g] (now validated) he received from Alice. Bob transmits
    # his public key [KB] (but NOT his private key kB) to Alice.
    kB, KB = dh.generate_keypair(q, p, g)

    # Alice, having received Bob's public key [KB], validates it.
    dh.validate_pub_key(KB, q, p)

    # Then, Alice uses Bob's public key [KB], along with her private key
    # kA, to generate a session key kSessionA, which must be kept secret.
    kSessionA = dh.generate_session_key(KB, kA, q, p)

    # Bob, having received Alice's public key [KA], uses it, along with his private key
    # kB to generate a session key kSessionB, which must be kept secret. Due to the
    # essential property of DH, the session keys kSessionA and kSessionB, that Alice
    # and Bob have computed independently, should be identical.
    kSessionB = dh.generate_session_key(KA, kB, q, p)
    assert kSessionA == kSessionB

    # Alice produces a message [mA], encrypts it using her session key kSessionA, and
    # transmits the ciphertext [mAC] to Bob.
    mA = "Encrypt me!"
    mAC = sym.encrypt(kSessionA, mA)

    # Bob receives the ciphertext [mAC], and decrypts it using his session key kSessionB.
    # The message Bob decrypts mB must equal the message Alice encrypted mA.
    mB = sym.decrypt(kSessionB, mAC)
    assert mA == mB

    print("full protocol test passed")


if __name__ == "__main__":
    main()
