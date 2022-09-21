import concurrent.futures
import copy
import os

from core import curves
from core import ec
from core import prng

from . import sym
from . import util

# Test curve 1 parameters
pt_group = [
    [5, 1],
    [6, 3],
    [10, 6],
    [3, 1],
    [9, 16],
    [16, 13],
    [0, 6],
    [13, 7],
    [7, 6],
    [7, 11],
    [13, 10],
    [0, 11],
    [16, 4],
    [9, 1],
    [3, 16],
    [10, 11],
    [6, 14],
    [5, 16],
    [None, None],
]
test_curve_1 = {"curve": curves.Curve(17, 2, 2, 5, 1, 19, 1), "pts": pt_group}

# Test curve 2 parameters
pt_group = [
    [0, 2],
    [13, 12],
    [11, 9],
    [1, 12],
    [7, 20],
    [9, 11],
    [15, 6],
    [14, 5],
    [4, 7],
    [22, 5],
    [10, 5],
    [17, 9],
    [8, 15],
    [18, 9],
    [18, 14],
    [8, 8],
    [17, 14],
    [10, 18],
    [22, 18],
    [4, 16],
    [14, 18],
    [15, 17],
    [9, 12],
    [7, 3],
    [1, 11],
    [11, 14],
    [13, 11],
    [0, 21],
    [None, None],
]
test_curve_2 = {"curve": curves.Curve(23, 1, 4, 0, 2, 29, 1), "pts": pt_group}
test_curves = [test_curve_1, test_curve_2]

real_curves = [
    curves.Secp192k1(),
    curves.Secp192r1(),
    curves.Secp224k1(),
    curves.Secp224r1(),
    curves.Secp256k1(),
    curves.Secp256r1(),
    curves.Secp384r1(),
    curves.Secp521r1(),
]

_TEST_CURVE_B_ITERS = 5


def main():
    print("Running ec tests...")
    test_add()
    test_double()
    test_validate_curve_params()
    test_point_at()
    test_fast_point_at()
    test_x_times_pt()
    test_generate_keypair_and_validate_pub_key()
    test_hash_to_int()
    test_sign_and_verify()
    test_full_protocol()
    print("all ec tests passed")


def test_add():
    print("test_add started")

    for test_curve in test_curves:
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        pt_group_local = test_curve["pts"]

        # Repeated addition of all group elements to the specified base point.
        for i in range(1, len(pt_group_local)):
            pt = ec._add(test_curve["curve"].G, pt_group_local[i - 1])
            assert pt == pt_group_local[i]

        # Repeated addition of all group elements to a randomly selected base point.
        rand_index = prng.randrange(0, len(pt_group_local))
        pt_set2 = {tuple(pt_group_local[rand_index])}
        for i in range(1, len(pt_group_local)):
            pt = ec._add(pt_group_local[rand_index], pt_group_local[i - 1])
            pt_set2.add(tuple(pt))

        pt_set1 = {tuple(pt) for pt in pt_group_local}
        assert len(pt_set2.difference(pt_set1)) == 0

        # Add selected group elements.
        pt = ec._add(pt_group_local[0], pt_group_local[9])
        assert pt == pt_group_local[10]

        # Commute.
        pt = ec._add(pt_group_local[9], pt_group_local[0])
        assert pt == pt_group_local[10]

        # Add selected group elements.
        pt = ec._add(pt_group_local[5], pt_group_local[3])
        assert pt == pt_group_local[9]

        # Commute.
        pt = ec._add(pt_group_local[5], pt_group_local[3])
        assert pt == pt_group_local[9]

        # Add the identity element to the base point.
        pt = ec._add(test_curve["curve"].G, ec._I)
        assert pt == test_curve["curve"].G

        # Commute.
        pt = ec._add(ec._I, test_curve["curve"].G)
        assert pt == test_curve["curve"].G

        # Add selected point to the identity element.
        pt = ec._add(pt_group_local[3], ec._I)
        assert pt == pt_group_local[3]

        # Commute.
        pt = ec._add(ec._I, pt_group_local[3])
        assert pt == pt_group_local[3]

        # Add the identity elements.
        pt = ec._add(ec._I, ec._I)
        assert pt == ec._I

        # Add the same two group elements.
        pt = ec._add(pt_group_local[2], pt_group_local[2])
        assert pt == pt_group_local[5]

        # Add first and last (non-identity) group elements.
        pt = ec._add(pt_group_local[0], pt_group_local[len(pt_group_local) - 2])
        assert pt == ec._I

    # Try to add bogus points.
    try:
        ec._add([6, 12], [19, 2])
        assert False
    except Exception:
        pass

    print("test_add passed")


