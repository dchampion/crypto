from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey

from src import dh

def construct(bit_len: int) -> DsaKey:
    """
    Given the size of a prime modulus in bits (bit_len), returns a Crypto.PublicKey.DSA.DsaKey
    (see https://www.pycryptodome.org/src/public_key/dsa# for relevant documentation and examples).
    """

    q, p, g = dh.generate_parameters(bit_len)
    k_prv, k_pub = dh.generate_keypair(q, p, g)

    return DSA.construct((k_pub, g, p, q, k_prv))