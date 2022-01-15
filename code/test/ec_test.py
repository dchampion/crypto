import sys
sys.path.append("../src")

import ec

# Test curve parameters
p = 17
a = 2
b = 2
Gx = 5
Gy = 1
n = 19
h = 1

pt_group = [[5,1],[6,3],[10,6],[3,1],[9,16],[16,13],[0,6],[13,7],[7,6],
            [7,11],[13,10],[0,11],[16,4],[9,1],[3,16],[10,11],[6,14],[5,16],[0,0]]

def main():
    print("Running ec tests...")
    test_add()
    test_double()
    print("all ec tests passed")

def test_add():
    ec.new_curve(p, a, b, Gx, Gy, n, h)
    for i in range(1, len(pt_group)):
        pt = ec.add(pt_group[i-1])
        assert pt == pt_group[i]

    print("test_ec_add passed")

def test_double():
    ec.new_curve(p, a, b, Gx, Gy, n, h)
    for i in range(1, len(pt_group)):
        pt = ec.double(pt_group[i-1])
        assert pt == pt_group[((i*2)%n)-1]

    print("test_ec_double passed")

if __name__ == "__main__":
    main()