def test_double():
    print("test_double started")
    for test_curve in test_curves:
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        pt_group_local = test_curve["pts"]

        # Double each group element starting with the base point.
        for i in range(1, len(pt_group_local)):
            pt = ec._double(pt_group_local[i - 1])
            assert pt == pt_group_local[((i * 2) % test_curve["curve"].n) - 1]

    # Try to double a bogus point.
    try:
        ec._double([19, 2])
        assert False
    except Exception:
        pass

    print("test_double passed")


def test_validate_curve_params():
    print("test_validate_curve_params started")
    # Test with default curve
    for real_curve in real_curves:
        ec.new_curve(real_curve)
        ec._validate_curve_params()

    for test_curve in test_curves:
        # Test with valid curve parameters.
        try:
            ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
            ec._validate_curve_params(_TEST_CURVE_B_ITERS)
        except Exception:
            assert False

    try:
        # Test with invalid curve parameter on test curve.
        ec.new_curve(curves.Curve(23, 1, 4, 2, 2, 29, 1), _TEST_CURVE_B_ITERS)
        ec._validate_curve_params(_TEST_CURVE_B_ITERS)
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)

    for real_curve in real_curves:
        try:
            # Test with invalid curve parameter on real curve.
            deep_copy = copy.deepcopy(real_curve)
            i = prng.randbelow(7)
            match i:
                case 0:
                    deep_copy.p = deep_copy.p + 1
                case 1:
                    deep_copy.a = deep_copy.a + 1
                case 2:
                    deep_copy.b = deep_copy.b + 1
                case 3:
                    deep_copy.Gx = deep_copy.Gx + 1
                case 4:
                    deep_copy.Gy = deep_copy.Gy + 1
                case 5:
                    deep_copy.n = deep_copy.n + 1
                case 6:
                    deep_copy.h = deep_copy.h + 1
            ec.new_curve(deep_copy)
            ec._validate_curve_params()
            assert False
        except Exception as e:
            assert isinstance(e, ValueError)

    print("test_validate_curve_params passed")


def test_point_at():
    print("test_point_at started")
    for test_curve in test_curves:
        # Test slow, add-only method of finding a point.
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        pt_group_local = test_curve["pts"]
        for i in range(1, len(pt_group_local) + 1):
            assert ec._point_at(i) == pt_group_local[i - 1]

        assert ec._point_at(test_curve["curve"].n) == ec._I

    print("test_point_at passed")


def test_fast_point_at():
    print("test_fast_point_at started")
    for test_curve in test_curves:
        # Test fast, double-and-add method of finding a point.
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        pt_group_local = test_curve["pts"]
        for i in range(1, len(pt_group_local) + 1):
            assert ec._point_at(i) == ec._fast_point_at(i)

        assert ec._fast_point_at(test_curve["curve"].n) == ec._I

    print("test_fast_point_at passed")


def test_x_times_pt():
    print("test_x_times_pt started")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(x_times_pt, real_curves)
        util.process_results(results)

    for test_curve in test_curves:
        # Test that the order of the curve group times any point on the curve yields the identity
        # element using the small test curves.
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        pt_group_local = test_curve["pts"]
        for i in range(0, len(pt_group_local)):
            assert ec._x_times_pt(test_curve["curve"].n, pt_group_local[i]) == ec._I

    print("test_x_times_pt passed")


def x_times_pt(curve):
    print(
        f"\ttesting scalar point multiplication on curve {type(curve).__name__} from pid={os.getpid()}"
    )
    ec.new_curve(curve)
    for _ in range(100):
        # Test that the order of the curve group times 100 randomly selected points on the curve
        # yields the identity element using the secp256k1 curve.
        _, Q = ec.generate_keypair()
        assert ec._x_times_pt(ec._CURVE.n, Q) == ec._I

    print(
        f"\tscalar point multiplication passed on curve {type(curve).__name__} from pid={os.getpid()}"
    )


def test_generate_keypair_and_validate_pub_key():
    print("test_generate_keypair started")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(generate_keypair_and_validate_pub_key, real_curves)
        util.process_results(results)

    print("test_generate_keypair passed")


def generate_keypair_and_validate_pub_key(curve):
    print(
        f"\ttesting keypair generation and validation on curve {type(curve).__name__} from pid={os.getpid()}"
    )
    ec.new_curve(curve)
    for _ in range(100):
        # Validate 100 randomly generated public keys from the secp256k1 curve.
        _, Q = ec.generate_keypair()
        try:
            ec.validate_pub_key(Q)
        except Exception:
            assert False

    print(
        f"\tkeypair generation and validation passed on curve {type(curve).__name__} from pid={os.getpid()}"
    )


def test_hash_to_int():
    print("test_hash_to_int started")
    # Test bit length of integer representative does not exceed that of the curve's order.
    for real_curve in real_curves:
        ec.new_curve(real_curve)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            e = ec._hash_to_int(m)
            assert e.bit_length() <= ec._CURVE.n.bit_length()

    for test_curve in test_curves:
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            e = ec._hash_to_int(m)
            assert e.bit_length() <= ec._CURVE.n.bit_length()

    print("test_hash_to_int passed")


