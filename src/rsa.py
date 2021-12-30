""" An implementation of RSA """
import primes
import euclid
import secrets
import math
import hashlib
import util
import random

# Allowable range, in bit length, of the 2 prime factors (p and q)
# of the RSA modulus (n).
factor_min_bit_len  = 1024
factor_max_bit_len  = 4096

# Allowable range, in bit length, of the RSA modulus (n).
modulus_min_bit_len = 2048
modulus_max_bit_len = 8192

# A cryptographically secure pseudo-random number generator (PRNG).
secure_random = secrets.SystemRandom()

# A PRNG for expanding k-bit numbers to n-bit numbers, where k < n.
insecure_random = random.Random()

def generate_rsa_prime(factor_bit_len):
    """
    Returns a prime number of factor_bit_len length suitable for an RSA modulus.
    A suitable factor p is one where p is prime, and p-1 is neither a multiple of
    3 nor 5; the latter restriction to ensure these small, computationally efficient
    values can be used as exponents for signature verification and encryption,
    respectively.
    """
    assert factor_min_bit_len <= factor_bit_len <= factor_max_bit_len,\
        f"factor_bit_len must be between {factor_min_bit_len} and {factor_max_bit_len}"

    tries = 100 * factor_bit_len
    for r in range(tries):
        # This loop counter helps ensure the PRNG is producing different values;
        # namely some of them prime, and neither multiples (-1) of 3 or 5.
        assert r < tries, f"Did not find a suitable prime after {tries} tries"

        # Pick a random value in the specified range.
        n = secure_random.randrange(2**(factor_bit_len-1), 2**factor_bit_len-1)

        # Ensure n-1 is neither a multiple of 3 nor 5, so that these values can
        # be used for signature verification and encryption, respectively.
        if n % 3 != 1 and n % 5 != 1 and primes.is_prime(n):
            break

    return n

def generate_rsa_key(modulus_bit_len):
    """
    Returns parameters necessary for an RSA setup; i.e., two prime factors [p, q]
    of length modulus_bit_len/2, the product of these factors [n], which is the RSA
    modulus, the modular multiplicative inverse of 3 modulo t [d3], where t is the
    least common multiple of (p-1)(q-1), and the modular multiplicative inverse of
    5 modulo t [d5]. d3 and d5 are the signing and decryption keys, respectively.
    """
    assert modulus_min_bit_len <= modulus_bit_len <= modulus_max_bit_len,\
        f"modulus_bit_len must be between {modulus_min_bit_len} and {modulus_max_bit_len}"

    # Compute prime factors p and q.
    p = generate_rsa_prime(math.floor(modulus_bit_len//2))
    q = generate_rsa_prime(math.floor(modulus_bit_len//2))

    # Bad PRNG?
    assert p != q, "p must not equal q"

    # Compute the lcm of pq, as it will behave the same as the totient of pq
    # (see original RSA) but, because it is smaller, will result in faster
    # computations.
    t = euclid.lcm(p-1, q-1)

    # Compute the signature and decryption exponents, d3 and d5, respectively.
    d3 = euclid.inverse(3, t)
    d5 = euclid.inverse(5, t)

    # p, q, d3 and d5 must be kept secret; only n (i.e., pq), together with the
    # encryption and signature verification exponents (the numbers 5 and 3,
    # respectively), are part of the public key. This implementation assumes
    # the public exponents 3 and 5 are agreed to by both parties in advance,
    # for example as part of the key negotiation protocol, so returning them
    # here is redundant.
    return p, q, p*q, d3, d5

def encrypt_random_key(n, e):
    """
    Given a public RSA key [n, e], returns a symmetric key [K] that is a hash of a
    random value [r], and the ciphertext [c] thereof. The function decrypt_random_key
    can be used to recover r from c, and then rehashed using the same function to
    reproduce K. It is assumed that both parties, and possibly even an adversary,
    know this hash function, but such knowledge in no way helps the adversary.
    K must be kept secret, and only c should be sent over an insecure channel.
    """
    # Compute the bit length of the modulus n.
    k = math.floor(math.log2(n))

    # Select a random value [r] in the full range of n.
    r = secure_random.randrange(0, 2**k-1)

    # Hash r; this will be the basis for the key [K] negotiated by both parties
    # using a symmetric scheme for message encryption (see decrypt_random_key).
    K = hashlib.sha256(str(r).encode()).digest()

    # Encrypt r.
    c = util.fast_mod_exp(r, e, n)

    # K must be kept secret; send only the ciphertext of r [c] to the other party.
    return K, c

def decrypt_random_key(d, c, p, q):
    """
    Given a private RSA key [d, p, q], and a ciphertext [c], returns a symmetric
    key [K] that is identical to that returned by the function encrypt_random_key.
    """
    assert 0 <= c <= p*q

    # Recover r from its ciphertext c.
    r = util.fast_mod_exp_crt(c, d, p, q)

    # Hash r to arrive at the same key [K] as that computed by the encrypting party
    # (see function encrypt_random_key).
    K = hashlib.sha256(str(r).encode()).digest()

    # K must be kept secret.
    return K

def msg_to_rsa_number(n, m):
    """
    Maps a message m to an integer suitable for signing.
    """
    # Seed the PRNG with a hash of the message [m] (or h(m)).
    insecure_random.seed(hashlib.sha256(str(m).encode()).digest())

    # Compute the bit length of the modulus [n].
    k = math.floor(math.log2(n))

    # Here we want a byte string that is always the same given the same m (and
    # hence the same h(m)). We are not interested in random data per se, but
    # rather a deterministic mapping from the 256-bit result of h(m) to an n-bit
    # number; that is, a number in the range of the modulus [n] (see RSA-FDH,
    # or full-domain hash, for more information).
    xb = insecure_random.randbytes(math.ceil(k//8))

    # Convert byte string to an integer "representative", whose bit length is
    # in the full range of the modulus [n].
    xi = int.from_bytes(xb, byteorder="little") % 2**k

    return xi

def sign(n, d, p, q, m):
    """
    Given a public modulus [n], a private signing key [d], and the private factors
    of n [p and q], signs a message [m] and returns its signature. This function is
    the inverse of the function verify.
    """
    # Map k-bit hash of m to an integer n bits in length.
    s = msg_to_rsa_number(n, m)

    # Sign the value using the CRT version of util.fast_mod_exp for a 3- to 4-fold
    # time savings (exponentiation by such a large exponent is otherwise costly).
    o = util.fast_mod_exp_crt(s, d, p, q)

    return o

def verify(n, e, m, o):
    """
    Given a public modulus and exponent [n, e], a message [m] and a signature [o],
    returns True if the signature is valid for the message m, or False otherwise.
    This function is the inverse of the function sign.
    """
    # Map k-bit hash of m to an integer n bits in length.
    s = msg_to_rsa_number(n, m)

    # Sign it (can't use CRT here since the verifier doesn't know the factorization
    # of n; anyway, the exponent is the number 3).
    o1 = util.fast_mod_exp(o, e, n)

    # Compare.
    return o1 == s