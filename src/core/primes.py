""" Various functions for generating primes and primality testing. """

import math

from . import prng
from . import util
from . import euclid

_small_primes =  [ 3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                  73, 79, 83, 83, 89, 97,101,103,107,109,113,127,131,137,139,149,151,157,163,
                 167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,
                 271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                 389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,
                 503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,
                 631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                 757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,
                 883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

def is_prime(n: int) -> bool:
    """
    Returns True if the supplied positive integer n is prime, or False if it is composite.
    This function is probabilistic, as defined by the following characteristics:

    If n < 1,000, then the probability this function will return a correct answer is 1;
    that is, this function is deterministic.

    If n > 1,000, and this function returns False, then the probability n is composite is
    also 1; that is, this function is deterministic.

    However, if n > 1,000, and this function returns True, then the probability n is
    composite is .25^64 (or 2.93 x 10^-39); that is, if n is prime, this function is
    probabilistic, but with an astronomically high level of confidence.
    """
    assert isinstance(n, int) and n > 1

    # Dispense with even numbers.
    if n % 2 == 0:
        return n == 2

    # Dispense with small primes and multiples thereof. Return True for an n that matches
    # any of the first 168 primes (less than 1,000). Any multiples thereof are composites
    # (but for those return False).
    for prime in _small_primes:
        if n % prime == 0:
            return n == prime

    # n is neither even, a small prime, nor a multiple of thereof; use Miller-Rabin.
    return not _is_composite(n)


def _is_composite(n: int) -> bool:
    # The Miller-Rabin primality test. Returns True if the supplied positive odd
    # integer n is composite; otherwise False. This function is probabilistic, in
    # that it is theoretically possible for it to return False for an n that is in
    # fact composite. However, the probability of such an error is .25^64. Conversely,
    # if this function returns True, n is assured to be composite.

    _validate_param(n)

    if n == 3:
        return False

    # factor n into s and t, such that n = ((2^t) * s) + 1.
    s, t = _factor_n(n)
    for _ in range(64):

        # select a random base a in the range [2..n-1] and raise it to the power of
        # s modulo n.
        a = prng.randrange(2, n - 1)
        x = util.fast_mod_exp(a, s, n)

        # if x is 1, we have a possible prime, and repeatedly squaring 1 will always
        # result in 1, so start over with another random base. If x is not 1, then
        # we have a possible composite and should continue probing for compositeness.
        if x != 1:

            # if x is n-1, we have a possible prime, so start over with another random
            # base. If x is not n-1, then we have a possible composite and should
            # continue probing for compositeness.
            i = 1
            while x != n - 1:

                if i == t:

                    # if we don't find a case where x = n-1 by repeatedly squaring x
                    # t times, then n MUST be composite; return True.
                    return True

                x = x**2 % n
                i += 1

    # we are here because we haven't established the compositeness of n after trying
    # 64 random bases. This means n is prime with a probability of 1 - .25^64. This
    # probability comes from the fact that roughly only 1 in 4 (or .25) bases is a
    # false witness to the primality of a composite n.
    return False


def _factor_n(n: int) -> tuple[int, int]:
    # Returns the tuple (s, t), after conversion of the supplied positive odd integer
    # n to the form (2^t * s) + 1, where s is the greatest odd divisor of n-1. This
    # function is a helper for _is_composite().

    _validate_param(n)

    s = n - 1
    t = 0

    while s % 2 == 0:
        s //= 2
        t = t + 1

    return s, t


def _is_composite_2(n: int) -> bool:
    # An implementation of the Miller-Rabin primality test that is easy to
    # reason about. We use this test instead of the Fermat test because some
    # pseudo-prime numbers, known as Carmichael numbers, defeat the Fermat
    # test. Specifically, for every base a, where 1 < a < n and n is a
    # Carmichael number, a^n = a (mod n) holds, even though n is not prime.

    # To understand the mechanics of this algorithm, it first helps to
    # consider these facts:

    # 1. Fermat's little theorem tells us that a^n = a (mod n) for any prime
    # n, where 1 < a < n.
    # 2. Dividing both sides by a, this can be rewritten as a^(n-1) = 1 (mod n).
    # 3. Further, the square root of a^(n-1) is a^((n-1)/2); e.g., 3^3 is the
    # square root of 3^6, which is the square root of 3^12, etc.
    # 4. If n is prime, then the square root of 1 modulo n must be either 1 or
    # -1 (which can also written as n-1). This is a specialization of Euclid's
    # lemma.
    # 5. If n is composite, it is also possible for the square root of 1 modulo n
    # to be 1 or -1, but the probability of such a result is only .25; i.e.,
    # approximately 1 in 4 bases a are false witnesses to the primality of said
    # composite n.
    # 6. If a square root of 1 modulo n is neither 1 nor -1, then n must be
    # composite.

    # The algorithm works as follows:

    # 1. Given an odd positive integer n, select a random base a in the range
    # [2..n-1] and set s = n-1.
    # 2. While s is even, set s = s/2 and x = a^s mod n. Note that halving an
    # exponent results in a square root. For example, the square root of a^s is
    # a^(s/2).
    # 3. If x = 1, n might be prime. Repeat step 2.
    # 4. If x = n-1, n might also be prime, but there is no need to test its
    # square root. Go to step 1. There is no further need to test its square root
    # because, given that the square root of 1 modulo n is either 1 or -1, there
    # is no such gaurantee regarding the square root of -1 modulo n.
    # 5. If x != 1 and x != n-1, n MUST be composite. Return True.
    # 6. If the compositeness of n is not established after executing steps 1-5
    # 64 times, then n is prime with a probability of 1 - .25^64. Return False.

    # The small likelihood (i.e., .25^-64) of this function falsely reporting n as
    # prime when it is in fact composite comes from the fact that, on average, 1 in
    # 4 (or .25) bases will pass the Miller-Rabin test if n is composite. Repeating
    # the test with 64 randomly selected bases thus results in a probability of
    # .25^64.

    _validate_param(n)

    if n == 3:
        return False

    for _ in range(64):
        a = prng.randrange(2, n - 1)
        s = n - 1
        while s % 2 == 0:
            s //= 2
            x = util.fast_mod_exp(a, s, n)
            if x == 1:
                continue
            if x == n - 1:
                break
            return True

    return False


def _fermat_is_prime(n: int) -> bool:
    # Returns True if the supplied positive odd integer n is prime; otherwise False. This
    # function is probabilistic, in that it is possible for it to return True for an n
    # that is in fact not prime. For example, if n is a so-called Carmichael number,
    # this function may return True even though n is composite. Because of this, the
    # miller_rabin function, which accounts for Carmichael numbers, should be preferred to
    # this one for primality testing.

    _validate_param(n)

    if n == 3:
        return True

    # Do up to 128 rounds of the Fermat primality test on random bases (see Fermat's little
    # theorem).
    for _ in range(128):
        a = prng.randrange(2, n - 1)
        result = util.fast_mod_exp(a, n, n)
        if result != a:
            return False

    return True


def fermat_factor(n: int) -> tuple[bool, int, int] | bool:
    """
    Attempts to factor a valid RSA modulus n using Fermat's factorization algorithm. A valid n
    is a composite integer that is the product of exactly two distinct prime factors. Returns
    the tuple (True, p, q) if the factorization is successful, where p and q are the prime
    factors of n; otherwise returns False. This function can be used to test the suitability of
    a modulus in an RSA public key. A successful factorization of n indicates its factors p and
    q are too close together, and therefore that n is not safe for use in such a key. Possible
    causes of this could be too small an n, a poorly implemented prime number-generating
    algorithm, a bad pseudo-random number generator...
    """
    assert isinstance(n, int) and n > 2 and n % 2 != 0
    assert not is_prime(n)
    assert not _is_square(n)

    # Fermat's factorization algorithm leverages the fact that a valid RSA modulus must be odd,
    # and every odd number can be expressed as the difference of two squares; i.e., n = a^2 - b^2
    # = (a+b)(a-b). If we start with a number a that is close to the square root of n, repeatedly
    # increment it by 1, and find after fewer than 1m iterations that b^2 = a^2 - n, then we have
    # found the nontrivial factors of n. Here b is the distance from a to the prime factors of n.
    a = math.isqrt(n) + 1
    c, tries = 0, 1000
    while not _is_square(a**2 - n):
        a += 1
        c += 1
        if c > tries:
            return False

    b2 = a**2 - n
    b = math.isqrt(b2)

    return True, a + b, a - b


def _is_square(n: int) -> bool:
    return n == math.isqrt(n) ** 2


def shor_factor(n: int) -> tuple[int, int]:
    """
    Attempts to factor a valid RSA modulus n using Shor's factorization algorithm. A valid n
    is an integer that is the composite product of exactly two distinct prime factors. Returns
    the tuple (p, q) if the factorization is successful, where p and q are the prime factors of
    n. The runtime performance of this algorithm is exponential in the size of n; therefore it
    should generally not be called with n > 32 bits.
    """
    assert isinstance(n, int) and n > 2 and n % 2 != 0
    assert not is_prime(n)
    assert not _is_square(n)

    while True:
        a = prng.randrange(1, n)
        g = euclid.gcd(a, n)
        if g != 1:
            return g, n // g

        r = 1
        while util.fast_mod_exp(a, r, n) != 1:
            r += 1

        if r % 2 == 0:
            s = util.fast_mod_exp(a, r//2, n)
            if s + 1 != n:
                return euclid.gcd(s+1, n), euclid.gcd(s-1, n)


def _validate_param(n: int) -> None:
    assert isinstance(n, int) and n >= 3 and n % 2 != 0


def generate_prime(bit_len: int) -> int:
    """
    Returns a prime number of bit_len bits in length, testing randomly selected values for
    primality. If a prime is not found after a sensible number of tries, an exception is raised
    (this should be rare), in which case the function can be called again to generate a prime.
    """
    tries = 100 * bit_len
    for _ in range(tries):
        n = prng.randrange(2 ** (bit_len - 1), 2**bit_len)
        if is_prime(n):
            return n

    raise Exception("Failed to generate a prime")
