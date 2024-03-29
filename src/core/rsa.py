"""
Implementations of the Rivest-Shamir-Adleman (RSA) algorithms for digital signature and encryption.
"""

import hashlib
import random

from . import euclid
from . import primes
from . import prng
from . import util

# Allowable range, in bit lengths, of the 2 prime factors (p and q) of an RSA modulus n.
_FACTOR_MIN_BIT_LEN = 512
_FACTOR_MID_BIT_LEN = 1024
_FACTOR_MAX_BIT_LEN = 1536

# Allowable range, in bit lengths, of the RSA modulus n.
_MODULUS_MIN_BIT_LEN = _FACTOR_MIN_BIT_LEN * 2 # (1024)
_MODULUS_MID_BIT_LEN = _FACTOR_MID_BIT_LEN * 2 # (2048)
_MODULUS_MAX_BIT_LEN = _FACTOR_MAX_BIT_LEN * 2 # (3072)

# Global RSA signature-verification and encryption exponents.
VERIFICATION_EXPONENT = 3
ENCRYPTION_EXPONENT   = 5

class RSAKey:
    """
    A class representing an RSA key. This is a dual-use key, meaning that
    it can safely be used for both encryption and digital signature,
    notwithstanding the generally accepted practice of using separate keys
    for each use case. A single instance of this key can be used to (a)
    encrypt a shared key to be used by two parties in a symmetric cipher,
    and (b) digitally sign data of arbitrary type and length.

    Note that because of its dual nature, the public components of this key
    consist of a single modulus and two exponents; one for encryption and
    the other for signature verification. Further, these exponents are
    fixed integer values. Because of this, the get_public_key() method
    of this class returns just a modulus, as it is assumed users on both
    sides of a protocol using this key already know the encryption and
    verification exponents.

    Do not instantiate this class directly; instead use the rsa module
    function make_key().
    """
    def __init__(self, size: int):
        """
        Build an RSA key.
        """
        self._p, self._q, self._n, self._d_sig, self._d_dec = generate_rsa_key(size)

    @property
    def p(self) -> int:
        """
        The prime factor p of the public modulus n of this RSA key. This value
        should be kept secret by users of this class.
        """
        return self._p

    @property
    def q(self) -> int:
        """
        The prime factor q of the public modulus n of this RSA key. This value
        should be kept secret by users of this class.
        """
        return self._q

    @property
    def n(self) -> int:
        """
        The public modulus n of this RSA key. This value may be shared freely by
        users of this class.
        """
        return self._n

    @property
    def d_sig(self) -> int:
        """
        The private signature exponent d_sig of this RSA key. This value should
        be kept secret by users of this class.
        """
        return self._d_sig

    @property
    def d_dec(self) -> int:
        """
        The private decryption exponent d_dec of this RSA key. This value should
        be kept secret by users of this class.
        """
        return self._d_dec
    
    def public_key(self) -> int:
        """
        Returns the public modulus of this RSA key. This value may be shared
        freely.
        """
        return self._n

    def modulus_size(self) -> int:
        """
        Returns the size, in bits, of the public modulus of this RSA key.
        """
        return self._n.bit_length()

    def sign(self, message: object) -> bytes:
        """
        Returns the signature of the supplied message by this RSA key.
        """
        return sign(self._d_sig, self._p, self._q, message)

    def decrypt_key(self, encrypted_key: object, hash_obj=None) -> bytes:
        """
        Recovers a session key from the encrypted key supplied to this
        method, so that it may be used in a symmetric cipher to communicate
        securely with the party from whom the encrypted key was obtained. If
        present, the optional parameter hash_obj must conform to the standard
        interface for hash objects specified in the Python standard library
        module hashlib.
        """
        return decrypt_key(self._d_dec, encrypted_key, self._p, self._q, hash_obj)

    def __eq__(self, other):
        return self._p  == other._p  and\
               self._q  == other._q  and\
               self._n  == other._n  and\
               self._d_sig == other._d_sig and\
               self._d_dec == other._d_dec

    def __hash__(self):
        return hash((self._p, self._q, self._n, self._d_sig, self._d_dec))

    def __ne__(self, other):
        return not self == other


def make_key(size: int=_MODULUS_MID_BIT_LEN) -> RSAKey:
    """
    Returns a new RSA key with a modulus length of size bits. This parameter is optional (the
    default is 2048 if it is omitted).
    """
    return RSAKey(size)


