from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey

from src import dh

def construct(bit_len: int) -> DsaKey:
    q, p, g = dh.generate_parameters(bit_len)
    k_prv, k_pub = dh.generate_keypair(q, p, g)

    return DSA.construct((k_pub, g, p, q, k_prv))