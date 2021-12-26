import sys
sys.path.append("../src")

import util
import primes
import random

def main():
    print("Running util tests...")
    test_crt_conversions()
    test_fast_mod_exp()
    test_fast_mod_exp_crt()
    print("util tests passed")

def test_crt_conversions():
    for _ in range(10):
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert p != q, "Bad PRNG?"
        x = random.randrange(1,1024-1)
        a, b = util.x_to_ab(x, p, q)
        x1 = util.ab_to_x(a, b, p, q)
        assert x == x1, "Conversion mismatch"

    print("x_to_ab -> ab_to_x conversion passed for 10 random inputs")

def test_fast_mod_exp():
    for _ in range(100):
        b = random.randrange(1000, 1000000)
        e = random.randrange(1000, 1000000)
        n = random.randrange(1000, 1000000)
        assert util.fast_mod_exp(b, e, n) == pow(b, e, n),\
            f"fast_mod_exp({b}, {e}, {n}) failed"

    print("fast_mod_exp passed for 100 large random inputs")

def test_fast_mod_exp_crt():
    for _ in range(10):
        b = random.randrange(1000, 1000000)
        e = random.randrange(1000, 1000000)
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert p != q, "Bad PRNG?"
        assert util.fast_mod_exp_crt(b, e, p, q) == pow(b, e, p*q),\
            f"fast_mod_exp_crt({b}, {e}, {p}, {q}) failed"

    print("fast_mod_exp_crt passed for 10 random inputs")

if __name__ == "__main__":
    main()