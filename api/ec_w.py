from Crypto.PublicKey import ECC

from src import curves
from src import ec

supported = (curves.Secp192r1.__name__,
             curves.Secp224r1.__name__,
             curves.Secp256r1.__name__,
             curves.Secp384r1.__name__,
             curves.Secp521r1.__name__)

def construct(curve: curves.Curve):
    if type(curve).__name__ not in supported:
        raise ValueError(f"Curve {type(curve).__name__} not supported.")

    ec.new_curve(curve)
    d, Q = ec.generate_keypair()

    return ECC.construct(curve=type(curve).__name__.lower(), d=d, seed=None, point_x=Q[0], point_y=Q[1])