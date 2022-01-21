import sys
sys.path.append("../src")
import importlib

import ec

# Test curve 1 parameters
p, a, b, Gx, Gy, n, h = 17, 2, 2, 5, 1, 19, 1
pt_group = [[5,1],[6,3],[10,6],[3,1],[9,16],[16,13],[0,6],[13,7],[7,6],
              [7,11],[13,10],[0,11],[16,4],[9,1],[3,16],[10,11],[6,14],[5,16]]
Curve1 = (p, a, b, Gx, Gy, n, h, pt_group)

# Test curve 2 parameters
p, a, b, Gx, Gy, n, h = 23, 1, 4, 0, 2, 29, 1
pt_group = [[0,2],[13,12],[11,9],[1,12],[7,20],[9,11],[15,6],[14,5],[4,7],
              [22,5],[10,5],[17,9],[8,15],[18,9],[18,14],[8,8],[17,14],[10,18],
              [22,18],[4,16],[14,18],[15,17],[9,12],[7,3],[1,11],[11,14],[13,11],[0,21]]
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
    print("all ec tests passed")

def test_add():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]

        # Repeated addition of all group elements to the generator _G.
        for i in range(1, len(pt_group)):
            pt = ec.add(ec._G, pt_group[i-1])
            assert pt == pt_group[i]

        # Add selected group elements.
        pt = ec.add(pt_group[0], pt_group[9])
        assert pt == pt_group[10]

        # Commute
        pt = ec.add(pt_group[9], pt_group[0])
        assert pt == pt_group[10]

        pt = ec.add(pt_group[5], pt_group[3])
        assert pt == pt_group[9]

        # Add selected group elements to the identity element.
        pt = ec.add(ec._G, ec._i)
        assert pt == ec._G

        pt = ec.add(pt_group[3], ec._i)
        assert pt == pt_group[3]

        pt = ec.add(ec._i, ec._G)
        assert pt == ec._G

        pt = ec.add(ec._i, pt_group[8])
        assert pt == pt_group[8]

        # Add the identity elements.
        pt = ec.add(ec._i, ec._i)
        assert pt == ec._i

        # Add identical group elements.
        pt = ec.add(pt_group[2], pt_group[2])
        assert pt == pt_group[5]

        # Add first and last group elements.
        pt = ec.add(pt_group[0], pt_group[len(pt_group)-1])
        assert pt == ec._i

    print("test_add passed")

def test_double():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(1, len(pt_group)):
            pt = ec.double(pt_group[i-1])
            assert pt == pt_group[((i*2)%curve[5])-1]

    print("test_double passed")

def test_validate_curve_params():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        ec._validate_curve_params(B_iters)

    print("test_validate_curve_params passed")

def test_point_at():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(1, len(pt_group)+1):
            assert ec._point_at(i) == pt_group[i-1]

        assert ec._point_at(curve[5]) == ec._i

    print("test_point_at passed")

def test_fast_point_at():
    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(1, len(pt_group)+1):
            assert ec._point_at(i) == ec._fast_point_at(i)

        assert ec._fast_point_at(curve[5]) == ec._i

    print("test_fast_point_at passed")

def test_x_times_pt():
    importlib.reload(ec)
    for _ in range(100):
        d, Q = ec.generate_keypair()
        assert ec.x_times_pt(ec._n, Q) == ec._i

    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        pt_group = curve[7]
        for i in range(0, len(pt_group)):
            assert ec.x_times_pt(curve[5], pt_group[i]) == ec._i

    print("test_x_times_pt passed")

def test_generate_keypair_and_validate_pub_key():
    importlib.reload(ec)
    for _ in range(100):
        d, Q = ec.generate_keypair()
        ec.validate_pub_key(Q)
        pt = ec._fast_point_at(d)
        assert pt == Q

    print("test_generate_keypair passed")

def test_hash_to_int():
    importlib.reload(ec)
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        e = ec.hash_to_int(m)
        assert e.bit_length() <= ec._n.bit_length()

    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            e = ec.hash_to_int(m)
            assert e.bit_length() <= ec._n.bit_length()

    print("test_hash_to_int passed")

def test_sign_and_verify():
    importlib.reload(ec)
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        d, Q = ec.generate_keypair()
        S = ec.sign(m, d)
        assert ec.verify(m, S, Q)

    for curve in Curves:
        ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
        for m in ["When", "in", "the", "course", "of", "human", "events..."]:
            ec.new_curve(curve[0], curve[1], curve[2], curve[3], curve[4], curve[5], curve[6], B_iters)
            d, Q = ec.generate_keypair()
            S = ec.sign(m, d)
            assert ec.verify(m, S, Q)

    print("test_sign_and_verify passed")

if __name__ == "__main__":
    main()