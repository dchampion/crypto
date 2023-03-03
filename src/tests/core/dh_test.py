import hashlib
from core import primes
from core import dh

from . import sym
from . import util


@util.test_log
def main():
    test_dh_setup()
    test_generate_p()
    test_full_protocol()
    test_full_protocol_dh_class()
    test_misc_dh_class()
    test_hash_injection()


@util.test_log
def test_dh_setup():
    util.parallelize(dh_setup, \
        util.random_ranges(dh._P_MIN_BIT_LEN, dh._P_MAX_BIT_LEN+1, 1024))


def dh_setup(modulus_bit_len):
    try:
        q, p, g = dh.generate_parameters(modulus_bit_len)
        dh.validate_parameters(q, p, g)

        x1, y1 = dh.generate_keypair(q, p, g)
        dh.validate_pub_key(y1, q, p)
        assert 1 <= x1 < q, "x1 is out of range"

        x2, y2 = dh.generate_keypair(q, p, g)
        dh.validate_pub_key(y2, q, p)
        assert 1 <= x2 < q, "x2 is out of range"
        assert x1 != x2, "x1 is equal to x2; bad PRNG?"

        ses_key_1 = dh.generate_session_key(y2, x1, q, p)
        ses_key_2 = dh.generate_session_key(y1, x2, q, p)
        assert ses_key_1 == ses_key_2, "Secrets don't match"

    except ValueError as ve:
        assert False, f"ValueError: {ve}"
    except Exception as e:
        assert False, f"Exception: {e}"


@util.test_log
def test_generate_p():
    util.parallelize(generate_p, \
        [primes.generate_prime(dh._Q_BIT_LEN) for _ in range(util.num_cores())])


def generate_p(q):
    p_bit_len = util.random_range(dh._P_MIN_BIT_LEN, dh._P_MAX_BIT_LEN+1, 1024)
    _, p = dh._generate_p(q, p_bit_len)
    assert p.bit_length() == p_bit_len


@util.test_log
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
    # xA, [yA] =                                                                             #
    #      generate_keypair(q, p, g)                                                         #
    #                                                                                        #
    # [p, q, g, yA]                     --->      [q, p, g, yA]                              #
    #                                             validate_parameters(q, p, g)               #
    #                                             validate_pub_key([yA], q, p)               #
    #                                                                                        #
    #                                             xB, [yB] =                                 #
    #                                                  generate_keypair(q, p, g)             #
    #                                                                                        #
    # [yB]                              <---      [yB]                                       #
    # validate_pub_key([yB], q, p)                                                           #
    #                                                                                        #
    # ses_key_a =                                 ses_key_b =                                #
    #      generate_session_key([yB], xA, q, p)         generate_session_key([yA], xB, q, p) #
    #                                                                                        #
    # [mAC] = sym_encrypt(ses_key_a, mA)                                                     #
    #                                                                                        #
    # [mAC]                             --->      [mAC]                                      #
    #                                                                                        #
    #                                             mB = sym.decrypt(ses_key_b, [mAC])         #
    #                                                                                        #
    # The message mB Bob decrypts must equal the message mA that Alice encrypted.            #
    ##########################################################################################

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
    xA, yA = dh.generate_keypair(q, p, g)

    # Bob MUST validate the public parameters [p, q, g] he receives from Alice.
    dh.validate_parameters(q, p, g)

    # Bob MUST ALSO validate Alice's public key [KA].
    dh.validate_pub_key(yA, q, p)

    # Bob generates his own private and public keys kB and [KB], using as inputs the
    # public parameters [p, q, g] (now validated) he received from Alice. Bob transmits
    # his public key [KB] (but NOT his private key kB) to Alice.
    xB, yB = dh.generate_keypair(q, p, g)

    # Alice, having received Bob's public key [KB], validates it.
    dh.validate_pub_key(yB, q, p)

    # Then, Alice uses Bob's public key [KB], along with her private key
    # kA, to generate a session key kSessionA, which must be kept secret.
    ses_key_a = dh.generate_session_key(yB, xA, q, p)

    # Bob, having received Alice's public key [KA], uses it, along with his private key
    # kB to generate a session key kSessionB, which must be kept secret. Due to the
    # essential property of DH, the session keys kSessionA and kSessionB, that Alice
    # and Bob have computed independently, should be identical.
    ses_key_b = dh.generate_session_key(yA, xB, q, p)
    assert ses_key_a == ses_key_b

    # Alice produces a message [mA], encrypts it using her session key kSessionA, and
    # transmits the ciphertext [mAC] to Bob.
    mA = "Encrypt me!"
    mAC = sym.encrypt(ses_key_a, mA)

    # Bob receives the ciphertext [mAC], and decrypts it using his session key kSessionB.
    # The message Bob decrypts mB must equal the message Alice encrypted mA.
    mB = sym.decrypt(ses_key_b, mAC)
    assert mA == mB


