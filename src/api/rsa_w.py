"""
Decorates key-generation primitives in core.rsa with the high-level services of
Crypto.PublicKey.RSA.
"""

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from core import rsa


def construct(bit_len: int) -> tuple[RsaKey, RsaKey]:
    """
    Given the size of an RSA modulus in bits (bit_len), returns a pair of
    Crypto.PublicKey.RSA.RsaKey(s); one for signing and the other for encryption.
    (see https://www.pycryptodome.org/src/public_key/rsa# for relevant documentation and examples).
    """

    p, q, n, d3, d5 = rsa._generate_rsa_key(bit_len)

    return RSA.construct((n, rsa.ENCRYPTION_EXPONENT, d5, p, q)), RSA.construct(
        (n, rsa.VERIFICATION_EXPONENT, d3, p, q)
    )
