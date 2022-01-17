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

# Global curve point X and Y list indices.
X = 0
Y = 1

def new_curve(p, a, b, Gx, Gy, n, h, B_iters=100):
    """
    Redefines and validates the default (secp256k1) elliptic curve.
    """
    global _p, _a, _b, _Gx, _Gy, _n, _h, _G
    _p, _a, _b, _Gx, _Gy, _n, _h = p, a, b, Gx, Gy, n, h
    _G = [_Gx, _Gy]
    validate_curve_params(B_iters)

def add(pt):
    """
    Returns the sum of the supplied point pt and the generator point _G; or,
    if pt[X] == _Gx, pt itself.
    """
    if pt == _G:
        [x, y] = double(pt)
    elif pt[X] != _Gx:
        [x, y] = _add(pt)
    else:
        [x, y] = pt #TODO: What here?

    return [x, y]

def _add(pt):
    """
    Returns the sum of the supplied point pt and the generator point _G.
    TODO: What happens if we pass this the identity element?
    """
    slope = ((pt[Y] - _Gy) * euclid.inverse((pt[X] - _Gx) % _p, _p)) % _p
    x = (slope**2 - (pt[X] + _Gx)) % _p
    y = ((slope * pt[X]) - (slope * x) - pt[Y]) % _p

    return [x, y]

def double(pt):
    """
    Returns the sum of the supplied point pt added to itself.
    """
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
    pt = _G
    for i in range(0, d):
        pt = add(pt)

    return d, pt

def validate_curve_params(B_iters=100):
    """
    Recommended curve parameter validation from the Standards for Efficient
    Cryptography Group's (SECG) specification, "SEC 1: Elliptic Curve Cryptography,
    Version 2.0" (https://www.secg.org/), section 3.1.1.2.1 (Elliptic Curve Domain
    Parameters over Fp Validation Primitive).
    """
    assert 0 <= B_iters <= 100
    assert 0 <= _a <= _p - 1
    assert 0 <= _b <= _p - 1
    assert _n != _p
    assert (4*(_a**3) + 27*(_b**2)) % _p != 0
    assert _Gy**2 % _p == (_Gx**3 + _a*_Gx + _b) % _p
    assert primes.is_prime(_p)
    assert primes.is_prime(_n)

    log2_p = math.ceil(math.log2(_p))
    assert _h <= 2**(log2_p//8)

    sqrt_p = math.sqrt(_p)
    assert _h == math.floor((sqrt_p+1)**2//_n)

    # Test to exclude curves with susceptibility to MOV, FR or SSSA attacks.
    # B_iters should be 100 (the default) for cryptographically strong curves.
    for B in range(1, B_iters):
        assert _p**B % _n != 1