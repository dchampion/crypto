"""
Decorates key-generation primitives in core.dh with the high-level services of Crypto.PublicKey.DSA.
"""

from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey

from core import dh


def construct(bit_len: int=2048) -> DsaKey:
    """
    Given the size of a prime modulus in bits (bit_len), returns a Crypto.PublicKey.DSA.DsaKey
    (see https://www.pycryptodome.org/src/public_key/dsa# for relevant documentation and examples).
    """

    dh_parameters = dh.make_parameters(bit_len)
    dh_key = dh.make_key(dh_parameters)

    return DSA.construct((dh_key.public_key(), \
        dh_parameters.g, dh_parameters.p, dh_parameters.q, dh_key._prv))
