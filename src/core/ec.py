"""
Implementations of the elliptic curve Diffie-Hellman (ECDH) and the elliptic
curve digital signature algorithms (ECDSA).
"""

from . import curves
from . import euclid
from . import primes
from . import prng
from . import util

import math

# Identity element, aka the "point at infinity."
_i = [None, None]

# Global curve point [_X, _Y] list indices.
_X = 0
_Y = 1

# Default curve is secp256k1.
_curve = curves.Secp256k1()

def new_curve(curve: curves.Curve, B_iters: int=100) -> None:
    """
    Given a curve (either one selected from the "curves" module of this package,
    or one that is user-defined), redefines this module's default elliptic curve
    (secp256k1) and validates the new curve's parameters.
    """

    global _curve
    _curve = curve
    _validate_curve_params(B_iters)

def _add(pt1: list[int], pt2: list[int]) -> list[int]:
    # Returns the sum of points pt1 and pt2 on the curve, according to the addition
    # rules of elliptic curves; i.e., (a) the identity element if pt1 and pt2 are
    # both the the identity element, (b) pt2 if pt1 is the identity element, (c) pt1
    # if pt2 is the identity element, (d) the identity element if pt1 and pt2 share
    # the same x-coordinate, or (e) the sum of pt1 and pt2 on the curve.

    _validate_pt(pt1)
    _validate_pt(pt2)

    if pt1 == _i and pt2 == _i:
        [x, y] = _i
    elif pt1 == _i:
        [x, y] = pt2
    elif pt2 == _i:
        [x, y] = pt1
    elif pt1 == pt2:
        [x, y] = _double(pt1)
    elif pt1[_X] == pt2[_X]:
        [x, y] = _i
    else:
        [x, y] = _additive_inverse(_secant_intersection(pt1, pt2))
    
    return [x, y]

def _double(pt: list[int]) -> list[int]:
    # Returns the sum of point pt with itself on the curve. If pt is the point at
    # infinity, returns the point at infinity.

    _validate_pt(pt)

    if pt == _i:
        return pt

    return _additive_inverse(_tangent_intersection(pt))

def _additive_inverse(pt: list[int]) -> list[int]:
    # Returns the additive inverse of pt, where pt is of the form [x, y], and pt's
    # inverse is [x, -y].

    return [pt[_X], -pt[_Y] % _curve.p]

def _tangent_intersection(pt: list[int]) -> list[int]:
    # Returns the point of intersection on the curve of a straight line drawn tangent
    # to the point pt on the curve. For a thorough explanation of the arithmetic used in
    # this function, consult the following URL:
    # https://nbviewer.org/github/dchampion/crypto/blob/master/doc/EllipticCurves.ipynb

    m = (((3 * pt[_X]**2) + _curve.a) * euclid.inverse(2 * pt[_Y], _curve.p)) % _curve.p
    pt2x = (m**2 - (2 * pt[_X])) % _curve.p
    pt2y = (m * (pt2x - pt[_X])) + pt[_Y] % _curve.p

    return [pt2x, pt2y]

def _secant_intersection(pt1: list[int], pt2: list[int]) -> list[int]:
    # Returns the point of intersection on the curve of a straight line drawn between
    # points pt1 and pt2 (i.e., the secant line) on the curve. For a thorough explanation
    # of the arithmetic used in this function, consult the following URL:
    # https://nbviewer.org/github/dchampion/crypto/blob/master/doc/EllipticCurves.ipynb

    m = ((pt2[_Y] - pt1[_Y]) * euclid.inverse((pt2[_X] - pt1[_X]) % _curve.p, _curve.p)) % _curve.p
    pt3x = (m**2 - pt1[_X] - pt2[_X]) % _curve.p
    pt3y = (m * (pt3x - pt1[_X]) + pt1[_Y]) % _curve.p

    return [pt3x, pt3y]

def generate_keypair() -> tuple[int, list[int]]:
    """
    Returns a tuple of the form (d, Q), where d is a private key and Q its
    corresponding public key. d is a randomly generated positive integer in the
    range 1 <= d < n (where n is the order of the base point), and Q is the point
    on the curve resulting from d point-additions of the base point. The private
    key must be kept secret by the caller of this function; whereas the public key
    may be shared freely.
    """

    d = _curve.n
    while not _validate_priv_key(d):
        d = prng.randbits(_curve.n.bit_length())

    return d, _fast_point_at(d)

