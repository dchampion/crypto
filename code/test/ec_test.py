import sys
sys.path.append("../src")
import importlib

import ec

# Test curve parameters
p = 17
a = 2
b = 2
Gx = 5
Gy = 1
n = 19
h = 1

B_iters = 5

pt_group = [[5,1],[6,3],[10,6],[3,1],[9,16],[16,13],[0,6],[13,7],[7,6],
            [7,11],[13,10],[0,11],[16,4],[9,1],[3,16],[10,11],[6,14],[5,16]]

def main():
    print("Running ec tests...")
    test_add()
    test_double()
    test_validate_curve_params()
    test_point_at()
    test_fast_point_at()
    test_generate_key()
    print("all ec tests passed")

def test_add():
    ec.new_curve(p, a, b, Gx, Gy, n, h, B_iters)
    for i in range(1, len(pt_group)):
        pt = ec.add(pt_group[i-1])
        assert pt == pt_group[i]

    print("test_add passed")

def test_double():
    ec.new_curve(p, a, b, Gx, Gy, n, h, B_iters)
    for i in range(1, len(pt_group)):
        pt = ec.double(pt_group[i-1])
        assert pt == pt_group[((i*2)%n)-1]

    print("test_double passed")

def test_validate_curve_params():
    ec.new_curve(p, a, b, Gx, Gy, n, h, B_iters)
    ec._validate_curve_params(B_iters)

    print("test_validate_curve_params passed")

def test_fast_point_at():
    ec.new_curve(p, a, b, Gx, Gy, n, h, B_iters)
    for i in range(1, len(pt_group)+1):
        assert ec._point_at(i) == ec._fast_point_at(i)

    assert ec._fast_point_at(n) == ec._pt_i

    print("test_fast_point_at passed")

def test_point_at():
    ec.new_curve(p, a, b, Gx, Gy, n, h, B_iters)
    for i in range(1, len(pt_group)+1):
        assert ec._point_at(i) == pt_group[i-1]

    assert ec._point_at(n) == ec._pt_i

    print("test_point_at passed")

def test_generate_key():
    importlib.reload(ec)
    d, Q = ec.generate_key()
    pt = ec._fast_point_at(d)
    assert pt == Q

    print("test_generate_key passed")

if __name__ == "__main__":
    main()