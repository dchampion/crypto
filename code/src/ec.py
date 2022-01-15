import euclid

# secp256k1 elliptic curve parameters (y**2 = x**3 + ax + b % p)
_p = 2**256 - 2**32 - 977
_a = 0
_b = 7
_Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
_Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
_G = [_Gx, _Gy]
_n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
_h = 1

X = 0
Y = 1

def new_curve(p, a, b, Gx, Gy, n, h):
    global _p, _a, _b, _Gx, _Gy, _G, _n, _h
    _p, _a, _b, _Gx, _Gy, _n, _h = p, a, b, Gx, Gy, n, h
    _G = [_Gx, _Gy]

def add(pt):
    if pt == _G:
        [x, y] = double(pt)
    elif pt[X] != _Gx:
        [x, y] = _add(pt)
    else:
        [x, y] = [0, 0]

    return [x, y]

def _add(pt):
    slope = ((pt[Y] - _Gy) * euclid.inverse((pt[X] - _Gx) % _p, _p)) % _p
    x = (slope**2 - (pt[X] + _Gx)) % _p
    y = ((slope * pt[X]) - (slope * x) - pt[Y]) % _p

    return [x, y]

def double(pt):
    slope = (((3 * pt[X]**2) + _a) * euclid.inverse(2 * pt[Y], _p)) % _p
    x = (slope**2 - (2 * pt[X])) % _p
    y = ((slope * pt[X]) - (slope * x) - pt[Y]) % _p

    return [x, y]
