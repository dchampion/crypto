"""
Implementations of the elliptic curve Diffie-Hellman (ECDH) and the elliptic
curve digital signature algorithms (ECDSA).
"""

import math

from . import curves
from . import euclid
from . import primes
from . import prng
from . import util

# Identity element, aka the "point at infinity."
_I = [None, None]

# Global curve point [_X, _Y] list indices.
_X = 0
_Y = 1

# Default curve is secp256k1.
_CURVE = curves.Secp256k1()

class ECPoint(object):
    """
    A class representing an elliptic curve point. Do not instantiate this
    class directly; instead use the ec module function make_point().
    """
    def __init__(self, x: int | None, y: int | None):
        _validate_pt([x, y])
        self._x = x
        self._y = y

    @property
    def x(self) -> int | None:
        """The x-coordinate of this point."""
        return self._x

    @property
    def y(self) -> int | None:
        """The y-coordinate of this point."""
        return self._y

    def double(self):
        """Return the doubled value of this point (i.e., 2*point)."""
        doubled = _double(self._as_list())
        return ECPoint(doubled[_X], doubled[_Y])

    def _as_list(self) -> list:
        # Return this point as a 2-member list consumable by the module
        # API.
        return [self._x, self._y]

    def __add__(self, other):
        if not isinstance(other, ECPoint):
            return NotImplemented
        sum = _add(self._as_list(), other._as_list())
        return ECPoint(sum[_X], sum[_Y])

    def __iadd__(self, other):
        if not isinstance(other, ECPoint):
            return NotImplemented
        self = self.__add__(other)
        return self

    def __mul__(self, n: int):
        if not isinstance(n, int):
            return NotImplemented
        product = _x_times_pt(n, self._as_list())
        return ECPoint(product[_X], product[_Y])

    def __imul__(self, n: int):
        if not isinstance(n, int):
            return NotImplemented
        self = self.__mul__(n)
        return self

    def __rmul__(self, lhs):
        return self.__mul__(lhs)

    def __str__(self):
        return f"x={self._x}, y={self._y}"

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __ne__(self, other):
        return not self == other

class ECKey(object):
    """
    A class representing an elliptic curve keypair. Do not instantiate
    this class directly; instead use the ec module function make_key().
    """
    def __init__(self, d: int, Q: ECPoint):
        _validate_priv_key(d)
        validate_pub_key(Q._as_list())
        self._d = d
        self._Q = Q

    @property
    def d(self) -> int:
        """
        The private key of this keypair. This value should be kept secret.
        """
        return self._d

    @property
    def Q(self) -> ECPoint:
        """
        The public key of this keypair. This value can be shared freely.
        """
        return self._Q

    def make_session_key(self, Q) -> bytes:
        """
        Given a public key Q supplied by another party, returns a session
        key suitable for use in a symmetric cipher with the other party.
        This value should be kept secret.
        """
        if not isinstance(Q, ECPoint):
            raise ValueError("Q is not a curve point.")
        return generate_session_key(self._d, Q._as_list())

    def sign(self, m: object) -> tuple[int, int]:
        """
        Given a message m, returns the signature of m by this keypair's
        private key.
        """
        return sign(self._d, m)

    def verify(self, Q: ECPoint, m: object, S: tuple[int, int]) -> bool:
        """
        Given a public key Q, a message m and a signature S supplied by
        another party, returns True if m was signed by the private key
        corresponding to Q; otherwise returns False.
        """
        return verify(Q._as_list(), m, S)

    def public_key(self) -> ECPoint:
        """
        Returns the public key of this keypair. This value can be
        shared freely.
        """
        return self.Q

    def __eq__(self, other):
        return self._d == other._d and self._Q == other._Q

    def __hash__(self):
        return hash((self._d, self._Q))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"d={self._d}, Q=[{self._Q}]"


