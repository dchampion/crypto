import sys
sys.path.append("../src")

import primes

odd_composites = [9,15,27,35,49,133,339,589,711,999,2**521+1,2**607+1]

# Large (Mersenne) primes
large_primes =  [2**521-1,2**607-1,2**1279-1,2**2203-1,2**2281-1]

small_carmichaels = [561,1105,1729,2465,2821,6601,8911,41041,62745,63973,825265]

large_carmichaels = [((6*925968953850065)+1)*((12*925968953850065)+1)*((18*925968953850065)+1),
                     ((6*8522851273339146)+1)*((12*8522851273339146)+1)*((18*8522851273339146)+1),
                     ((6*9510693751425636)+1)*((12*9510693751425636)+1)*((18*9510693751425636)+1),
                     ((6*9510693751431925)+1)*((12*9510693751431925)+1)*((18*9510693751431925)+1),
                     ((6*9510693751446670)+1)*((12*9510693751446670)+1)*((18*9510693751446670)+1)]


def main():
    print("Running primes tests...")
    test_factor_n()
    test_fermat()
    test_is_prime()
    test_genearate_large_prime()
    print("primes tests passed")
    
def test_factor_n():    
    for n in primes.small_primes:
        mult, exp = primes.factor_n(n)
        assert (2 ** exp) * mult == n - 1, f"factor_n failed to factor {n} into {mult} and {exp}"
    print(f"factor_n passed for all {len(primes.small_primes)} \
primes <= {primes.small_primes[len(primes.small_primes)-1]}")

    for n in large_primes:
        mult, exp = primes.factor_n(n)
        assert (2 ** exp) * mult == n - 1, f"factor_n failed to factor {n} into {mult} and {exp}"
    print(f"factor_n passed for {len(large_primes)} large primes")

def test_fermat():
    for n in primes.small_primes:
        assert primes.fermat(n), f"fermat failed to identify {n} as prime"
    print(f"fermat passed for all {len(primes.small_primes)} \
primes <= {primes.small_primes[len(primes.small_primes)-1]}")

    for n in odd_composites:
        assert not primes.fermat(n), f"fermat failed to identify {n} as composite"
    print(f"fermat passed for {len(odd_composites)} odd composites")

    for n in small_carmichaels:
        assert not primes.fermat(n), f"fermat failed to identify {n} as composite"
    print(f"fermat passed with true negatives for {len(small_carmichaels)} small Carmichael numbers")

    for n in large_carmichaels:
        assert primes.fermat(n), f"fermat failed to identify {n} as composite"
    print(f"fermat passed with false positives for {len(large_carmichaels)} large Carmichael numbers")

    for n in large_primes:
        assert primes.fermat(n), f"fermat failed to identify {n} as prime"
    print(f"fermat passed for {len(large_primes)} large primes")

def test_is_prime():
    for n in primes.small_primes:
        assert primes.is_prime(n), f"is_prime failed to identify {n} as prime"
    print(f"is_prime passed for all {len(primes.small_primes)} \
primes <= {primes.small_primes[len(primes.small_primes)-1]}")

    for n in primes.small_primes:
        n = n ** 2
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"
    print(f"is_prime passed for the squares of all {len(primes.small_primes)} \
primes <= {primes.small_primes[len(primes.small_primes)-1]}")

    for n in odd_composites:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"
    print(f"is_prime passed for {len(odd_composites)} odd composites")

    for n in small_carmichaels:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"
    print(f"is_prime passed with true negatives for {len(small_carmichaels)} small Carmichael numbers")

    for n in large_carmichaels:
        assert not primes.is_prime(n), f"is_prime failed to identify {n} as composite"
    print(f"is_prime passed with true negatives for {len(large_carmichaels)} large Carmichael numbers")

    for n in large_primes:
        assert primes.is_prime(n), f"is_prime failed to identify {n} as prime"
    print(f"is_prime passed for {len(large_primes)} large primes")

def test_genearate_large_prime():
    for x in range(3, 12):
        p = primes.generate_prime(2**x)
        assert p.bit_length() == 2**x, f"expected bit length {2**x}, got {p.bit_length()}"
        assert primes.is_prime(p), f"generate_prime() returned {p}, which is not prime"
    print("generate_large_prime() passed for primes up to 2048 bits in length")

if __name__ == "__main__":
    main()