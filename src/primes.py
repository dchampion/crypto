""" Various functions for generating primes and primality testing. """

import random
import secrets
import math
import util

small_primes =  [  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                  73, 79, 83, 83, 89, 97,101,103,107,109,113,127,131,137,139,149,151,157,163,
                 167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,
                 271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                 389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,
                 503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,
                 631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                 757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,
                 883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

def is_prime(n):
    """
    Returns True if the supplied positive integer n is prime, or False if it is composite.
    If n < 1000, the probability of a correct answer is 1 (that is, this function is
    deterministic). If n > 1000, the probability this function will return an incorrect
    answer, or false positive, is .5^-128; i.e., it is infinitesimally small.
    """
    assert n > 1

    # Handle most trivial cases.
    if n == 2:
        return True
    elif n % 2 == 0:
        return False

    # Before doing any heavy lifting, return True for an n that matches any of the first 168
    # primes (up to 1k). Any multiples thereof are composites, and should therefore also fall
    # out, but in that case we return False.
    for prime in small_primes:
        if n % prime == 0:
            return prime == n

    # n is neither a small prime (up to 1k), nor is it a multiple of thereof, so use Miller-Rabin.
    return miller_rabin(n)

def miller_rabin(n):
    """
    With a very high degree of probability, returns True if the supplied positive odd integer n
    is prime. The probability of a false positive (i.e., that this function will return True if
    in fact n is composite) is .5**128; i.e., it is infinitesimally small. Otherwise, if n is
    composite, this method will return False with a probability of 1.
    """
    assert n >= 3 and n % 2 != 0

    if n == 3:
        # return True in this most trivial edge case.
        return True

    # factor n into 2**e * m + 1.
    m, e = _factor_n(n)
    for _ in range(0, 128, 2):
        b = random.randrange(2, n - 1)
        x = util.fast_mod_exp(b, m, n)

        # if x is 1, repeated squaring will not change the result, so go back to the beginning
        # and try another random b.
        if x != 1:
            i = 0
            while x != n - 1:
                if i == e - 1:
                    # if we don't find an x = n - 1 by repeated squaring, n cannot be prime,
                    # so return False and we're done.
                    return False
                else:
                    x = x ** 2 % n
                    i += 1

    # if we haven't found a composite after 64 rounds, then n is prime with a 1-(2**-128)
    # degree of probability.
    return True

def fermat(n):
    """
    With a very high degree of probability, returns True if the supplied positive odd integer
    n is prime, or False if it is composite. The probability of a false positive (i.e., that
    this function will return True if in fact n is composite) .5**128; i.e., it is infinitesimally
    small. However, if n happens to be a Carmichael number, in particular one with very large
    prime factors, this function will very likely return True, even though n is composite. While
    Carmichael numbers of this sort are rare, they do exist. Because of this, the Miller-Rabin
    test, which controls for them, should be preferred.
    """
    assert n >= 3 and n % 2 != 0

    if n == 3:
        return True

    # Do up to 128 rounds of the Fermat primality test on random bases (see Fermat's little
    # theorem).
    for _ in range(0, 128):
        base = random.randrange(2, n - 1)
        result = util.fast_mod_exp(base, n - 1, n)
        if result != 1:
            return False

    return True

def _factor_n(n):
    """
    Returns the pair (m, e), after conversion of the supplied positive odd integer n to the
    form 2**e * m + 1, where m is the greatest odd divisor of n - 1.
    """
    assert n >= 3 and n % 2 != 0

    m = n - 1
    e = 0

    while m % 2 == 0:
        m //= 2
        e += 1

    return m, e

def generate_prime(bit_len):
    """
    Returns a prime number of bit_len bits in length. The function selects random values in the
    range 2**bit_len-1 to 2**bit_len, and tests them for primality. If a prime is not found after
    a sensible number of tries, an exception is raised (this should be rare), in which case the
    function can be called again to generate a prime.
    """
    tries = 100 * math.floor(math.log2(2**bit_len)+1)
    secure_random = secrets.SystemRandom()
    for _ in range(tries):
        p = secure_random.randrange(2**(bit_len-1), 2**bit_len)

        # Make p odd.
        p |= 1
        if is_prime(p):
            return p

    raise Exception("Failed to generate a prime")