@util.test_log
def test_full_protocol_dh_class():
    key_a = dh.make_key()
    key_params_a = key_a.public_parameters()
    key_pub_a = key_a.public_key()

    key_b = dh.make_key(key_params_a)
    assert key_b.public_parameters() == key_params_a

    key_pub_b = key_b.public_key()
    ses_key_b = key_b.make_session_key(key_pub_a)

    ses_key_a = key_a.make_session_key(key_pub_b)
    assert ses_key_a == ses_key_b

    mA = "Encrypt me!"
    mAC = sym.encrypt(ses_key_a, mA)
    mB = sym.decrypt(ses_key_b, mAC)
    assert mA == mB


@util.test_log
def test_misc_dh_class():
    key1 = dh.make_key()
    key2 = dh.make_key()
    key_dict = {key1: "key1", key2: "key2"}
    assert key_dict[key1] == "key1"
    assert "key1" == key_dict[key1]
    assert key_dict[key2] == "key2"
    assert "key2" == key_dict[key2]
    assert key_dict[key1] != "key2"
    assert "key1" != key_dict[key2]
    assert key_dict[key2] != "key1"
    assert "key2" != key_dict[key1]

    parameters1 = dh.make_parameters()
    parameters2 = dh.make_parameters()
    params_dict = {parameters1: "parameters1", parameters2: "parameters2"}
    assert params_dict[parameters1] == "parameters1"
    assert "parameters1" == params_dict[parameters1]
    assert params_dict[parameters2] == "parameters2"
    assert "parameters2" == params_dict[parameters2]
    assert params_dict[parameters1] != "parameters2"
    assert "parameters1" != params_dict[parameters2]
    assert params_dict[parameters2] != "parameters1"
    assert "parameters2" != params_dict[parameters1]


@util.test_log
def test_hash_injection():
    q, p, g = dh.generate_parameters(dh._P_MIN_BIT_LEN)
    dh.validate_parameters(q, p, g)

    x_a, y_a = dh.generate_keypair(q, p, g)
    x_b, y_b = dh.generate_keypair(q, p, g)

    ses_key_a = dh.generate_session_key(y_b, x_a, q, p, hashlib.sha224())
    ses_key_b = dh.generate_session_key(y_a, x_b, q, p, hashlib.sha512())
    assert ses_key_a != ses_key_b, "Secrets match, but they should not"

    key_a = dh.make_key()
    key_b = dh.make_key(key_a.public_parameters())

    ses_key_a = key_a.make_session_key(key_b.public_key(), hashlib.sha1())
    ses_key_b = key_b.make_session_key(key_a.public_key(), hashlib.sha384())
    assert ses_key_a != ses_key_b, "Secrets match, but they should not"

    ses_key_a = dh.generate_session_key(y_b, x_a, q, p, hashlib.sha224())
    ses_key_b = dh.generate_session_key(y_a, x_b, q, p, hashlib.sha224())
    assert ses_key_a == ses_key_b, "Secrets don't match, but they should"

    ses_key_a = key_a.make_session_key(key_b.public_key(), hashlib.sha1())
    ses_key_b = key_b.make_session_key(key_a.public_key(), hashlib.sha1())
    assert ses_key_a == ses_key_b, "Secrets don't match, but they should"


if __name__ == "__main__":
    main()
