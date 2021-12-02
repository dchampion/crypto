import sys
import random

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} n [rounds],\n' +
               '       where n is a natural number,\n' +
               '         and rounds (optional) specifies the number of Miller-Rabin rounds to apply')
        exit(1)
    
    n = sys.argv[1]
    rounds = 128 if len(sys.argv) < 3 else int(sys.argv[2])
    
    print(f'{n} is', 'prime' if is_prime(int(sys.argv[1]), rounds) else 'not prime')

'''
Returns True if the supplied natural number (positive integer) n is prime. If n < 1000, the
probability of a correct answer is 1 (that is, this function is deterministic). If n > 1000,
the probability of a correct answer is 1 - (2^-128), and increases as the value of rounds
increases. The default value of rounds is 128, which should be sufficient for most
cryptographic purposes.

'''
def is_prime(n, rounds=128):
    
    assert n >= 3,        'n must be no less than 3'
    assert n % 2 != 0,    'n must be an odd number'
    assert rounds >= 128, 'Rounds must be no less than 128'

    small_primes = [  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                     73, 79, 83, 83, 89, 97,101,103,107,109,113,127,131,137,139,149,151,157,163,
                    167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,
                    271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                    389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,
                    503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,
                    631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                    757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,
                    883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

    # Before doing any heavy lifting, return True for an n that matches any of the first 168
    # primes (up to 1k). Any multiples thereof are composites, and should therefore also fall
    # out, but in that case we return False.
    for prime in small_primes:
        if n % prime == 0:
            return prime == n

    # n is neither a small prime (up to 1k), nor is it a multiple of thereof, so use Miller-Rabin.
    return miller_rabin(n, rounds)

'''
The Miller-Rabin primality test.

With a very high degree of probability, returns True if the supplied natural number (positive
integer) n is prime. The probability of a false positive is a function of the magnitude of
rounds, and is 2^-128 given its default value of 128 (i.e., it is vanishingly small). Otherwise,
if n is composite, this method will return False with a probability of 1.

'''
def miller_rabin(n, rounds=128):

    assert n >= 3,        'n must be no less than 3'
    assert n % 2 != 0,    'n must be an odd number'
    assert rounds >= 128, 'rounds must be no less than 128'

    if n == 3:
        return True

    mult, exp = factor_n(n)

    random.seed()
    
    for _ in range(rounds):
        
        base = random.randrange(2, n - 1)
        
        x = fast_mod_exp(base, mult, n)
        if x != 1:
        
            i = 0
            while x != n - 1:
                if i == exp - 1:
                    return False
                else:
                    x = (x ** 2) % n
                    i += 1

    return True

'''
Converts input n to the form 2^exp * mult + 1, where mult is the greatest odd
divisor of n - 1, and returns mult and exp.

'''
def factor_n(n):

    assert n >= 3,      'n must be no less than 3'
    assert n % 2 != 0,  'n must be an odd number'

    mult = n - 1
    exp = 0

    while mult % 2 == 0:
        mult //= 2
        exp += 1
    
    assert (2 ** exp) * mult == n - 1

    return mult, exp

'''
A fast algorithm for modular exponentiation (see square-and-multiply)

'''
def fast_mod_exp(base, exp, n):

    assert base > 1,    'Base must be greater than 1'
    assert exp >= 1,    'Exponent must be greater than 0'
    assert n > 1,       'Modulus must be greater than 1'

    result = base if (exp & 1) else 1
    exp_bit_len = exp.bit_length()

    for x in range(1, exp_bit_len):
        base = (base ** 2) % n
        if (exp >> x) & 1:
            result = (result * base) % n

    return result

if __name__ == '__main__':
    main()