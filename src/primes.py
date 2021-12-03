import random

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
    print('factor_n passed for all primes < 1000')

    for n in large_primes:
        mult, exp = factor_n(n)
        assert (2 ** exp) * mult == n - 1
    print('factor_n passed for large primes')
    ### End tests for factor_n

    ### Begin tests for fast_mod_exp
    for _ in range(100):
        base = random.randrange(1000, 1000000)
        exp = random.randrange(1000,1000000)
        n = random.randrange(1000, 1000000)
        assert fast_mod_exp(base, exp, n) == pow(base, exp, n)
    print('fast_mod_exp passed for 100 large random inputs')
    ### End tests for fast_mod_exp

    ### Begin tests for fermat
    for n in small_primes:
        assert fermat(n)
    print('fermat passed for all primes < 1000')

    for n in odd_composites:
        assert not fermat(n)
    print('fermat passed for odd composites')

    for n in carmichaels:
        assert fermat(n)
    print('fermat passed with false positives for the first 3 carmichael numbers')
    ### End tests for fermat

    ### Begin tests for is_prime
    for n in small_primes:
        assert is_prime(n)
    print('is_prime passed for all primes < 1000')

    for n in small_primes:
        n = n ** 2
        assert not is_prime(n)
    print(f'is_prime passed for the squares of all primes < 1000')

    for n in odd_composites:
        assert not is_prime(n)
    print('is_prime passed for odd composites')

    for n in carmichaels:
        assert not is_prime(n)
    print('is_prime passed with true negatives for the first 3 carmichael numbers')

    for n in large_primes:
        assert is_prime(n)
    print('is_prime passed for large primes')
    ### End tests for is_prime

'''
Returns True if the supplied natural number (positive integer) n is prime. If n < 1000, the
probability of a correct answer is 1 (that is, this function is deterministic). If n > 1000,
the probability of a correct answer is 1 - (2^-128), and increases as the value of rounds
increases. The default value of rounds is 128, which should be sufficient for most
cryptographic purposes.

'''
def is_prime(n):
    
    assert n >= 3 and n % 2 != 0,   'n must be an odd integer > 2'

    # Before doing any heavy lifting, return True for an n that matches any of the first 168
    # primes (up to 1k). Any multiples thereof are composites, and should therefore also fall
    # out, but in that case we return False.
    for prime in small_primes:
        if n % prime == 0:
            return prime == n

    # n is neither a small prime (up to 1k), nor is it a multiple of thereof, so use Miller-Rabin.
    return miller_rabin(n)

'''
The Miller-Rabin primality test.

With a very high degree of probability, returns True if the supplied natural number (positive
integer) n is prime. The probability of a false positive is a function of the magnitude of
rounds, and is 2^-128 given its default value of 128 (i.e., it is vanishingly small). Otherwise,
if n is composite, this method will return False with a probability of 1.

'''
def miller_rabin(n):

    assert n >= 3 and n % 2 != 0,   'n must be an odd integer > 2'

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

'''
Converts input n to the form 2^exp * mult + 1, where mult is the greatest odd
divisor of n - 1, and returns mult and exp.

'''
def factor_n(n):

    assert n >= 3 and n % 2 != 0,   'n must be an odd integer > 2'

    mult = n - 1
    exp = 0

    while mult % 2 == 0:
        mult //= 2
        exp += 1

    return mult, exp

'''
A fast algorithm for modular exponentiation (see square-and-multiply)

'''
def fast_mod_exp(base, exp, n):

    assert base >= 1 and exp >= 1 and n >= 1,   'Base, exp and n must all be > 0'

    result = base if (exp & 1) else 1
    exp_bit_len = exp.bit_length()

    for x in range(1, exp_bit_len):
        base = (base ** 2) % n
        if (exp >> x) & 1:
            result = (result * base) % n

    return result

'''
The Fermat primality test.

Returns True if the the natural number n is prime; otherwise False. This test will,
however, falsely report as prime any of the so-called Carmichael numbers
(e.g. 561, 41041, 825265...) because such numbers, although they are composite,
satisfy the congruence relation a^n = a (mod n) for all 1 < a < n. The Miller-Rabin
primality test accounts for the existence of these numbers, and therefore reports
with a much higher degree of probability the primality of n.
'''
def fermat(n):

    assert n >= 3 and n % 2 != 0,   'n must be an odd integer > 2'

    for i in range(1, n):
        result = fast_mod_exp(i, n, n)
        if result != i:
            return False

    return True

if __name__ == '__main__':
    main()