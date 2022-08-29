from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from src import rsa

def construct(bit_len: int) -> tuple[RsaKey, RsaKey]:

    p, q, n, d3, d5 = rsa.generate_rsa_key(bit_len)

    return RSA.construct((n, rsa.ENCRYPTION_EXPONENT, d5, p, q)),\
           RSA.construct((n, rsa.VERIFICATION_EXPONENT, d3, p, q))