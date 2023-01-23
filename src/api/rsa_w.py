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
    Crypto.PublicKey.RSA.RsaKey(s); one for encryption and the other for signing.
    (see https://www.pycryptodome.org/src/public_key/rsa# for relevant documentation and examples).
    """

    keypair = rsa.make_key()

    return RSA.construct((keypair.n, rsa.ENCRYPTION_EXPONENT,   keypair.d5, keypair.p, keypair.q)),\
           RSA.construct((keypair.n, rsa.VERIFICATION_EXPONENT, keypair.d3, keypair.p, keypair.q))