def test_sign_and_verify():
    print("test_sign_and_verify started")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(sign_and_verify, real_curves)
        util.process_results(results)

    for test_curve in test_curves:
        ec.new_curve(test_curve["curve"], _TEST_CURVE_B_ITERS)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            # Test sign/verify using the small test curves.
            d, Q = ec.generate_keypair()
            S = ec.sign(d, m)
            assert ec.verify(Q, m, S)

    print("test_sign_and_verify passed")


def sign_and_verify(curve):
    print(
        f"\ttesting sign and verify on curve {type(curve).__name__} from pid={os.getpid()}"
    )
    ec.new_curve(curve)
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        # Test sign/verify using the secp256k1 curve.
        d, Q = ec.generate_keypair()
        S = ec.sign(d, m)
        assert ec.verify(Q, m, S)

    print(
        f"\tsign and verify passed on curve {type(curve).__name__} from pid={os.getpid()}"
    )


def test_full_protocol():
    print("test_full_protocol started")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(full_protocol, real_curves)
        util.process_results(results)

    print("test_full_protocol passed")


def full_protocol(curve):
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
    # dA, [QA] = generate_keypair()               dB, [QB] = generate_keypair()            #
    #                                                                                      #
    # [QA]                                --->    [QA]                                     #
    #                                                                                      #
    # [QB]                                <---    [QB]                                     #
    #                                                                                      #
    # kSessionA =                                 kSessionB =                              #
    #   generate_session_key(dA, QB)                generate_session_key(dB, QA)           #
    #                                                                                      #
    # mA = "8675309" (Message to be                                                        #
    #         signed and encrypted.)                                                       #
    #                                                                                      #
    # [sA] = sign(dA, mA)                                                                  #
    #                                                                                      #
    # [mAC] = sym_encrypt(kSessionA, mA)                                                   #
    #                                                                                      #
    # [sA, mAC]                           --->      [sA, mAC] (Bob receives message        #
    #                                                    signature, and encrypted message, #
    #                                                    from Alice.)                      #
    #                                                                                      #
    #                                               mB = sym_decrypt(kSessionB, [mAC])     #
    #                                                                                      #
    #                                               result = verify([QB], mB, [sA])        #
    #                                                                                      #
    # If, in the very last step, the result of the verify() operation performed by Bob     #
    # returns True, Bob can be sure the message mB he decrypts and verifies was signed by  #
    # Alice's private key; and is therefore identical to the message mA that Alice signed  #
    # and encrypted.                                                                       #
    ########################################################################################

    print(
        f"\ttesting full protocol on curve {type(curve).__name__} from pid={os.getpid()}"
    )

    ec.new_curve(curve)

    # Alice generates her keypair, dA and [QA], and transmits her public key [QA] to Bob.
    # She keeps her private key dA secret.
    dA, QA = ec.generate_keypair()

    # Bob generates his keypair, dB and [QB], and transmits his public key [QB] to Alice.
    # He keeps his private key dB secret.
    dB, QB = ec.generate_keypair()

    # Alice generates her ECDH session key kSessionA; this key must be kept secret.
    kSessionA = ec.generate_session_key(dA, QB)

    # Bob generates his ECDH session key kSessionB; this key must be kept secret. Due to the
    # essential property of DH, Bob's session key kSessionB should be identical to Alice's
    # kSessionB, and it should be computationally infeasible for an attacker to derive this
    # key with possession of either Alice or Bob's public keys, [QA] or [QB].
    kSessionB = ec.generate_session_key(dB, QA)

    # Alice produces a message mA, and signs it with her private key dA, thus producing the
    # ECDSA signature [sA].
    mA = "8675309"
    sA = ec.sign(dA, mA)

    # Alice encrypts her message mA using her ECDH session key kSessionA. Alice transmits the
    # message ciphertext [mAC] and the message signature [sA] to Bob.
    mAC = sym.encrypt(kSessionA, mA)

    # Bob decrypts the ciphertext [mAC] of Alice's message mA with his ECDH session key
    # kSessionB, and stores the result in mB. Then he verifies the decrypted message mB with
    # the signature Alice sent him [sA], and her public key [QA]. If the verify operation
    # returns True, Bob can be satisfied that nobody but he and Alice knows the contents of
    # mB (confidentiality), no one has tampered with mB (integrity), and that it was indeed
    # Alice who sent him mB (authenticity).
    mB = sym.decrypt(kSessionB, mAC)
    assert ec.verify(QA, mB, sA)

    print(
        f"\tfull protocol test on curve {type(curve).__name__} passed from pid={os.getpid()}"
    )


if __name__ == "__main__":
    main()