def generate_session_key(d: int, Q: list[int]) -> bytes:
    """
    Given a keypair, consisting of the caller's private key d and another party's
    public key Q, returns a byte array suitable for use as a session key in a symmetric
    cipher (e.g., AES, 3DES) used to encrypt messages transmitted between the caller and
    the other party. The session key returned by this function must be kept secret.
    """

    assert _validate_priv_key(d)
    validate_pub_key(Q)

    # Compute a shared point on the curve using the essential property of Diffie-
    # Hellman. In the case of elliptic curves, this is done by multiplying the
    # other party's public key Q by the caller's private key d.
    k_pt = _x_times_pt(d, Q)

    # Use only the x-coordinate of the shared point in the shared key, and hash it
    # to obscure any mathematical structure that could be exploited by an adversary
    # if it were to be leaked.
    return util.hash(k_pt[_X])

def sign(d: int, m: any) -> tuple[int, int]:
    """
    Returns a tuple of the form (r, s), which comprises the signature of the message m
    using the caller's private key d. Receivers of this signature can verify the message's
    authenticity using this module's verify function.
    """

    assert _validate_priv_key(d)

    s = 0
    while s == 0:
        r = 0
        while r == 0:
            # k is the ephemeral (i.e., one-time use) key.
            k, R = generate_keypair()
            assert 0 <= R[_X] < _curve.p

            # r is the x-coordinate of R; the first element of the tuple (r, s)
            # returned by this function (try again if r is 0).
            r = R[_X] % _curve.n

        # Convert m to an integer representative of its hash.
        e = _hash_to_int(m)

        # Compute the second element of the tuple (r, s) returned by this function
        # (try again if s is 0).
        s = (euclid.inverse(k, _curve.n) * (e + d * r)) % _curve.n

    return r, s

def verify(Q: list[int], m: any, S: tuple[int, int]) -> bool:
    """
    Returns True if the signature S, a tuple of the form (r, s) that is returned
    by this module's sign function, is valid for the message m and a public key Q;
    otherwise returns False.
    """

    validate_pub_key(Q)

    r, s = S[0], S[1]

    # TODO: These should raise exceptions, not assert (see Java psychic-signature vulnerability).
    assert 1 <= r <_curve.n
    assert 1 <= s < _curve.n

    # Convert m to an integer representative of its hash.
    e = _hash_to_int(m)

    s_inv = euclid.inverse(s, _curve.n)
    u1 = (e * s_inv) % _curve.n
    u2 = (r * s_inv) % _curve.n

    # Recover the point computed in the signing operation.
    R = _add(_x_times_pt(u1, _curve.G), _x_times_pt(u2, Q))
    assert R != _i

    v = R[_X] % _curve.n

    # Proof of correctness:
    #      v = u1 x _G + u2 x Q
    #      v = u1 x _G + u2 x d x _G             (expand Q to d x _G)
    #      v = s^-1 x e x _G + u2 x d x _G       (expand u1 to s^-1 x e)
    #      v = s^-1 x e x _G + s^-1 x r x d x _G (expand u2 to s^-1 x r)
    #      v = s^-1(e + r x d) x _G              (distribute s^-1 over addition)
    # k x _G = s^-1(e + r x d) x _G              (expand v to k x _G)
    #      k = s^-1(e + r x d)                   (divide both sides by _G)
    #  s x k = (e + r x d)                       (multiply both sides by s)
    #      s = k^-1(e + r x d)                   (divide both sides by k,
    #                                             and we recover 's' from sign function)

    return v == r

def _hash_to_int(m: any) -> int:
    # Converts a message m to an integer representation of its hash.

    h = util.hash(m)
    i = int.from_bytes(h, byteorder="big")

    if _curve.n.bit_length() >= i.bit_length():
        e = i
    else:
        # Use only the leftmost _n bits if _n is smaller than m.
        e = i >> (i.bit_length() - _curve.n.bit_length())

    return e

def _fast_point_at(d: int) -> list[int]:
    # Returns the point on the curve at d point-additions of the base point, where
    # d is a positive integer in the range 1 <= d < n, and n is the order of the
    # base point. In contrast with the function _point_at, this function runs in
    # logarithmic time.

    assert isinstance(d, int) and 0 < d <= _curve.n

    return _x_times_pt(d, _curve.G)

def _x_times_pt(x: int, pt: list[int]) -> list[int]:
    # Returns the point on the curve at x point-additions of the start point pt.

    _validate_pt(pt)
    assert isinstance(x, int) and x > 0

    start_pt = pt
    for i in range(x.bit_length()-2, -1, -1):
        pt = _double(pt)
        if (x>>i) & 1:
            pt = _add(start_pt, pt)

    return pt

