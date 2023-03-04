"""
A cryptographically secure pseudo-random number generator (CSPRNG).

These routines are more or less a copy/paste of equivalent routines in
the Random and SystemRandom classes, and are used exclusively by modules
in this package that require their services. They are reimplemented here
to provide maximum transparency into their implementation.
"""

import os

from core import util


def randrange(l: int, u: int) -> int:
    """
    Returns a random integer in the range (l, u-1), where l is the lower bound
    and u is the upper bound.
    """
    assert isinstance(l, int) and l >= 0
    assert isinstance(u, int) and u >= 1
    assert u > l

    width = u - l

    return l + randbelow(width)


def randbelow(n: int) -> int:
    """
    Returns a random integer in the range (0, n-1), where n is the upper bound.
    """
    assert isinstance(n, int) and n >= 0

    if n == 0:
        return 0

    k = n.bit_length()

    # 0 <= r < 2**k
    r = randbits(k)
    while r >= n:
        r = randbits(k)

    return r


def randbits(k: int) -> int:
    """
    Returns a positive integer with k random bits.
    """
    assert isinstance(k, int) and k >= 1

    # bits / 8 and rounded up
    numbytes = (k + 7) // 8
    x = util.to_int(os.urandom(numbytes))

    # trim excess bits
    return x >> (numbytes * 8 - k)
