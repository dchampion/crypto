"""
Decorates key-generation primitives in core.dh with the high-level services of Crypto.PublicKey.DSA.
"""

from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey

from core import dh


def construct(bit_len: int) -> DsaKey:
    """
    Given the size of a prime modulus in bits (bit_len), returns a Crypto.PublicKey.DSA.DsaKey
    (see https://www.pycryptodome.org/src/public_key/dsa# for relevant documentation and examples).
    """

    dh_key = dh.make_key()
    dh_key_params = dh_key.public_parameters()

    return DSA.construct((dh_key.public_key(), \
        dh_key_params.g, dh_key_params.p, dh_key_params.q, dh_key._prv))
