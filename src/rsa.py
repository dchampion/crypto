""" An implementation of RSA """
import primes
import euclid
import math
import hashlib
import util
import random
import prng

# Allowable range, in bit length, of the 2 prime factors (p and q) of an RSA modulus n.
_factor_min_bit_len  = 1024
_factor_max_bit_len  = 4096

# Allowable range, in bit length, of the RSA modulus n.
_modulus_min_bit_len = _factor_min_bit_len*2
_modulus_max_bit_len = _factor_max_bit_len*2

# Global RSA signature-verification and encryption exponents.
_VERIFICATION_EXPONENT = 3
_ENCRYPTION_EXPONENT   = 5

def _generate_rsa_prime(factor_bit_len: int) -> int:
    # Returns a prime number p, of factor_bit_len length, suitable for use as a factor in a
    # public RSA modulus. A suitable factor p is one where p is prime, and p-1 is neither a
    # multiple 3 or 5. The latter restriction allows these small, computationally efficient
    # values to be used as exponents for signature-verification and encryption, respectively.
    # Any value returned by this function must be kept secret if it is to be used as a factor
    # in a public RSA modulus.

    assert isinstance(factor_bit_len, int)
    assert _factor_min_bit_len <= factor_bit_len <= _factor_max_bit_len

    l, u = 2**(factor_bit_len-1), 2**factor_bit_len-1
    tries = 100 * factor_bit_len
    for r in range(tries):
        # Pick a random n in the appropriate range.
        n = prng.randrange(l, u)

        # Ensure n-1 is neither a multiple of 3 or 5, so that these values can be used as
        # signature-verification and encryption exponents, respectively. n must of course
        # be prime.
        if n % _VERIFICATION_EXPONENT != 1\
             and n % _ENCRYPTION_EXPONENT != 1 and primes.is_prime(n):
            break

    if r == tries - 1:
        raise Exception("Unable to find a suitable prime")

    return n