def _point_at(d: int) -> list[int]:
    # Returns the point on the curve at d point-additions of the base point, where
    # d is a positive integer in the range 1 <= d < n, and n is the order of the
    # base point. In contrast with the function _fast_point_at, this function runs
    # in linear time.

    assert isinstance(d, int) and 0 < d <= _curve.n

    pt = _curve.G
    for _ in range(1, d):
        pt = _add(_curve.G, pt)

    return pt

def _validate_pt(pt: list[int]) -> None:
    # pt must be a 2-element list.

    assert isinstance(pt, list) and len(pt) == 2

    # pt's types must match.
    assert type(pt[_X]) == type(pt[_Y])

    if isinstance(pt[_X], int):
        # If pt is purported to be a point on the curve, prove that it is.
        assert _on_curve(pt)
    else:
        # If pt's elements are not of type int, then they must be of type None.
        assert pt[_X] == None and pt[_Y] == None

def _on_curve(pt: list[int]) -> bool:
    # Returns True if the point pt is on the curve; otherwise returns False.

    return pt[_Y]**2 % _curve.p == (pt[_X]**3 + (_curve.a*pt[_X]) + _curve.b) % _curve.p

def _validate_priv_key(d: int) -> None:
    # Private keys must fall in the range 1 <= d < n

    return isinstance(d, int) and 1 <= d < _curve.n

def validate_pub_key(Q: list[int]) -> None:
    """
    Recommended public key validation from the Standards for Efficient Cryptography
    Group's (SECG) specification, "SEC 1: Elliptic Curve Cryptography, Version 2.0"
    (https://www.secg.org/), section 3.2.2.1 (Elliptic Curve Public Key Validation
    primitive).
    """
    _validate_pt(Q)

    valid = True

    # Q must not be the identity element.
    if valid and Q == _i:
        valid = False

    # Q's x coordinate must be in the interval [0, p-1].
    if valid and Q[_X] > _curve.p-1 or Q[_X] < 0:
        valid = False

    # Q's y coordinate must be in the interval [0, p-1].
    if valid and Q[_Y] > _curve.p-1 or Q[_Y] < 0:
        valid = False

    # Q must be on the curve
    if valid and not _on_curve(Q):
        valid = False

    # If the cofactor h is greater than 1, then the order of the group n times Q must
    # equal the identity element.
    if valid and _curve.h > 1 and _x_times_pt(_curve.n, Q) != _i:
        valid = False

    if not valid:
        raise ValueError("Invalid public key")

def _validate_curve_params(B_iters: int=100) -> None:
    # Recommended curve parameter validation from the Standards for Efficient Cryptography
    # Group's (SECG) specification, "SEC 1: Elliptic Curve Cryptography, Version 2.0"
    # (https://www.secg.org/), section 3.1.1.2.1 (Elliptic Curve Domain Parameters over
    # Fp Validation Primitive).

    valid = True

    # a must be a group element; i.e., within the interval [0, p-1].
    if valid and _curve.a > _curve.p - 1 or _curve.a < 0:
        valid = False

    # b must be a group element; i.e., within the interval [0, p-1].
    if valid and _curve.b > _curve.p - 1 or _curve.b < 0:
        valid = False

    # Gx must be a group element; i.e., within the interval [0, p-1].
    if valid and _curve.Gx > _curve.p - 1 or _curve.Gx < 0:
        valid = False

    # Gy must be a group element; i.e., within the interval [0, p-1].
    if valid and _curve.Gy > _curve.p - 1 or _curve.Gy < 0:
        valid = False

    # n must not equal p.
    if valid and _curve.n == _curve.p:
        valid = False

    # The curve must be smooth.
    if valid and (4*(_curve.a**3) + 27*(_curve.b**2)) % _curve.p == 0:
        valid = False

    # The base point G must be on the curve.
    if valid and not _on_curve(_curve.G):
        valid = False

    # p must be prime.
    if valid and not primes.is_prime(_curve.p):
        valid = False

    # n must be prime.
    if valid and not primes.is_prime(_curve.n):
        valid = False

    # n additions of the base point G must yield the identity element _i.
    if valid and _fast_point_at(_curve.n) != _i:
        valid = False

    # The following two tests are for the cofactor h.
    if valid and _curve.h != (math.sqrt(_curve.p)+1)**2 // _curve.n:
        valid = False

    if valid and _curve.h > 2**((_curve.p.bit_length() // 2) // 8):
        valid = False

    # Check that the curve is not susceptible to the MOV, FR or SSSA attacks
    # (B_iters should be 100 (the default) for cryptographically strong curves).
    if valid and B_iters < 1:
        valid = False
    else:
        for B in range(1, B_iters):
            if _curve.p**B % _curve.n == 1:
                valid = False

    if not valid:
        raise ValueError("Invalid curve")