def make_key():
    """
    Constructs and returns an elliptic curve keypair (ECKey) for the
    currently active elliptic curve.
    """
    d, Q = generate_keypair()
    return ECKey(d, make_point(Q[_X], Q[_Y]))


def make_point(x: int | None, y: int | None) -> ECPoint:
    """
    Constructs and returns an elliptic curve point (ECPoint) on the
    currently active elliptic curve.
    """
    return ECPoint(x, y)


def base_point() -> ECPoint:
    """
    Returns the base point (ECPoint) on the currently active elliptic
    curve.
    """
    return make_point(_CURVE.Gx, _CURVE.Gy)


def id_elem() -> ECPoint:
    """
    Returns the identity element (ECPoint) of the currently active
    elliptic curve.
    """
    return make_point(None, None)


def new_curve(curve: curves.Curve, B_iters: int = 100) -> None:
    """
    Given a curve (either one selected from the "curves" module of this
    package, or one that is user-defined), redefines this module's default
    elliptic curve (secp256k1) and validates the new curve's parameters.
    """

    global _CURVE
    _CURVE = curve
    _validate_curve_params(B_iters)


def _add(pt1: list[int], pt2: list[int]) -> list[int]:
    # Returns the sum of points pt1 and pt2 on the curve, according to the addition
    # rules of elliptic curves; i.e., (a) the identity element if pt1 and pt2 are
    # both the the identity element, (b) pt2 if pt1 is the identity element, (c) pt1
    # if pt2 is the identity element, (d) the identity element if pt1 and pt2 share
    # the same x-coordinate, or (e) the sum of pt1 and pt2 on the curve.

    _validate_pt(pt1)
    _validate_pt(pt2)

    if pt1 == _I and pt2 == _I:
        [x, y] = _I
    elif pt1 == _I:
        [x, y] = pt2
    elif pt2 == _I:
        [x, y] = pt1
    elif pt1 == pt2:
        [x, y] = _double(pt1)
    elif pt1[_X] == pt2[_X]:
        [x, y] = _I
    else:
        [x, y] = _additive_inverse(_secant_intersection(pt1, pt2))

    return [x, y]


def _double(pt: list[int]) -> list[int]:
    # Returns the sum of point pt with itself on the curve. If pt is the point at
    # infinity, returns the point at infinity.

    _validate_pt(pt)

    if pt == _I:
        return pt

    return _additive_inverse(_tangent_intersection(pt))


def _additive_inverse(pt: list[int]) -> list[int]:
    # Returns the additive inverse of pt, where pt is of the form [x, y], and pt's
    # inverse is [x, -y].

    return [pt[_X], -pt[_Y] % _CURVE.p]


def _tangent_intersection(pt: list[int]) -> list[int]:
    # Returns the point of intersection on the curve of a straight line drawn tangent
    # to the point pt on the curve. For a thorough explanation of the arithmetic used in
    # this function, consult the following URL:
    # https://nbviewer.org/github/dchampion/crypto/blob/master/doc/EllipticCurves.ipynb

    m = (
        ((3 * pt[_X] ** 2) + _CURVE.a) * euclid.inverse(2 * pt[_Y], _CURVE.p)
    ) % _CURVE.p
    pt2x = (m**2 - (2 * pt[_X])) % _CURVE.p
    pt2y = (m * (pt2x - pt[_X])) + pt[_Y] % _CURVE.p

    return [pt2x, pt2y]


def _secant_intersection(pt1: list[int], pt2: list[int]) -> list[int]:
    # Returns the point of intersection on the curve of a straight line drawn between
    # points pt1 and pt2 (i.e., the secant line) on the curve. For a thorough explanation
    # of the arithmetic used in this function, consult the following URL:
    # https://nbviewer.org/github/dchampion/crypto/blob/master/doc/EllipticCurves.ipynb

    m = (
        (pt2[_Y] - pt1[_Y]) * euclid.inverse((pt2[_X] - pt1[_X]) % _CURVE.p, _CURVE.p)
    ) % _CURVE.p
    pt3x = (m**2 - pt1[_X] - pt2[_X]) % _CURVE.p
    pt3y = (m * (pt3x - pt1[_X]) + pt1[_Y]) % _CURVE.p

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

    d = _CURVE.n
    while not _validate_priv_key(d):
        d = prng.randbits(_CURVE.n.bit_length())

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
    return util.digest(k_pt[_X])


