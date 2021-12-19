""" Implementations of the simple and extended Euclidean algorithms. """
import math

def main():
    print("Running tests...")
    ### Begin tests for swap
    a, b = swap(1,2)
    assert b > a, f"expected {b} > {a}, got {a} > {b}"
    
    a, b = swap(2,1)
    assert b > a, f"expected {b} > {a}, got {a} > {b}"
    
    a, b = swap(-2,4)
    assert b > a, f"expected {b} > {a}, got {a} > {b}"
    
    a, b = swap(2,2)
    assert b == a, f"expected {a} == {b}, got {a} != {b}"
    
    print("swap tests passed")
    ### End tests for swap

    ### Begin tests for gcd
    a = gcd(7,60)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(60,7)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(3,26)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(26,3)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(7,997)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(997,7)
    assert a == 1, f"expected 1, got {a}"

    a = gcd(8,60)
    assert a == 4, f"expected 4, got {a}"

    a = gcd(60,8)
    assert a == 4, f"expected 4, got {a}"

    print("gcd tests passed")
    ### End tests for gcd

    ### Begin tests for _gcd
    a = _gcd(7,60)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(60,7)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(3,26)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(26,3)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(7,997)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(997,7)
    assert a == 1, f"expected 1, got {a}"

    a = _gcd(8,60)
    assert a == 4, f"expected 4, got {a}"

    a = _gcd(60,8)
    assert a == 4, f"expected 4, got {a}"

    print("_gcd tests passed")
    ### End tests for _gcd

    ### Begin tests for gcdx
    a, x, y = gcdx(7,60)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = gcdx(60,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = gcdx(3,26)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = gcdx(26,3)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = gcdx(7,997)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = gcdx(997,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = gcdx(8,60)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    a, x, y = gcdx(60,8)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    print("gcdx tests passed")
    ### End tests for gcdx

    ### Begin tests for _gcdx
    a, x, y = _gcdx(7,60)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = _gcdx(60,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == -17, f"expected -17, got {x}"
    assert y == 2,   f"expected 2, got {y}"

    a, x, y = _gcdx(3,26)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = _gcdx(26,3)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 9,   f"expected 9, got {x}"
    assert y == -1,  f"expected -1, got {y}"

    a, x, y = _gcdx(7,997)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = _gcdx(997,7)
    assert a == 1,   f"expected 1, got {a}"
    assert x == 285, f"expected 285, got {x}"
    assert y == -2,  f"expected -2, got {y}"

    a, x, y = _gcdx(8,60)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    a, x, y = _gcdx(60,8)
    assert a == 4,  f"expected 4, got {a}"
    assert x == -7, f"expected -7, got {x}"
    assert y == 1,  f"expected 1, got {y}"

    print("_gcdx tests passed")
    ### End tests for _gcdx

    ### Begin tests for lcm
    assert lcm(9,2) == math.lcm(9,2), f"expected {math.lcm(9,2)}, got {lcm(9,2)}"
    assert lcm(2,9) == math.lcm(2,9), f"expected {math.lcm(2,9)}, got {lcm(2,9)}"
    assert lcm(2,9) == math.lcm(9,2), f"expected {math.lcm(9,2)}, got {lcm(2,9)}"
    assert lcm(9,2) == math.lcm(2,9), f"expected {math.lcm(9,2)}, got {lcm(9,2)}"
    assert lcm(887083423,3499734995) == math.lcm(887083423,3499734995),\
        f"expected {math.lcm(887083423,3499734995)}, got {lcm(887083423,3499734995)}"
    assert lcm(3499734995,887083423) == math.lcm(3499734995,887083423),\
        f"expected {math.lcm(3499734995,887083423)}, got {lcm(3499734995,887083423)}"
    assert lcm(3499734995,887083423) == math.lcm(887083423,3499734995),\
        f"expected {math.lcm(887083423,3499734995)}, got {lcm(3499734995,887083423)}"
    assert lcm(887083423,3499734995) == math.lcm(3499734995,887083423),\
        f"expected {math.lcm(3499734995,887083423)}, got {lcm(887083423,3499734995)}"
    print("lcm tests passed")
    ### End tests for lcm

    ### Begin tests for inverse
    a = inverse(60,7)
    assert a == 2,    f"expected 2, got {a}"
    
    a = inverse(7,60)
    assert a == 43,   f"expected 43, got {a}"

    a = inverse(26,3)
    assert a == 2,    f"expected 2, got {a}"

    a = inverse(3,26)
    assert a == 9,    f"expected 9, got {a}"

    a = inverse(997,7)
    assert a == 5,    f"expected 5, got {a}"

    a = inverse(7,997)
    assert a == 285,  f"expected 285, got {a}"

    try:
        inverse(60,8)
        raise Exception("Expected inverse(60,8) to raise an exeption, but didn't")
    except Exception as e:
        print(e)

    print("inverse tests passed")
    ### End tests for inverse

def swap(a, b):
    """ Returns a and b in increasing order from left-to-right. """
    if a > b:
        return b, a
    return a, b

def gcd(a, b):
    """ Returns the greatest common divisor (or gcd) of a and b. """

    assert a >= 0 and b >= 0

    while b != 0:
        a, b = swap(a, b)
        b = b % a

    return a

def _gcd(a, b):
    """
    Returns the greatest common divisor (or gcd) of a and b. Note
    this function uses recursion, which can cause stack overflow if
    its inputs a and/or b are too large. A safer alternative is to
    use gcd(a,b) instead.
    """
    assert a >= 0 and b >= 0

    if b == 0:
        return a
    
    a, b = swap(a, b)

    return gcd(a, b % a)

def gcdx(a, b):
    """
    Returns the greatest common divisor (or gcd) of a and b, and the
    x and y solutions for the relation ax = bx = gcd(a,b) (see Bezout's
    identity).
    """
    assert a >= 0 and b >= 0

    a, b = swap(a, b)

    a1, b1, x1, y1 = 1, 0, 1, 0
    while b != 0:
        q = a // b
        temp = b

        b = a - q * b
        a = temp

        temp = a1
        a1 = y1 - q * a1
        y1 = temp

        temp = b1
        b1 = x1 - q * b1
        x1 = temp

    return a, x1, y1

def _gcdx(a, b):
    """
    Returns the greatest common divisor (or gcd) of a and b, and the
    x and y solutions for the relation ax = bx = gcd(a,b) (see Bezout's
    identity). Note this function uses recursion, which can cause stack
    overflow if its inputs a and/or b are too large. A safer alternative
    is to use gcdx(a,b) instead.
    """
    assert a >= 0 and b >= 0

    if b == 0:
        return a, 0, 1
    
    a, b = swap(a, b)

    gcd, x1, y1 = gcdx(a, b % a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

def lcm(a, b):
    """ Returns the least common multiple (or lcm) of a and b. """
    assert a >= 0 and b >= 0

    return (a*b) // gcd(a, b)

def inverse(a, b):
    """
    Returns the modular multiplicative inverse of a modulo b;
    if no such inverse exists, raises an exception.
    """
    assert a >= 0 and b >= 0

    gcd, x, y = gcdx(a, b)
    if gcd != 1:
        err_str = f"{a} has no inverse modulo {b}."
        raise Exception(err_str)
    
    inverse = x if a < b else y

    return (inverse % b + b) % b

if __name__ == "__main__":
    main()