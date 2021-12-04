"""
Various functions for generating large random numbers and testing them for primality.
"""
import random
import secrets
import math

small_primes =  [ 3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                 73, 79, 83, 83, 89, 97,101,103,107,109,113,127,131,137,139,149,151,157,163,
                 167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,
                 271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                 389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,
                 503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,
                 631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                 757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,
                 883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

odd_composites = [9,15,27,35,49,133,339,589,711,999,2**521+1,2**607+1]

# Large Mersenne primes
large_primes =  [2**521-1,2**607-1,2**1279-1,2**2203-1,2**2281-1]

carmichaels =   [561,41041,825265]

def main():

    ### Begin tests for factor_n
    for n in small_primes:
        mult, exp = factor_n(n)
        assert (2 ** exp) * mult == n - 1
    print(f"factor_n passed for all {len(small_primes)} primes <= {small_primes[len(small_primes)-1]}")

    for n in large_primes:
        mult, exp = factor_n(n)
        assert (2 ** exp) * mult == n - 1
    print(f"factor_n passed for {len(large_primes)} large primes")
    ### End tests for factor_n

    ### Begin tests for fast_mod_exp
    for _ in range(100):
        base = random.randrange(1000, 1000000)
        exp = random.randrange(1000,1000000)
        n = random.randrange(1000, 1000000)
        assert fast_mod_exp(base, exp, n) == pow(base, exp, n)
    print("fast_mod_exp passed for 100 large random inputs")
    ### End tests for fast_mod_exp

    ### Begin tests for fermat
    for n in small_primes:
        assert fermat(n)
    print(f"fermat passed for all {len(small_primes)} primes <= {small_primes[len(small_primes)-1]}")

    for n in odd_composites:
        assert not fermat(n)
    print(f"fermat passed for {len(odd_composites)} odd composites")

    for n in carmichaels:
        assert fermat(n)
    print(f"fermat passed with false positives for {len(carmichaels)} Carmichael numbers")
    ### End tests for fermat

    ### Begin tests for is_prime
    for n in small_primes:
        assert is_prime(n)
    print(f"is_prime passed for all {len(small_primes)} primes <= {small_primes[len(small_primes)-1]}")

    for n in small_primes:
        n = n ** 2
        assert not is_prime(n)
    print(f"is_prime passed for the squares of all {len(small_primes)} primes <= {small_primes[len(small_primes)-1]}")

    for n in odd_composites:
        assert not is_prime(n)
    print(f"is_prime passed for {len(odd_composites)} odd composites")

    for n in carmichaels:
        assert not is_prime(n)
    print(f"is_prime passed with true negatives for {len(carmichaels)} Carmichael numbers")

    for n in large_primes:
        assert is_prime(n)
    print(f"is_prime passed for {len(large_primes)} large primes")
    ### End tests for is_prime

    ### Begin tests for generate_large_prime
    for x in range(3, 12):
        p = generate_prime(2 ** x - 1, 2 ** x)
        assert is_prime(p)
    print("generate_large_primes passed for primes up to 2048 bits in length")
    ### End tests for generate_large_prime

def is_prime(n):
    """
    Returns True if the supplied natural number (positive integer) n is prime. If n < 1000, the
    probability of a correct answer is 1 (that is, this function is deterministic). If n > 1000,
    the probability of a correct answer is 1 - (2^-128); i.e., it is infinitesimally small.
    """
    assert n >= 3 and n % 2 != 0,   "n must be an odd integer > 2"

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
    The Miller-Rabin primality test.

    With a very high degree of probability, returns True if the supplied natural number (positive
    integer) n is prime. The probability of a false positive is 1 - (2^-128); i.e., it is
    infinitesimally small. Otherwise, if n is composite, this method will return False with
    a probability of 1.
    """
    assert n >= 3 and n % 2 != 0,   "n must be an odd integer > 2"

    if n == 3:
        # return True in this most trivial edge case.
        return True

    # factor n into 2^exp * mult + 1.
    mult, exp = factor_n(n)

    random.seed()
    
    for _ in range(0, 128, 2):
        
        base = random.randrange(2, n - 1)
        
        x = fast_mod_exp(base, mult, n)
        
        # if x is 1, repeated squaring will
        # not change the result, so don't bother continuing.
        if x != 1:
            i = 0
            while x != n - 1:
                if i == exp - 1:
                    # if we don't find an x = n - 1 by
                    # repeated squaring, n cannot be prime.
                    return False
                else:
                    x = (x ** 2) % n
                    i += 1

    # if we haven't found a composite after 64 rounds,
    # then n is prime with a 1-2^-128 degree of probability.
    return True

def factor_n(n):
    """
    Converts input n to the form 2^exp * mult + 1, where mult is the greatest odd
    divisor of n - 1, and returns mult and exp.
    """
    assert n >= 3 and n % 2 != 0,   "n must be an odd integer > 2"

    mult = n - 1
    exp = 0

    while mult % 2 == 0:
        mult //= 2
        exp += 1

    return mult, exp

def fast_mod_exp(base, exp, n):
    """
    A fast algorithm for modular exponentiation (see square-and-multiply).
    """
    assert base >= 1 and exp >= 1 and n >= 1,   "Base, exp and n must all be > 0"

    result = base if (exp & 1) else 1
    exp_bit_len = exp.bit_length()

    for x in range(1, exp_bit_len):
        base = (base ** 2) % n
        if (exp >> x) & 1:
            result = (result * base) % n

    return result

def fermat(n):
    """
    The Fermat primality test.

    Returns True if the the natural number n is prime; otherwise False. This test will,
    however, falsely report as prime any of the so-called Carmichael numbers
    (e.g. 561, 41041, 825265, ...) because such numbers, although they are composite,
    satisfy the congruence relation a^n = a (mod n) for all 1 < a < n. The Miller-Rabin
    test should therefore be preferred, because it accounts for the Carmichael numbers,
    and therefore reports with a much higher degree of probability the primality of n.
    """
    assert n >= 3 and n % 2 != 0,   "n must be an odd integer > 2"

    for i in range(1, n):
        result = fast_mod_exp(i, n, n)
        if result != i:
            return False

    return True

def generate_prime(l, u):
    """
    Returns a prime number between l and u bits in length. The function randomly selects numbers
    in the range 2^l to 2^u and tests them for primality. If a prime is not found in a sensible
    number of tries, an exception is raised (this should be rare), in which case the function can
    be tried again.
    """
    secure_random = secrets.SystemRandom()
    tries = 100 * math.floor(math.log2(u)+1)
    for _ in range(tries):
        p = secure_random.randrange(2**l, 2**u) | 1
        if is_prime(p):
            return p

    err_str = f"Unable to find a prime between {l} and {u} bits in {tries} random selections"
    raise Exception(err_str)

if __name__ == "__main__":
    main()