def sign(d: int, m: object) -> tuple[int, int]:
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
            assert 0 <= R[_X] < _CURVE.p

            # r is the x-coordinate of R; the first element of the tuple (r, s)
            # returned by this function (try again if r is 0).
            r = R[_X] % _CURVE.n

        # Convert m to an integer representative of its hash.
        e = _hash_to_int(m)

        # Compute the second element of the tuple (r, s) returned by this function
        # (try again if s is 0).
        s = (euclid.inverse(k, _CURVE.n) * (e + d * r)) % _CURVE.n

    return r, s


def verify(Q: list[int], m: object, S: tuple[int, int]) -> bool:
    """
    Returns True if the signature S, a tuple of the form (r, s) that is returned
    by this module's sign function, is valid for the message m and a public key Q;
    otherwise returns False.
    """

    validate_pub_key(Q)

    r, s = S[0], S[1]

    # TODO: These should raise exceptions, not assert (see Java psychic-signature vulnerability).
    assert 1 <= r < _CURVE.n
    assert 1 <= s < _CURVE.n

    # Convert m to an integer representative of its hash.
    e = _hash_to_int(m)

    s_inv = euclid.inverse(s, _CURVE.n)
    u1 = (e * s_inv) % _CURVE.n
    u2 = (r * s_inv) % _CURVE.n

    # Recover the point computed in the signing operation.
    R = _add(_x_times_pt(u1, _CURVE.G), _x_times_pt(u2, Q))
    assert R != _I

    v = R[_X] % _CURVE.n

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


def _hash_to_int(m: object) -> int:
    # Converts a message m to an integer representation of its hash.

    h = util.digest(m)
    i = util.to_int(h)

    if _CURVE.n.bit_length() >= i.bit_length():
        e = i
    else:
        # Use only the leftmost _n bits if _n is smaller than m.
        e = i >> (i.bit_length() - _CURVE.n.bit_length())

    return e


def _fast_point_at(d: int) -> list[int]:
    # Returns the point on the curve at d point-additions of the base point, where
    # d is a positive integer in the range 1 <= d < n, and n is the order of the
    # base point. In contrast with the function _point_at, this function runs in
    # logarithmic time.

    assert isinstance(d, int) and 0 < d <= _CURVE.n

    return _x_times_pt(d, _CURVE.G)


def _x_times_pt(x: int, pt: list[int]) -> list[int]:
    # Returns the point on the curve at x point-additions of the start point pt.

    _validate_pt(pt)
    assert isinstance(x, int) and x > 0

    start_pt = pt
    for i in range(x.bit_length() - 2, -1, -1):
        pt = _double(pt)
        if (x >> i) & 1:
            pt = _add(start_pt, pt)

    return pt


def _point_at(d: int) -> list[int]:
    # Returns the point on the curve at d point-additions of the base point, where
    # d is a positive integer in the range 1 <= d < n, and n is the order of the
    # base point. In contrast with the function _fast_point_at, this function runs
    # in linear time.

    assert isinstance(d, int) and 0 < d <= _CURVE.n

    pt = _CURVE.G
    for _ in range(1, d):
        pt = _add(_CURVE.G, pt)

    return pt


def _validate_pt(pt: list[int|None]) -> None:
    # pt must be a 2-element list.

    assert isinstance(pt, list) and len(pt) == 2

    if isinstance(pt[_X], int):
        # pt's types must match.
        assert isinstance(pt[_Y], int)

        # If pt is purported to be a point on the curve, prove that it is.
        assert _on_curve(pt)
    else:
        # If pt's elements are not of type int, then they must be of type None.
        assert pt[_X] is None and pt[_Y] is None


