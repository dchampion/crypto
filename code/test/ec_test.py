import sys
sys.path.append("../src")
import importlib

import ec

# Test curve 1 parameters
p, a, b, Gx, Gy, n, h = 17, 2, 2, 5, 1, 19, 1
pt_group = [[5,1],[6,3],[10,6],[3,1],[9,16],[16,13],[0,6],[13,7],[7,6],
              [7,11],[13,10],[0,11],[16,4],[9,1],[3,16],[10,11],[6,14],[5,16]]
C1 = (p, a, b, Gx, Gy, n, h, pt_group)

# Test curve 2 parameters
p, a, b, Gx, Gy, n, h = 23, 1, 4, 0, 2, 29, 1
pt_group = [[0,2],[13,12],[11,9],[1,12],[7,20],[9,11],[15,6],[14,5],[4,7],
              [22,5],[10,5],[17,9],[8,15],[18,9],[18,14],[8,8],[17,14],[10,18],
              [22,18],[4,16],[14,18],[15,17],[9,12],[7,3],[1,11],[11,14],[13,11],[0,21]]
C2 = (p, a, b, Gx, Gy, n, h, pt_group)

B_iters = 5

def main():
    print("Running ec tests...")
    test_add(C1)
    test_add(C2)
    test_double(C1)
    test_double(C2)
    test_validate_curve_params(C1)
    test_validate_curve_params(C2)
    test_point_at(C1)
    test_point_at(C2)
    test_fast_point_at(C1)
    test_fast_point_at(C2)
    test_x_times_pt()
    test_generate_and_validate_key()
    print("all ec tests passed")

def test_add(C):
    ec.new_curve(C[0], C[1], C[2], C[3], C[4], C[5], C[6], B_iters)
    pt_group = C[7]
    
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

def test_double(C):
    ec.new_curve(C[0], C[1], C[2], C[3], C[4], C[5], C[6], B_iters)
    pt_group = C[7]
    for i in range(1, len(pt_group)):
        pt = ec.double(pt_group[i-1])
        assert pt == pt_group[((i*2)%C[5])-1]

    print("test_double passed")

def test_validate_curve_params(C):
    ec.new_curve(C[0], C[1], C[2], C[3], C[4], C[5], C[6], B_iters)
    ec._validate_curve_params(B_iters)

    print("test_validate_curve_params passed")

def test_point_at(C):
    ec.new_curve(C[0], C[1], C[2], C[3], C[4], C[5], C[6], B_iters)
    pt_group = C[7]
    for i in range(1, len(pt_group)+1):
        assert ec._point_at(i) == pt_group[i-1]

    assert ec._point_at(C[5]) == ec._i

    print("test_point_at passed")

def test_fast_point_at(C):
    ec.new_curve(C[0], C[1], C[2], C[3], C[4], C[5], C[6], B_iters)
    pt_group = C[7]
    for i in range(1, len(pt_group)+1):
        assert ec._point_at(i) == ec._fast_point_at(i)

    assert ec._fast_point_at(C[5]) == ec._i

    print("test_fast_point_at passed")

def test_x_times_pt():
    importlib.reload(ec)
    for _ in range(100):
        d, Q = ec.generate_key()
        assert ec._x_times_pt(ec._n, Q) == ec._i

    ec.new_curve(C1[0], C1[1], C1[2], C1[3], C1[4], C1[5], C1[6], B_iters)
    pt_group = C1[7]
    for i in range(0, len(pt_group)):
        assert ec._x_times_pt(C1[5], pt_group[i]) == ec._i

    ec.new_curve(C2[0], C2[1], C2[2], C2[3], C2[4], C2[5], C2[6], B_iters)
    pt_group = C2[7]
    for i in range(0, len(pt_group)):
        assert ec._x_times_pt(C2[5], pt_group[i]) == ec._i

    print("test_x_times_pt passed")

def test_generate_and_validate_key():
    importlib.reload(ec)
    for _ in range(100):
        d, Q = ec.generate_key()
        ec.validate_key(Q)
        pt = ec._fast_point_at(d)
        assert pt == Q

    print("test_generate_key passed")

if __name__ == "__main__":
    main()