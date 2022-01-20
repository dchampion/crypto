"""
A cryptographically secure pseudo-random number generator (PRNG).

These routines are more or less a copy/paste of equivalent routines in
the Random and SystemRandom classes, but are reimplemented here to maintain
control of their evolution.
"""

import os

def randrange(l, u):
    """
    Returns a random integer in the range (l, u-1), where l is the lower bound
    and u is the upper bound.
    """
    assert isinstance(l, int)
    assert isinstance(u, int)
    assert u > l

    width = u - l

    return l + randbelow(width)

def randbelow(n):
    """
    Returns a random integer in the range (0, n-1), where n is the upper bound.
    """
    assert isinstance(n, int)

    if n == 0:
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
    assert isinstance(k, int) and k >= 1

    # bits / 8 and rounded up
    numbytes = (k + 7) // 8
    x = int.from_bytes(os.urandom(numbytes), byteorder="big")

    # trim excess bits
    return x >> (numbytes * 8 - k)