def generate_rsa_key(modulus_bit_len: int) -> tuple[int, int, int, int, int]:
    """
    Returns a tuple of the form (p, q, n, d_sig, d_dec), where p and q are randomly-selected,
    distinct prime factors of size modulus_bit_len/2, n is the semiprime product of p and q
    (this is the public RSA modulus), d_sig is the modular multiplicative inverse of 3 modulo
    t, where t is the least common multiple of p-1 and q-1 (algebraically, this is
    "lcm(p-1, q-1)"), and d_dec is the modular multiplicative inverse of 5 modulo t. d_sig and
    d_dec are the exponents to be used for message signature and decryption, respectively. The
    signature-verification and encryption exponents (the constants 3 and 5, respectively),
    together with the RSA modulus n, comprise the RSA public key and may be shared freely. The
    prime factors p and q, and the signature and decryption exponents d_sig and d_dec, however,
    must be kept secret by callers of this function.
    """

    assert isinstance(modulus_bit_len, int)
    assert modulus_bit_len == _MODULUS_MIN_BIT_LEN or \
        modulus_bit_len == _MODULUS_MID_BIT_LEN or modulus_bit_len == _MODULUS_MAX_BIT_LEN

    # Compute the factors p and q of RSA modulus n.
    p, q = _generate_rsa_factors(modulus_bit_len)

    # Compute the lcm of p-1 and q-1, as its behavior will be just as correct as for the
    # totient of p*q (as specified in the original RSA paper). However, because the lcm will
    # likely be smaller, so too will the exponenents d_sig and d_dec, thus resulting in faster arithmetic.
    t = euclid.lcm(p - 1, q - 1)

    # Compute the signature and decryption exponents, d_sig and d_dec, respectively.
    d_sig = euclid.inverse(VERIFICATION_EXPONENT, t)
    d_dec = euclid.inverse(ENCRYPTION_EXPONENT, t)

    # p, q, d_sig and d_dec must be kept secret; only n (i.e., p*q), together with the signature-
    # verification and encryption exponents (the numbers 3 and 5, respectively), are part of
    # the public key. This implementation assumes a protocol will be used in which the public
    # exponents are understood by both parties to be 3 and 5 in advance, so returning them
    # here is unnecessary.
    return p, q, p * q, d_sig, d_dec


