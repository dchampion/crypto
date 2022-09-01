""" Cryptographic helper functions for finite-field operations. """

from . import euclid

import hashlib

def fast_mod_exp(b: int, e: int, n: int) -> int:
    """
    Returns the equivalent of b^e % n, but with much better performance than
    that form for very large numbers.
    """
    assert isinstance(b, int) and b >= 0
    assert isinstance(e, int) and e >= 0
    assert isinstance(n, int) and n >= 1

    e_bit_len = e.bit_length()

    # Don't screw around with edge cases; let the language primitives do the
    # work (this will be no slower than the fast algorithm).
    if e_bit_len < 8:
        result = b**e % n
    else:
        # Use square-and-multiply for speedy exponentiation of larger exponents.
        result = b if (e&1) else 1
        for x in range(1, e_bit_len):
            b = (b**2) % n
            if (e>>x) & 1:
                result = (result * b) % n

    return result

def fast_mod_exp_crt(b: int, e: int, p: int, q: int) -> int:
    """
    Returns the equivalent of b^e % pq, but with much better performance than
    that form for very large numbers. When exponentiating bases to very large
    powers modulo a semiprime modulus whose factors are known (i.e., p and q),
    this function provides a factor of 3-4 performance improvement over the
    function fast_mod_exp.
    """
    assert isinstance(b, int)
    assert isinstance(e, int)
    assert isinstance(p, int)
    assert isinstance(q, int)

    a = fast_mod_exp(b, _reduce(e, p), p)
    b = fast_mod_exp(b, _reduce(e, q), q)

    return from_crt(a, b, p, q)

def _reduce(e: int, n: int) -> int:
    r = e % (n - 1)
    return r if r != 0 else e

def from_crt(a: int, b: int, p: int, q: int) -> int:
    """
    Returns a unique value x from the set (1, ..., p*q - 1) given the CRT
    representation of x, or (x mod p, x mod q). The parameter a is shorthand
    for x mod p, and the parameter b is shorthand for x mod q.
    """
    assert isinstance(a, int) and a >= 0
    assert isinstance(b, int) and b >= 0
    assert isinstance(p, int) and p >= 1
    assert isinstance(q, int) and q >= 1

    inv = euclid.inverse(q, p)

    # Use Garner's formula to compute x mod pq
    return (((a - b) * inv) % p) * q + b

def to_crt(x: int, p: int, q: int) -> tuple[int, int]:
    """
    Returns the tuple (a, b), where (a, b) is the CRT representation of x in the
    set (1, ..., p*q - 1). The value a from the returned tuple is shorthand for
    x mod p, and the value b is shorthand for x mod q.
    """
    assert isinstance(x, int) and x >= 0
    assert isinstance(p, int) and p >= 1
    assert isinstance(q, int) and q >= 1

    return x % p, x % q

def hash(k: any) -> bytes:
    """
    Returns a hashed byte array of input k.
    """
    return hashlib.sha256(str(k).encode("utf-8")).digest()
