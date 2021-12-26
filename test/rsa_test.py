import sys
sys.path.append("../src")

import rsa
import primes
import euclid

def main():
    print("Running rsa tests...")
    test_generate_rsa_prime()
    test_generate_rsa_key()
    test_encrypt_decrypt()
    test_sign_verify()
    print("rsa tests passed")

def test_generate_rsa_prime():
    for _ in range(10):
        n = rsa.generate_rsa_prime(rsa.factor_min_bit_len)
        assert primes.is_prime(n), "n is not prime"
        assert n.bit_length() == rsa.factor_min_bit_len,\
            f"expected bit length {rsa.factor_min_bit_len}, got {n.bit_length()}"
        assert n % 3 != 1, "n-1 must not be a multiple of 3"
        assert n % 5 != 1, "n-1 must not be a multiple of 5"

    print(f"generate_rsa_prime passed 10 tests using {rsa.factor_min_bit_len}-bit moduli")

def test_generate_rsa_key():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        t = euclid.lcm(p-1, q-1)
        assert primes.is_prime(p), "p is not prime"
        assert primes.is_prime(q), "q is not prime"
        assert n == p*q, "n != p*q"
        assert euclid.inverse(d3, t) == 3,\
            f"expected inverse of {d3} and {t} is 3, got {euclid.inverse(d3, t)}"
        assert euclid.inverse(d5, t) == 5,\
            f"expected inverse of {d5} and {t} is 5, got {euclid.inverse(d5, t)}"

    print(f"generate_rsa_key passed 10 tests using {rsa.modulus_min_bit_len}-bit moduli")

def test_encrypt_decrypt():
    for _ in range(10):
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        K1, c = rsa.encrypt_random_key(n, 5)
        K2 = rsa.decrypt_random_key(n, d5, c, p, q)
        assert K1 == K2, "Keys don't match"

    print(f"encrypt/decrypt_random_key passed 10 tests using {rsa.modulus_min_bit_len}-bit moduli")

def test_sign_verify():
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        p, q, n, d3, d5 = rsa.generate_rsa_key(rsa.modulus_min_bit_len)
        o = rsa.sign(n, d3, p, q, m)
        assert True == rsa.verify(n, 3, m, o)

    print(f"sign/verify passed multiple tests using {rsa.modulus_min_bit_len}-bit moduli")

if __name__ == "__main__":
    main()