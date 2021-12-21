""" Crypto helper functions """
import random
import euclid
import primes

def main():
    print("Running tests...")
    ### Begin tests for CRT conversions
    for _ in range(10):
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert p != q, "Bad PRNG?"
        x = random.randrange(1,1024-1)
        a, b = x_to_ab(x, p, q)
        x1 = ab_to_x(a, b, p, q)
        assert x == x1, "Conversion mismatch"
    print("x_to_ab -> ab_to_x conversion passed for 10 random inputs")
    ### End tests for CRT conversions

    ### Begin tests for fast_mod_exp
    for _ in range(100):
        b = random.randrange(1000, 1000000)
        e = random.randrange(1000, 1000000)
        n = random.randrange(1000, 1000000)
        assert fast_mod_exp(b, e, n) == pow(b, e, n),\
            f"fast_mod_exp({b}, {e}, {n}) failed"
    print("fast_mod_exp() passed for 100 large random inputs")
    ### End tests for fast_mod_exp

    ### Begin tests for fast_mod_exp_crt
    for _ in range(10):
        b = random.randrange(1000, 1000000)
        e = random.randrange(1000, 1000000)
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert p != q, "Bad PRNG?"
        assert fast_mod_exp_crt(b, e, p, q) == pow(b, e, p*q),\
            f"fast_mod_exp_crt({b}, {e}, {p}, {q}) failed"
    print("fast_mod_exp_crt passed for 10 random inputs")
    ### End tests for fast_mod_exp_crt
    print("all tests passed")

def fast_mod_exp(b, e, n):
    """
    A fast algorithm for modular exponentiation (see square-and-multiply).
    """
    assert b >= 1 and e >= 1 and n >= 1,   "b, e and n must all be > 0"

    result = b if (e & 1) else 1
    exp_bit_len = e.bit_length()

    for x in range(1, exp_bit_len):
        b = (b ** 2) % n
        if (e >> x) & 1:
            result = (result * b) % n

    return result

def fast_mod_exp_crt(b, e, p, q):
    """
    A fast algorithm for modular exponentiation, where the modulus is a large,
    semi-prime number; i.e., the product of two very large prime factors (p and q),
    the primary use-case for which is RSA. When exponentiating very large bases
    to very large powers modulo a semi-prime number, this function provides a
    factor of 3-4 time savings over fast_mod_exp.
    """
    a = fast_mod_exp(b, e % (p - 1), p)
    b = fast_mod_exp(b, e % (q - 1), q)

    return ab_to_x(a, b, p, q)

def ab_to_x(a, b, p, q):
    """
    Given a CRT representation (x mod p, x mod q) of some integer x mod pq,
    returns x mod pq (CRT -> Chinese Remainder Theorem).
    """
    inv = euclid.inverse(q, p)

    # Use Garner's formula to compute x mod pq
    return (((a - b) * inv) % p) * q + b

def x_to_ab(x, p, q):
    """
    Given some integer x mod pq, returns the CRT representation (x mod p, x mod q)
    (CRT -> Chinese Remainder Theorem).
    """
    return x % p, x % q

if __name__ == "__main__":
    main()