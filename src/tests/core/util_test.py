import random

from core import primes
from core import util as core_util
from . import util as test_util

@test_util.test_log
def main():
    test_crt_conversions()
    test_fast_mod_exp()
    test_fast_mod_exp_crt()


@test_util.test_log
def test_crt_conversions():
    for _ in range(10):
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        x = random.randrange(1, p * q - 1)
        a, b = core_util.to_crt(x, p, q)
        x1 = core_util.from_crt(a, b, p, q)
        assert x == x1, "Conversion mismatch"

    # Test edge cases
    for _ in range(100):
        while True:
            p = random.choice(primes._small_primes[0:5])
            q = random.choice(primes._small_primes[0:5])
            if p != q:
                break
        x = random.randrange(1, 10)
        a, b = core_util.to_crt(x, p, q)
        x1 = core_util.from_crt(a, b, p, q)
        assert x == x1, "Conversion mismatch"


@test_util.test_log
def test_fast_mod_exp():
    for _ in range(100):
        b = random.randrange(0, 2**1024)
        e = random.randrange(0, 2**1024)
        n = random.randrange(1, 2**1024)
        assert core_util.fast_mod_exp(b, e, n) == pow(
            b, e, n
        ), f"fast_mod_exp({b}, {e}, {n}) failed"

    # Test edge cases
    for b in range(0, 10):
        for e in range(0, 10):
            for n in range(1, 10):
                assert core_util.fast_mod_exp(b, e, n) == b**e % n


@test_util.test_log
def test_fast_mod_exp_crt():
    for _ in range(10):
        b = random.randrange(0, 2**1024)
        e = random.randrange(0, 2**1024)
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert core_util.fast_mod_exp_crt(b, e, p, q) == pow(
            b, e, p * q
        ), f"fast_mod_exp_crt({b}, {e}, {p}, {q}) failed"

    # Test edge cases
    for b in range(0, 10):
        for e in range(0, 10):
            for _ in range(1, 10):
                while True:
                    p = random.choice(primes._small_primes[0:5])
                    q = random.choice(primes._small_primes[0:5])
                    if p != q:
                        break
                assert core_util.fast_mod_exp_crt(b, e, p, q) == b**e % (p * q)


if __name__ == "__main__":
    main()
