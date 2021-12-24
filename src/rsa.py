""" An implementation of RSA """
import primes
import euclid
import secrets
import math
import hashlib
import util
import random

factor_min_bit_len  = 1024
factor_max_bit_len  = 4096
modulus_min_bit_len = 2048
modulus_max_bit_len = 8192

secure_random = secrets.SystemRandom()
insecure_random = random.Random()

def main():
    print("Running tests...")
    ### Begin tests for generate_rsa_prime
    for i in range(10):
        n = generate_rsa_prime(factor_min_bit_len)
        assert primes.is_prime(n), "n is not prime"
        assert n.bit_length() == factor_min_bit_len,\
            f"expected bit length {factor_min_bit_len}, got {n.bit_length()}"
        assert n % 3 != 1, "n-1 must not be a multiple of 3"
        assert n % 5 != 1, "n-1 must not be a multiple of 5"
    print(f"generate_rsa_prime passed 10 tests using {factor_min_bit_len}-bit factors")
    ### End tests for generate_rsa_prime

    ### Begin tests for generate_rsa_key
    for _ in range(10):
        p, q, n, d3, d5 = generate_rsa_key(modulus_min_bit_len)
        t = euclid.lcm(p-1, q-1)
        assert primes.is_prime(p), "p is not prime"
        assert primes.is_prime(q), "q is not prime"
        assert n == p*q, "n != p*q"
        assert euclid.inverse(d3, t) == 3,\
            f"expected inverse of {d3} and {t} is 3, got {euclid.inverse(d3, t)}"
        assert euclid.inverse(d5, t) == 5,\
            f"expected inverse of {d5} and {t} is 5, got {euclid.inverse(d5, t)}"
    print(f"generate_rsa_key passed 10 tests using {modulus_min_bit_len}-bit moduli")
    ### End tests for generate_rsa_prime

    ### Begin tests for encrypt_random_key and decrypt_random_key
    for _ in range(10):
        p, q, n, d3, d5 = generate_rsa_key(modulus_min_bit_len)
        K1, c = encrypt_random_key(n, 5)
        K2 = decrypt_random_key(n, d5, c, p, q)
        assert K1 == K2, "Keys don't match"
    print(f"encrypt/decrypt_random_key passed 10 tests using {modulus_min_bit_len}-bit moduli")
    ### End tests for encrypt_random_key and decrypt_random_key

    ### Begin tests for sign and verify
    for m in ["When", "in", "the", "course", "of", "human", "events..."]:
        p, q, n, d3, d5 = generate_rsa_key(modulus_min_bit_len)
        o = sign(n, d3, p, q, m)
        assert True == verify(n, 3, m, o)
    print(f"sign/verify passed multiple tests using {modulus_min_bit_len}-bit moduli")
    ### End tests for sign and verify

    print("all tests passed")

def generate_rsa_prime(factor_bit_len):
    """
    Returns a prime factor of factor_bit_len length suitable for an RSA modulus.
    A suitable factor p is one where p is prime, and p-1 is neither a multiple of
    3 nor 5; the latter is necessary to ensure these values can be used as exponents
    for signing and encryption, respectively.
    """
    
    assert factor_min_bit_len <= factor_bit_len <= factor_max_bit_len,\
        f"bit_len must be between {factor_min_bit_len} and {factor_max_bit_len}"

    tries = 100 * factor_bit_len
    for r in range(tries):
        # This loop counter helps ensure the PRNG is producing different values;
        # namely some of them prime, and neither multiples (-1) of 3 or 5.
        assert r < tries, f"Did not find a suitable prime after {tries} tries"
        
        n = secure_random.randrange(2**(factor_bit_len-1), 2**factor_bit_len-1)
        
        # Ensure n-1 is neither a multiple of 3 nor 5, so that
        # these values can be used for signing and encryption, respectively.
        if n % 3 != 1 and n % 5 != 1 and primes.is_prime(n):
            break

    return n

def generate_rsa_key(modulus_bit_len):
    """
    Returns parameters necessary for an RSA setup; i.e., two prime factors p and q
    of length modulus_bit_len / 2, the product of these factors n, the modular
    multiplicative inverse of 3 modulo t (t being the least common multiple of
    (p-1)(q-1)), and the modular multiplicative inverse of 5 modulo t.
    """
    assert modulus_min_bit_len <= modulus_bit_len <= modulus_max_bit_len,\
        f"modulus_bit_len must be between {modulus_min_bit_len} and {modulus_max_bit_len}"

    # Compute factors p and q.
    p = generate_rsa_prime(math.floor(modulus_bit_len//2))
    q = generate_rsa_prime(math.floor(modulus_bit_len//2))

    # Bad PRNG?
    assert p != q, "p must not equal q"

    # Compute the lcm of pq, as it will behave the same as the totient
    # of pq but, because it is smaller, with better performance.
    t = euclid.lcm(p-1, q-1)

    # Compute the signing and encryption exponents.
    d3 = euclid.inverse(3, t)
    d5 = euclid.inverse(5, t)

    return p, q, p*q, d3, d5

def encrypt_random_key(n, e):
    """
    Given a public RSA key (n, e), returns a symmetric key K that is a hash of
    a random value r, and the ciphertext c thereof. The function decrypt_random_key
    can be used to recover r from c, and then rehashed using the same function to
    reproduce K.
    """
    
    k = math.floor(math.log2(n))
    r = secure_random.randrange(0, 2**k-1)
    
    K = hashlib.sha256(str(r).encode()).digest()
    c = util.fast_mod_exp(r, e, n)
    
    return K, c

def decrypt_random_key(n, d, c, p, q):
    """
    Given a private RSA key (n, d), and a ciphertext c, returns a symmetric key K
    that is identical to that returned by the function encrypt_random_key
    """
    assert 0 <= c <= n

    m = util.fast_mod_exp_crt(c, d, p, q)
    K = hashlib.sha256(str(m).encode()).digest()

    return K

def msg_to_rsa_number(n, m):
    """
    Maps a message m to an integer suitable for signing.
    """
    # Seed the PRNG with a hash of the message m, or h(m).
    insecure_random.seed(hashlib.sha256(str(m).encode()).digest())

    # Compute the bit length of of the modulus n.
    k = math.floor(math.log2(n))

    # Here we want a byte string that is the same given the same
    # m, and hence the same h(m). We are not interested in random
    # data per se, but rather a deterministic mapping from the 256-
    # bit result of h(m) to an n-bit number; that is, a number the
    # size of the RSA modulus n (see RSA-FDH, or full-domain hash).
    xb = insecure_random.randbytes(math.ceil(k//8))

    # Convert bytes to an integer "representative" whose bit length
    # is equal to that of the modulus n.
    xi = int.from_bytes(xb, "little")
    return xi % (2**k)

def sign(n, d, p, q, m):
    """
    Given a public modulus n, a private signing key d, and the private factors
    of n (p,q), signs a message m and returns the signature.
    """
    s = msg_to_rsa_number(n, m)
    o = util.fast_mod_exp_crt(s, d, p, q)

    return o

def verify(n, e, m, o):
    """
    Given a public modulus and exponent (n,e), a message m and a signature o,
    returns True if the signature is valid for the message m, or False otherwise.
    """
    s = msg_to_rsa_number(n, m)
    o1 = util.fast_mod_exp(o, e, n)

    return o1 == s

if __name__ == "__main__":
    main()