def _generate_rsa_factors(modulus_bit_len: int) -> tuple[int, int]:
    # Compute/return prime factors p and q of RSA modulus n.

    assert isinstance(modulus_bit_len, int)
    assert modulus_bit_len == _MODULUS_MIN_BIT_LEN or \
        modulus_bit_len == _MODULUS_MID_BIT_LEN or modulus_bit_len == _MODULUS_MAX_BIT_LEN

    p = _generate_rsa_prime(modulus_bit_len // 2)
    q = _generate_rsa_prime(modulus_bit_len // 2)

    # The product of two n-bit numbers will be smaller than 2n bits if one or both of the n-bit
    # factors is small enough. Whereas in principle a modulus of length 2n-1 bits is secure
    # (enough), some implementations will complain if the modulus bit length is not a multiple
    # of 8. So the trial-and-error here trades performance for compatibility/interoperability
    # with such systems.
    while (p * q).bit_length() < modulus_bit_len:
        q = _generate_rsa_prime(modulus_bit_len // 2)

    # Test for bad PRNG
    _validate_factors(p, q)

    return p, q


def _generate_rsa_prime(factor_bit_len: int) -> int:
    # Returns a prime number p, of factor_bit_len length, suitable for use as a factor in a
    # public RSA modulus. A suitable factor p is one where p is prime, and p-1 is neither a
    # multiple of 3 or 5. The latter restriction allows these small, computationally efficient
    # values to be used as exponents for signature-verification and encryption, respectively.
    # Any value returned by this function must be kept secret if it is to be used as a factor
    # in a public RSA modulus.

    assert isinstance(factor_bit_len, int)
    assert factor_bit_len == _FACTOR_MIN_BIT_LEN or \
        factor_bit_len == _FACTOR_MID_BIT_LEN or factor_bit_len == _FACTOR_MAX_BIT_LEN

    l, u = 2 ** (factor_bit_len - 1), 2**factor_bit_len - 1
    max_tries = 100 * factor_bit_len
    for tries in range(max_tries):
        # Pick a random n in the appropriate range.
        n = prng.randrange(l, u)

        # Ensure n-1 is neither a multiple of 3 or 5, so that these values can be used as
        # signature-verification and encryption exponents, respectively. n must of course
        # be prime.
        if (
            n % VERIFICATION_EXPONENT != 1
            and n % ENCRYPTION_EXPONENT != 1
            and primes.is_prime(n)
        ):
            break

    if tries == max_tries - 1:
        raise Exception("Unable to find a suitable prime")

    return n


def _validate_factors(p: int, q: int) -> None:
    if p == q:
        raise Exception("p must not equal q")
    if primes.fermat_factor(p*q):
        raise Exception("p is too close to q")


def encrypt_key(n: int, hash_obj=None) -> tuple[bytes, bytes]:
    """
    Given a public RSA key n, and a hash function provided by hash_obj (optional),
    returns a symmetric key K that is a hash of a random integer r in the range 0
    to n-1, and the ciphertext c thereof. If present, hash_obj must conform to the
    standard interface for hash objects specified in the Python standard library
    module hashlib. The function decrypt_key can be used by a receiving party to
    recover r from c, which can be re-hashed using the same hash function to recover
    K. It is assumed that both parties know this hash function in advance, and that
    knowledge of this function by an adversary in no way helps the adversary. K
    must be kept secret by callers of this function, and only c should be transmitted
    on an insecure channel.
    """

    assert isinstance(n, int)
    assert n.bit_length() == _MODULUS_MIN_BIT_LEN or \
        n.bit_length() == _MODULUS_MID_BIT_LEN or n.bit_length() == _MODULUS_MAX_BIT_LEN

    # Select a random value r in the full range of n.
    r = prng.randrange(0, n - 1)

    # Hash r; this will be the basis for the key K negotiated by both parties using a
    # symmetric cipher for message encryption (see decrypt_key).
    if hash_obj is None:
        hash_obj = hashlib.sha256()
    K = util.digest(r, hash_obj)

    # Encrypt r.
    c = util.fast_mod_exp(r, ENCRYPTION_EXPONENT, n)

    # K must be kept secret; send only the ciphertext of r (i.e., c) to the other party.
    return K, util.to_bytes(c)


def decrypt_key(d: int, c: object, p: int, q: int, hash_obj=None) -> bytes:
    """
    Given a private RSA key d, a ciphertext c, the prime factors p and q of a public RSA
    modulus n, and a hash function provided by hash_obj (optional), returns a symmetric key
    K that is identical to that returned by the function encrypt_key. If present, hash_obj
    must conform to the standard interface for hash objects specified in the Python standard
    library module hashlib. K must be kept secret by callers of this function.
    """

    assert isinstance(d, int)
    assert isinstance(p, int)
    assert isinstance(q, int)

    ci = util.to_int(c)
    assert 0 <= ci <= p * q

    # Recover r from its ciphertext c (using CRT for fast exponentiation).
    r = util.fast_mod_exp_crt(ci, d, p, q)

    # Hash r to arrive at the same key K as that computed by the encrypting party (see function
    # encrypt_key).
    if hash_obj is None:
        hash_obj = hashlib.sha256()
    K = util.digest(r, hash_obj)

    # K must be kept secret.
    return K


def sign(d: int, p: int, q: int, m: object) -> bytes:
    """
    Given a private signing key d, and the factors p and q of a public RSA modulus n,
    signs a message m and returns its signature. This function is the inverse of the function
    verify.
    """

    assert isinstance(d, int)
    assert isinstance(p, int)
    assert isinstance(q, int)

    # Map k-bit hash of m to an integer p*q (aka n) bits in length.
    s = _msg_to_rsa_number(p * q, m)

    # Sign the value using CRT for a 3- to 4-fold performance improvement (exponentiation to
    # such large exponents is otherwise costly).
    o = util.fast_mod_exp_crt(s, d, p, q)

    return util.to_bytes(o)


def verify(n: int, m: object, o: object) -> bool:
    """
    Given an RSA modulus n, a message m and a signature o, returns True if the signature
    is valid for the message m, or False otherwise. This function is the inverse of the
    function sign.
    """

    assert isinstance(n, int)

    # Map k-bit hash of m to an integer n bits in length.
    s = _msg_to_rsa_number(n, m)

    # Sign it (can't use CRT here since the verifier doesn't know the factorization of n; anyway,
    # the exponent here is the number 3).
    oi = util.fast_mod_exp(util.to_int(o), VERIFICATION_EXPONENT, n)

    # Compare.
    return oi == s


def _msg_to_rsa_number(n: int, m: object) -> int:
    # Maps a message m to an integer suitable for signing.

    assert isinstance(n, int)
    assert n.bit_length() == _MODULUS_MIN_BIT_LEN or \
        n.bit_length() == _MODULUS_MID_BIT_LEN or n.bit_length() == _MODULUS_MAX_BIT_LEN


    # Seed the PRNG with a hash of the message m (or h(m)).
    random.seed(util.digest(m, hashlib.sha256()))

    # Here we want a byte string that is always the same given the same m (and hence the same
    # h(m)). We are not interested in random data per se, but rather a deterministic mapping
    # from the 256-bit result of h(m) to an n-bit number; that is, a number in the range of
    # the modulus n (see RSA-FDH, or full-domain hash, for more information).
    xb = random.randbytes((n.bit_length() + 7) // 8)

    # Convert byte string to an integer "representative", whose bit length is in the full range
    # of the modulus n.
    # TODO: revisit endian-ness.
    xi = util.to_int(xb, byteorder="little") % n.bit_length()

    return xi
