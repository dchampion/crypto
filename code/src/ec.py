import euclid
import primes
import math
import prng

# secp256k1 elliptic curve parameters (y**2 = x**3 + ax + b % p)
_p = 2**256 - 2**32 - 977
_a = 0
_b = 7
_Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
_Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
_G = [_Gx, _Gy]
_n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
_h = 1

# Point at infinity
_pt_i = [0, 0]

# Global curve point X and Y list indices.
X = 0
Y = 1

def new_curve(p, a, b, Gx, Gy, n, h, B_iters=100):
    """
    Redefines the default (secp256k1) elliptic curve parameters, and validates
    the new ones.
    """
    global _p, _a, _b, _Gx, _Gy, _n, _h, _G

    _p, _a, _b, _Gx, _Gy, _n, _h = p, a, b, Gx, Gy, n, h
    _G = [_Gx, _Gy]

    validate_curve_params(B_iters)

def add(pt):
    """
    Returns the sum of the supplied point pt and the generator _G. If
    pt[X] == _Gx, or pt == [0, 0] (i.e., the point at infinity), returns
    [0, 0].
    """
    validate_pt(pt)

    if pt == _G:
        return double(pt)
    elif pt[X] == _Gx or pt == _pt_i:
        return _pt_i
    else:
        slope = ((pt[Y] - _Gy) * euclid.inverse((pt[X] - _Gx) % _p, _p)) % _p
        x = (slope**2 - (pt[X] + _Gx)) % _p
        y = ((slope * pt[X]) - (slope * x) - pt[Y]) % _p

    return [x, y]

def double(pt):
    """
    Returns the sum of supplied point pt with itself. If pt == [0, 0] (i.e.,
    the point at infinity), returns [0, 0].
    """
    validate_pt(pt)

    if pt == _pt_i:
        return pt

    slope = (((3 * pt[X]**2) + _a) * euclid.inverse(2 * pt[Y], _p)) % _p
    x = (slope**2 - (2 * pt[X])) % _p
    y = ((slope * pt[X]) - (slope * x) - pt[Y]) % _p

    return [x, y]

def generate_key():
    """
    Returns a randomly generated private key d in the range 1 <= d < _n, where
    _n is the order of the generator _G; and the point on the curve resulting
    from d point additions of _G.
    """
    d = _n
    while d < 1 or d >= _n:
        d = prng.randbits(_n.bit_length())

    return d, fast_point_at(d)

def fast_point_at(d):
    """
    Returns the point pt at d point-additions of the generator point _G, where
    d is in the range 1 <= d < _n, and _n is the order of _G. In contrast with
    point_at, this function runs in O(log2(n)) (logarithmic) time.
    """
    assert isinstance(d, int)
    assert 0 < d <= _n

    pt = _G
    for i in range(d.bit_length()-2, -1, -1):
        pt = double(pt)
        if (d>>i) & 1:
            pt = add(pt)

    return pt

def point_at(d):
    """
    Returns the point pt at d point-additions of the generator point _G, where
    d is in the range 1 <= d < _n, and _n is the order of _G. In contrast with
    fast_point_at, this function runs in O(n) (linear) time.
    """
    assert isinstance(d, int)
    assert 0 < d <= _n

    pt = _G
    for _ in range(1, d):
        pt = add(pt)

    return pt

def validate_pt(pt):
    assert isinstance(pt[X], int) and pt[X] >= 0
    assert isinstance(pt[Y], int) and pt[Y] >= 0

def validate_curve_params(B_iters=100):
    """
    Recommended curve parameter validation from the Standards for Efficient
    Cryptography Group's (SECG) specification, "SEC 1: Elliptic Curve Cryptography,
    Version 2.0" (https://www.secg.org/), section 3.1.1.2.1 (Elliptic Curve Domain
    Parameters over Fp Validation Primitive).
    """
    assert 0 <= B_iters <= 100
    assert 0 <= _a  <= _p - 1
    assert 0 <  _b  <= _p - 1 # _b cannot be zero if we want to represent _pt_i as [0,0].
    assert 0 <= _Gx <= _p - 1
    assert 0 <= _Gy <= _p - 1
    assert _n != _p
    assert (4*(_a**3) + 27*(_b**2)) % _p != 0
    assert _Gy**2 % _p == (_Gx**3 + _a*_Gx + _b) % _p
    assert primes.is_prime(_p)
    assert primes.is_prime(_n)

    t = _p.bit_length() // 2
    assert _h <= 2**(t // 8)

    assert _h == math.floor((math.sqrt(_p)+1)**2 // _n)
    assert fast_point_at(_n) == _pt_i

    # Test to exclude curves with susceptibility to MOV, FR or SSSA attacks.
    # B_iters should be 100 (the default) for cryptographically strong curves.
    for B in range(1, B_iters):
        assert _p**B % _n != 1