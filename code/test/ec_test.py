import sys
sys.path.append("../src")
import importlib

import ec
import prng
import sym

# Test curve 1 parameters
p, a, b, Gx, Gy, n, h = 17, 2, 2, 5, 1, 19, 1
pt_group = [[5,1],[6,3],[10,6],[3,1],[9,16],[16,13],[0,6],[13,7],[7,6],
            [7,11],[13,10],[0,11],[16,4],[9,1],[3,16],[10,11],[6,14],
            [5,16],[None,None]]

Curve1 = (p, a, b, Gx, Gy, n, h, pt_group)

# Test curve 2 parameters
p, a, b, Gx, Gy, n, h = 23, 1, 4, 0, 2, 29, 1
pt_group = [[0,2],[13,12],[11,9],[1,12],[7,20],[9,11],[15,6],[14,5],[4,7],
            [22,5],[10,5],[17,9],[8,15],[18,9],[18,14],[8,8],[17,14],
            [10,18],[22,18],[4,16],[14,18],[15,17],[9,12],[7,3],[1,11],
            [11,14],[13,11],[0,21],[None,None]]

Curve2 = (p, a, b, Gx, Gy, n, h, pt_group)
Curves = (Curve1, Curve2)

B_iters = 5

def main():
    print("Running ec tests...")
    test_add()
    test_double()
    test_validate_curve_params()
    test_point_at()
    test_fast_point_at()
    test_x_times_pt()
    test_generate_keypair_and_validate_pub_key()
    test_sign_and_verify()
    test_full_protocol()
    print("all ec tests passed")

def test_add():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]

        # Repeated addition of all group elements to the specified base point.
        for i in range(1, len(pt_group)):
            pt = ec.add(ec._G, pt_group[i-1])
            assert pt == pt_group[i]

        # Repeated addition of all group elements to a randomly selected base point.
        rand_index = prng.randrange(0,len(pt_group))
        pt_set2 = {tuple(pt_group[rand_index])}
        for i in range(1, len(pt_group)):
            pt = ec.add(pt_group[rand_index], pt_group[i-1])
            pt_set2.add(tuple(pt))

        pt_set1 = set(map(lambda pt: tuple(pt), pt_group))
        assert len(pt_set2.difference(pt_set1)) == 0

        # Add selected group elements.
        pt = ec.add(pt_group[0], pt_group[9])
        assert pt == pt_group[10]

        # Commute.
        pt = ec.add(pt_group[9], pt_group[0])
        assert pt == pt_group[10]

        # Add selected group elements.
        pt = ec.add(pt_group[5], pt_group[3])
        assert pt == pt_group[9]

        # Commute.
        pt = ec.add(pt_group[5], pt_group[3])
        assert pt == pt_group[9]

        # Add the identity element to the base point.
        pt = ec.add(ec._G, ec._i)
        assert pt == ec._G

        # Commute.
        pt = ec.add(ec._i, ec._G)
        assert pt == ec._G

        # Add selected point to the identity element.
        pt = ec.add(pt_group[3], ec._i)
        assert pt == pt_group[3]

        # Commute.
        pt = ec.add(ec._i, pt_group[3])
        assert pt == pt_group[3]

        # Add the identity elements.
        pt = ec.add(ec._i, ec._i)
        assert pt == ec._i

        # Add the same two group elements.
        pt = ec.add(pt_group[2], pt_group[2])
        assert pt == pt_group[5]

        # Add first and last (non-identity) group elements.
        pt = ec.add(pt_group[0], pt_group[len(pt_group)-2])
        assert pt == ec._i

    print("test_add passed")

def test_double():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]

        # Double each group element starting with the base point.
        for i in range(1, len(pt_group)):
            pt = ec.double(pt_group[i-1])
            assert pt == pt_group[((i*2)%curve[5])-1]

    print("test_double passed")

def test_validate_curve_params():
    for curve in Curves:
        # Test with valid curve parameters.
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        ec.validate_curve_params(B_iters)

    try:
        # Test with invalid curve parameter.
        ec.new_curve(curve[0], curve[1], curve[2], curve[4], curve[4], curve[5], curve[6], B_iters)
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)

    print("test_validate_curve_params passed")

def test_point_at():
    for curve in Curves:
        # Test slow, add-only method of finding a point.
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(1, len(pt_group)+1):
            assert ec._point_at(i) == pt_group[i-1]

        assert ec._point_at(curve[5]) == ec._i

    print("test_point_at passed")

def test_fast_point_at():
    for curve in Curves:
        # Test fast, double-and-add method of finding a point.
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(1, len(pt_group)+1):
            assert ec._point_at(i) == ec._fast_point_at(i)

        assert ec._fast_point_at(curve[5]) == ec._i

    print("test_fast_point_at passed")

def test_x_times_pt():
    importlib.reload(ec)
    for _ in range(100):
        # Test that the order of the curve group times 100 randomly selected points on the curve yields
        # the identity element using the secp256k1 curve.
        d, Q = ec.generate_keypair()
        assert ec.x_times_pt(ec._n, Q) == ec._i

    for curve in Curves:
        # Test that the order of the curve group times any point on the curve yields the identity
        # element using the small test curves.
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(0, len(pt_group)):
            assert ec.x_times_pt(curve[5], pt_group[i]) == ec._i

    print("test_x_times_pt passed")

def test_generate_keypair_and_validate_pub_key():
    importlib.reload(ec)
    for _ in range(100):
        # Validate 100 randomly generated public keys from the secp256k1 curve.
        d, Q = ec.generate_keypair()
        try:
            ec.validate_pub_key(Q)
        except Exception as e:
            assert False

    print("test_generate_keypair passed")

def test_hash_to_int():
    # Test bit length of integer representative does not exceed that of the curve's order.
    importlib.reload(ec)
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        e = ec._hash_to_int(m)
        assert e.bit_length() <= ec._n.bit_length()

    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            e = ec._hash_to_int(m)
            assert e.bit_length() <= ec._n.bit_length()

    print("test_hash_to_int passed")

def test_sign_and_verify():
    importlib.reload(ec)
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        # Test sign/verify using the secp256k1 curve.
        d, Q = ec.generate_keypair()
        S = ec.sign(d, m)
        assert ec.verify(Q, m, S)

    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        # Test sign/verify using the small test curves.
            d, Q = ec.generate_keypair()
            S = ec.sign(d, m)
            assert ec.verify(Q, m, S)

    print("test_sign_and_verify passed")

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

    print("test_full_protocol passed")

if __name__ == "__main__":
    main()