""" A cryptographically secure pseudo-random number generator (PRNG). """
import os
import operator

def randrange(l, u):
    """
    Returns a random integer in the range (l, u-1), where l is the lower bound
    and u is the upper bound.
    """
    il = operator.index(l)
    iu = operator.index(u)
    width = iu - il
    if width < 1:
        raise ValueError(f"upper bound {u} must be greater than lower bound {l}")

    return il + randbelow(width)

def randbelow(n):
    """
    Returns a random integer in the range (0, n-1), where n is the upper bound.
    """
    if not n:
        return 0

    k = n.bit_length()

    # 0 <= r < 2**k
    r = randbits(k)
    while r >= n:
        r = randbits(k)
    return r

def randbits(k):
    """
    Returns a positive integer with k random bits.
    """
    if k < 0:
        raise ValueError("Number of bits must be non-negative")

    # bits / 8 and rounded up
    numbytes = (k + 7) // 8
    x = int.from_bytes(os.urandom(numbytes), byteorder="big")

    # trim excess bits
    return x >> (numbytes * 8 - k)