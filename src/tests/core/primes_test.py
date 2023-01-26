from core import primes

from . import util

odd_composites = [
    9,
    15,
    27,
    35,
    49,
    133,
    339,
    589,
    711,
    999,
    2**521 + 1,
    2**607 + 1,
]
even_composites = [n + 1 for n in odd_composites]

# Large (Mersenne) primes
large_primes = [2**521 - 1, 2**607 - 1, 2**1279 - 1, 2**2203 - 1, 2**2281 - 1]

small_carmichaels = [
    561,
    1105,
    1729,
    2465,
    2821,
    6601,
    8911,
    41041,
    62745,
    63973,
    825265,
]

# These Carmichaels will defeat the Fermat primality test (but not Miller-Rabin).
large_carmichaels = [
    ((6 * 925968953850065) + 1)
    * ((12 * 925968953850065) + 1)
    * ((18 * 925968953850065) + 1),
    ((6 * 8522851273339146) + 1)
    * ((12 * 8522851273339146) + 1)
    * ((18 * 8522851273339146) + 1),
    ((6 * 9510693751425636) + 1)
    * ((12 * 9510693751425636) + 1)
    * ((18 * 9510693751425636) + 1),
    ((6 * 9510693751431925) + 1)
    * ((12 * 9510693751431925) + 1)
    * ((18 * 9510693751431925) + 1),
    ((6 * 9510693751446670) + 1)
    * ((12 * 9510693751446670) + 1)
    * ((18 * 9510693751446670) + 1),
]


@util.test_log
def main():
    test_factor_n()
    test_fermat_is_prime()
    test_is_prime()
    test_generate_prime()
    test_fermat_factor()
    test_is_composite_2()

@util.test_log
def test_factor_n():
    for n in primes._small_primes:
        m, e = primes._factor_n(n)
        assert 2**e * m == n - 1, f"_factor_n failed to factor {n} into {m} and {e}"

    for n in large_primes:
        m, e = primes._factor_n(n)
        assert (2**e) * m == n - 1, f"_factor_n failed to factor {n} into {m} and {e}"

    for n in odd_composites:
        m, e = primes._factor_n(n)
        assert (2**e) * m == n - 1, f"_factor_n failed to factor {n} into {m} and {e}"


@util.test_log
def test_fermat_is_prime():
    for n in primes._small_primes:
        assert primes._fermat_is_prime(n), f"_fermat_is_prime failed to identify {n} as prime"

    for n in odd_composites:
        assert not primes._fermat_is_prime(n), f"_fermat_is_prime failed to identify {n} as composite"

    for n in small_carmichaels:
        assert primes._fermat_is_prime(n), f"_fermat_is_prime failed to identify composite {n} as prime"

    for n in large_carmichaels:
        assert primes._fermat_is_prime(n), f"_fermat_is_prime failed to identify composite {n} as prime"

    for n in large_primes:
        assert primes._fermat_is_prime(n), f"_fermat_is_prime failed to identify {n} as prime"


@util.test_log
def test_is_prime():
    # Test smallest prime.
    assert primes.is_prime(2), "2 is a prime"

    for n in primes._small_primes:
        assert primes.is_prime(n), f"is_prime failed to identify {n} as prime"

    for n in primes._small_primes:
        n = n**2
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"

    for n in odd_composites:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"

    for n in even_composites:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"

    for n in small_carmichaels:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"

    for n in large_carmichaels:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"

    for n in large_primes:
        assert primes.is_prime(n), f"is_prime failed to identify {n} as prime"


@util.test_log
def test_generate_prime():
    for n in range(3, 12):
        p = primes.generate_prime(2**n)
        assert (
            p.bit_length() == 2**n
        ), f"expected bit length {2**n}, got {p.bit_length()}"
        assert primes.is_prime(p), f"generate_prime() returned {p}, which is not prime"


@util.test_log
def test_fermat_factor():
    i = len(primes._small_primes) // 2
    j = i
    while j < len(primes._small_primes):
        if j - i < 92:
            assert primes.fermat_factor(
                primes._small_primes[i] * primes._small_primes[j]
            )[
                0
            ], f"factors {primes._small_primes[i]} and {primes._small_primes[j]} \
should be factorable by fermat_factor()"
        else:
            assert not primes.fermat_factor(
                primes._small_primes[i] * primes._small_primes[j]
            ), f"factors {primes._small_primes[i]} and {primes._small_primes[j]} \
should not be factorable by fermat_factor()"
        i -= 1
        j += 1

    for _ in range(10):
        p = primes.generate_prime(1024)
        q = primes.generate_prime(1024)
        assert not primes.fermat_factor(
            p * q
        ), f"factors {p} and {q} should not be factorable by fermat_factor()"


@util.test_log
def test_is_composite_2():
    for n in primes._small_primes:
        assert not primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as prime"

    for n in primes._small_primes:
        n **= 2
        assert primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as composite"

    for n in odd_composites:
        assert primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as composite"

    for n in small_carmichaels:
        assert primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as composite"

    for n in large_carmichaels:
        assert primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as composite"

    for n in large_primes:
        assert not primes._is_composite_2(n), f"_is_composite_2 failed to identify {n} as prime"


if __name__ == "__main__":
    main()
