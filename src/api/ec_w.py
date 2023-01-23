"""
Decorates key-generation primitives in core.ec with the high-level services of Crypto.PublicKey.ECC.
"""

from Crypto.PublicKey import ECC
from Crypto.PublicKey.ECC import EccKey

from core import curves
from core import ec


def construct(curve: str) -> EccKey:
    """
    Given a supported elliptic curve (i.e., any of the curves derived from verifiably random
    seeds in the ECC table in https://www.pycryptodome.org/src/public_key/ecc#), returns a
    Crypto.PublicKey.ECC.EccKey.
    """

    ec.new_curve(_from_str(curve))
    keypair = ec.make_key()

    return ECC.construct(curve=curve, d=keypair.d, point_x=keypair.Q.x, point_y=keypair.Q.y)


def _from_str(as_str: str) -> curves.Curve:

    curve = None

    match as_str:
        case "NIST P-192" | "p192" | "P-192" | "prime192v1" | "secp192r1":
            curve = curves.Secp192r1()
        case "NIST P-224" | "p224" | "P-224" | "prime224v1" | "secp224r1":
            curve = curves.Secp224r1()
        case "NIST P-256" | "p256" | "P-256" | "prime256v1" | "secp256r1":
            curve = curves.Secp256r1()
        case "NIST P-384" | "p384" | "P-384" | "prime384v1" | "secp384r1":
            curve = curves.Secp384r1()
        case "NIST P-521" | "p521" | "P-521" | "prime521v1" | "secp521r1":
            curve = curves.Secp521r1()

    if curve is None:
        raise ValueError(
            f"Curve {as_str} not supported. See https://www.pycryptodome.org/src/public_key/ecc# for valid strings"
        )

    return curve
