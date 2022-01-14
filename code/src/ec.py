import euclid

# secp256k1 elliptic curve parameters (y**2 = x**3 + ax + b % p)
p = 2**256 - 2**32 - 977
a = 0
b = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = [Gx, Gy]
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1

T = (p, a, b, G, n, h)

X = 0
Y = 1

def new_curve(p1, a1, b1, Gx1, Gy1, n1, h1):
    global p, a, b, Gx, Gy, G, n, h
    p, a, b, Gx, Gy, n, h = p1, a1, b1, Gx1, Gy1, n1, h1
    G = [Gx, Gy]

def add(pt):
    if pt == G:
        slope = (((3 * pt[X]**2) + a) * euclid.inverse(2 * Gy, p)) % p
        x = (slope**2 - (2 * Gx)) % p
        y = ((slope * Gx) - (slope * x) - Gy) % p
    elif pt[X] == Gx:
        x, y = 0, 0
    else:
        slope = ((pt[Y] - Gy) * euclid.inverse(pt[X] - Gx, p)) % p
        x = (slope**2 - (pt[X] + Gx)) % p
        y = ((slope * pt[X]) - (slope * x) - pt[Y]) % p

    return x, y