def _on_curve(pt: list[int]) -> bool:
    # Returns True if the point pt is on the curve; otherwise returns False.

    return (
        pt[_Y] ** 2 % _CURVE.p
        == (pt[_X] ** 3 + (_CURVE.a * pt[_X]) + _CURVE.b) % _CURVE.p
    )


def _validate_priv_key(d: int) -> bool:
    # Private keys must fall in the range 1 <= d < n

    return isinstance(d, int) and 1 <= d < _CURVE.n


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
    if valid and Q == _I:
        valid = False

    # Q's x coordinate must be in the interval [0, p-1].
    if valid and (Q[_X] > _CURVE.p - 1 or Q[_X] < 0):
        valid = False

    # Q's y coordinate must be in the interval [0, p-1].
    if valid and (Q[_Y] > _CURVE.p - 1 or Q[_Y] < 0):
        valid = False

    # Q must be on the curve
    if valid and not _on_curve(Q):
        valid = False

    # If the cofactor h is greater than 1, then the order of the group n times Q must
    # equal the identity element.
    if valid and (_CURVE.h > 1 and _x_times_pt(_CURVE.n, Q) != _I):
        valid = False

    if not valid:
        raise ValueError("Invalid public key")


def _validate_curve_params(B_iters: int = 100) -> None:
    # Recommended curve parameter validation from the Standards for Efficient Cryptography
    # Group's (SECG) specification, "SEC 1: Elliptic Curve Cryptography, Version 2.0"
    # (https://www.secg.org/), section 3.1.1.2.1 (Elliptic Curve Domain Parameters over
    # Fp Validation Primitive).

    valid = True

    # a must be a group element; i.e., within the interval [0, p-1].
    if valid and (_CURVE.a > _CURVE.p - 1 or _CURVE.a < 0):
        valid = False

    # b must be a group element; i.e., within the interval [0, p-1].
    if valid and (_CURVE.b > _CURVE.p - 1 or _CURVE.b < 0):
        valid = False

    # Gx must be a group element; i.e., within the interval [0, p-1].
    if valid and (_CURVE.Gx > _CURVE.p - 1 or _CURVE.Gx < 0):
        valid = False

    # Gy must be a group element; i.e., within the interval [0, p-1].
    if valid and (_CURVE.Gy > _CURVE.p - 1 or _CURVE.Gy < 0):
        valid = False

    # n must not equal p.
    if valid and _CURVE.n == _CURVE.p:
        valid = False

    # The curve must be smooth.
    if valid and (4 * (_CURVE.a**3) + 27 * (_CURVE.b**2)) % _CURVE.p == 0:
        valid = False

    # The base point G must be on the curve.
    if valid and not _on_curve(_CURVE.G):
        valid = False

    # p must be prime.
    if valid and not primes.is_prime(_CURVE.p):
        valid = False

    # n must be prime.
    if valid and not primes.is_prime(_CURVE.n):
        valid = False

    # n additions of the base point G must yield the identity element _i.
    if valid and _fast_point_at(_CURVE.n) != _I:
        valid = False

    # The following two tests are for the cofactor h.
    if valid and _CURVE.h != (math.sqrt(_CURVE.p) + 1) ** 2 // _CURVE.n:
        valid = False

    if valid and _CURVE.h > 2 ** ((_CURVE.p.bit_length() // 2) // 8):
        valid = False

    # Check that the curve is not susceptible to the MOV, FR or SSSA attacks
    # (B_iters should be 100 (the default) for cryptographically strong curves).
    if valid and B_iters < 1:
        valid = False
    else:
        for B in range(1, B_iters):
            if _CURVE.p**B % _CURVE.n == 1:
                valid = False

    if not valid:
        raise ValueError("Invalid curve")
