""" Cryptographic helper functions for finite-field operations. """

from . import euclid


def fast_mod_exp(a: int, e: int, n: int) -> int:
    """
    Returns the equivalent of b^e % n, but with much better performance than
    that form for very large numbers.
    """
    assert isinstance(a, int) and a >= 0
    assert isinstance(e, int) and e >= 0
    assert isinstance(n, int) and n >= 1

    e_bit_len = e.bit_length()

    # Don't screw around with edge cases; let the language primitives do the
    # work (this will be no slower than the fast algorithm).
    if e_bit_len < 8:
        result = a**e % n
    else:
        # Use square-and-multiply for speedy exponentiation of larger exponents.
        result = a if (e & 1) else 1
        for x in range(1, e_bit_len):
            a = (a**2) % n
            if (e >> x) & 1:
                result = (result * a) % n

    return result


def fast_mod_exp_crt(a: int, e: int, p: int, q: int) -> int:
    """
    Returns the equivalent of b^e % pq, but with much better performance than
    that form for very large numbers. When exponentiating bases to very large
    powers modulo a semiprime modulus whose factors are known (i.e., p and q),
    this function provides a factor of 3-4 performance improvement over the
    function fast_mod_exp.
    """
    assert isinstance(a, int)
    assert isinstance(e, int)
    assert isinstance(p, int)
    assert isinstance(q, int)

    x = fast_mod_exp(a, _reduce(e, p), p)
    y = fast_mod_exp(a, _reduce(e, q), q)

    return from_crt(x, y, p, q)


def _reduce(e: int, n: int) -> int:
    r = e % (n - 1)
    return r if r != 0 else e


def from_crt(x: int, y: int, p: int, q: int) -> int:
    """
    Returns a unique value x from the set (1, ..., p*q - 1) given the CRT
    representation of x, or (x mod p, x mod q). The parameter a is shorthand
    for x mod p, and the parameter b is shorthand for x mod q.
    """
    assert isinstance(x, int) and x >= 0
    assert isinstance(y, int) and y >= 0
    assert isinstance(p, int) and p >= 1
    assert isinstance(q, int) and q >= 1

    inv = euclid.inverse(q, p)

    # Use Garner's formula to compute x mod pq
    return (((x - y) * inv) % p) * q + y


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


def digest(k: object, hash_obj) -> bytes:
    """
    Returns a hashed byte array of input k using the hash algorithm provided by
    hash_obj. hash_obj must conform to the standard interface for hash objects
    specified in the Python standard library module hashlib.
    """
    hash_obj.update(str(k).encode("utf-8"))
    return hash_obj.digest()


def to_int(o: object, byteorder: str="big") -> int:
    """
    Given an object o, and an optional parameter byteorder (default="big"),
    returns the integer representation of o.
    """
    if isinstance(o, int):
        return o
    elif isinstance(o, bytes):
        i = int.from_bytes(o, byteorder=byteorder)
    else:
        i = int.from_bytes(str(o).encode("utf-8"), byteorder=byteorder)

    return i


def to_bytes(i: int, byteorder: str="big") -> bytes:
    """
    Given an integer i, and an optional parameter byteorder (default="big"),
    returns a byte array representation of i.
    """
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder=byteorder)

