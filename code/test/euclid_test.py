import path_resolver
import euclid
import math

def main():
    print("Running euclid tests...")
    test_swap()
    test_gcd()
    test__gcd()
    test_gcdx()
    test__gcdx()
    test_lcm()
    test_inverse()
    print("all euclid tests passed")

def test_swap():
    a, b = euclid.swap(1,2)
    assert b > a, f"expected {b} > {a}, got {a} > {b}"

    a, b = euclid.swap(2,1)
    assert b > a, f"expected {b} > {a}, got {a} > {b}"

    a, b = euclid.swap(2,2)
    assert b == a, f"expected {a} == {b}, got {a} != {b}"

    print("swap tests passed")

def test_gcd():
    a = euclid.gcd(7,60)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(60,7)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(3,26)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(26,3)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(7,997)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(997,7)
    assert a == 1, f"expected 1, got {a}"

    a = euclid.gcd(8,60)
    assert a == 4, f"expected 4, got {a}"

    a = euclid.gcd(60,8)
    assert a == 4, f"expected 4, got {a}"

    print("gcd tests passed")

def test__gcd():
    a = euclid._gcd(7,60)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(60,7)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(3,26)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(26,3)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(7,997)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(997,7)
    assert a == 1, f"expected 1, got {a}"

    a = euclid._gcd(8,60)
    assert a == 4, f"expected 4, got {a}"

    a = euclid._gcd(60,8)
    assert a == 4, f"expected 4, got {a}"

    print("_gcd tests passed")

def test_gcdx():
    a, x, y = euclid.gcdx(7,60)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = euclid.gcdx(60,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = euclid.gcdx(3,26)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = euclid.gcdx(26,3)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = euclid.gcdx(7,997)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = euclid.gcdx(997,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = euclid.gcdx(8,60)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    a, x, y = euclid.gcdx(60,8)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    print("gcdx tests passed")

def test__gcdx():
    a, x, y = euclid._gcdx(7,60)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = euclid._gcdx(60,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = euclid._gcdx(3,26)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = euclid._gcdx(26,3)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = euclid._gcdx(7,997)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = euclid._gcdx(997,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = euclid._gcdx(8,60)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    a, x, y = euclid._gcdx(60,8)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    print("_gcdx tests passed")

def test_lcm():
    assert euclid.lcm(9,2) == math.lcm(9,2), f"expected {math.lcm(9,2)}, got {euclid.lcm(9,2)}"
    assert euclid.lcm(2,9) == math.lcm(2,9), f"expected {math.lcm(2,9)}, got {euclid.lcm(2,9)}"
    assert euclid.lcm(2,9) == math.lcm(9,2), f"expected {math.lcm(9,2)}, got {euclid.lcm(2,9)}"
    assert euclid.lcm(9,2) == math.lcm(2,9), f"expected {math.lcm(9,2)}, got {euclid.lcm(9,2)}"
    assert euclid.lcm(887083423,3499734995) == math.lcm(887083423,3499734995),\
        f"expected {math.lcm(887083423,3499734995)}, got {euclid.lcm(887083423,3499734995)}"
    assert euclid.lcm(3499734995,887083423) == math.lcm(3499734995,887083423),\
        f"expected {math.lcm(3499734995,887083423)}, got {euclid.lcm(3499734995,887083423)}"
    assert euclid.lcm(3499734995,887083423) == math.lcm(887083423,3499734995),\
        f"expected {math.lcm(887083423,3499734995)}, got {euclid.lcm(3499734995,887083423)}"
    assert euclid.lcm(887083423,3499734995) == math.lcm(3499734995,887083423),\
        f"expected {math.lcm(3499734995,887083423)}, got {euclid.lcm(887083423,3499734995)}"

    print("lcm tests passed")

def test_inverse():
    a = euclid.inverse(60,7)
    assert a == 2,    f"expected 2, got {a}"
    
    a = euclid.inverse(7,60)
    assert a == 43,   f"expected 43, got {a}"

    a = euclid.inverse(26,3)
    assert a == 2,    f"expected 2, got {a}"

    a = euclid.inverse(3,26)
    assert a == 9,    f"expected 9, got {a}"

    a = euclid.inverse(997,7)
    assert a == 5,    f"expected 5, got {a}"

    a = euclid.inverse(7,997)
    assert a == 285,  f"expected 285, got {a}"

    try:
        euclid.inverse(60,8)
        assert False, "Expected inverse(60,8) to raise an exeption, but didn't"
    except Exception as e:
        assert isinstance(e, ValueError)

    print("inverse tests passed")

if __name__ == "__main__":
    main()