def generate_rsa_key(modulus_bit_len: int) -> tuple[int, int, int, int, int]:
    """
    Returns a tuple of the form (p, q, n, d3, d5), where p and q are randomly-selected, distinct
    prime factors of size modulus_bit_len/2, n is the semiprime product of p and q (this is
    the public RSA modulus), d3 is the modular multiplicative inverse of 3 modulo t, where t is
    the least common multiple of p-1 and q-1 (algebraically, this is "lcm(p-1, q-1)"), and d5 is
    the modular multiplicative inverse of 5 modulo t. d3 and d5 are the exponents to be used for
    message signature and decryption, respectively. The signature-verification and encryption
    exponents (3 and 5, respectively), together with the RSA modulus n, comprise the RSA public
    key and may be shared freely. The prime factors p and q, and the signature and decryption
    exponents d3 and d5, however, must be kept secret.
    """

    assert isinstance(modulus_bit_len, int)
    assert _modulus_min_bit_len <= modulus_bit_len <= _modulus_max_bit_len

    # Compute prime factors p and q.
    p = _generate_rsa_prime(math.floor(modulus_bit_len//2))
    q = _generate_rsa_prime(math.floor(modulus_bit_len//2))

    # Test for bad PRNG
    _validate_factors(p, q)

    # Compute the lcm of p-1 and q-1, as its behavior will be just as correct as for the
    # totient of p*q (as specified in the original RSA paper). However, because the lcm will
    # likely smaller, so too will the exponenents d3 and d5, resulting in faster exponentiations.
    t = euclid.lcm(p-1, q-1)

    # Compute the signature and decryption exponents, d3 and d5, respectively.
    d3 = euclid.inverse(_VERIFICATION_EXPONENT, t)
    d5 = euclid.inverse(_ENCRYPTION_EXPONENT, t)

    # p, q, d3 and d5 must be kept secret; only n (i.e., p*q), together with the signature-
    # verification and encryption exponents (the numbers 3 and 5, respectively), are part of
    # the public key. This implementation assumes a protocol will be used in which the public
    # exponents are understood by both parties to be 3 and 5 in advance, so returning them
    # here is unnecessary.
    return p, q, p*q, d3, d5

def _validate_factors(p: int, q: int) -> None:
    assert p != q, "p must not equal q"
    assert not primes.fermat_factor(p*q), "p is too close to q"

def encrypt_random_key(n: int, e: int) -> tuple[bytes, int]:
    """
    Given a public RSA key, consisting of a modulus n and an encryption exponent e, returns
    a symmetric key K that is a hash of a random integer r, and the ciphertext thereof c.
    The function decrypt_random_key can be used by a receiving party to recover r from c,
    and then rehashed using the same function to recover K. It is assumed that both parties
    know this hash function in advance, and that knowledge of this function by an adversary
    in no way helps the adversary. K must be kept secret by callers of this function, and only
    c be sent to another party over an insecure channel.
    """

    assert isinstance(n, int) and n.bit_length() >= _modulus_min_bit_len - 1
    assert isinstance(e, int)

    # Select a random value r in the full range of n.
    r = prng.randrange(0, n-1)

    # Hash r; this will be the basis for the key K negotiated by both parties using a
    # symmetric cipher for message encryption (see decrypt_random_key).
    K = util.hash(r)

    # Encrypt r.
    c = util.fast_mod_exp(r, e, n)

    # K must be kept secret; send only the ciphertext of r (i.e., c) to the other party.
    return K, c

def decrypt_random_key(d: int, c: int, p: int, q: int) -> bytes:
    """
    Given a private RSA key d, p and q, and a ciphertext c, returns a symmetric key K that
    is identical to that returned by the function encrypt_random_key. K must be kept secret by
    callers of this function.
    """

    assert isinstance(d, int)
    assert isinstance(c, int)
    assert isinstance(p, int)
    assert isinstance(q, int)
    assert 0 <= c <= p*q

    # Recover r from its ciphertext c.
    r = util.fast_mod_exp_crt(c, d, p, q)

    # Hash r to arrive at the same key K as that computed by the encrypting party (see function
    # encrypt_random_key).
    K = hashlib.sha256(str(r).encode()).digest()

    # K must be kept secret.
    return K

def _msg_to_rsa_number(n: int, m: int) -> int:
    # Maps a message m to an integer suitable for signing.

    assert isinstance(n, int) and n.bit_length() >= _modulus_min_bit_len - 1

    # Seed the PRNG with a hash of the message m (or h(m)).
    random.seed(hashlib.sha256(str(m).encode()).digest())

    # Here we want a byte string that is always the same given the same m (and hence the same
    # h(m)). We are not interested in random data per se, but rather a deterministic mapping
    # from the 256-bit result of h(m) to an n-bit number; that is, a number in the range of
    # the modulus n (see RSA-FDH, or full-domain hash, for more information).
    xb = random.randbytes(math.ceil(n.bit_length()//8))

    # Convert byte string to an integer "representative", whose bit length is in the full range
    # of the modulus n.
    xi = int.from_bytes(xb, byteorder="little") % n.bit_length()

    return xi

def sign(d: int, p: int, q: int, m: int) -> int:
    """
    Given a private signing key d, and the private factors of a public modulus p and q,
    signs a message m and returns its signature. This function is the inverse of the function
    verify.
    """

    assert isinstance(d, int)
    assert isinstance(p, int)
    assert isinstance(q, int)

    # Map k-bit hash of m to an integer p*q (aka n) bits in length.
    s = _msg_to_rsa_number(p*q, m)

    # Sign the value using the CRT version of util.fast_mod_exp for a 3- to 4-fold performance
    # improvement (exponentiation to such large exponents is otherwise costly).
    o = util.fast_mod_exp_crt(s, d, p, q)

    return o

def verify(n: int, e: int, m: int, o: int) -> bool:
    """
    Given a public modulus n and exponent e, a message m and a signature o, returns True
    if the signature is valid for the message m, or False otherwise. This function is the
    inverse of the function sign.
    """

    assert isinstance(n, int)
    assert isinstance(e, int)
    assert isinstance(o, int)

    # Map k-bit hash of m to an integer n bits in length.
    s = _msg_to_rsa_number(n, m)

    # Sign it (can't use CRT here since the verifier doesn't know the factorization of n; anyway,
    # the exponent here is the number 3).
    o1 = util.fast_mod_exp(o, e, n)

    # Compare.
    return o1 == s