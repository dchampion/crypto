import badkeys

from api import ec_w
from core import curves

_CURVES = (
    curves.Secp192r1.__name__.lower(),
    curves.Secp224r1.__name__.lower(),
    curves.Secp256r1.__name__.lower(),
    curves.Secp384r1.__name__.lower(),
    curves.Secp521r1.__name__.lower(),
)


def main():
    print("Running ec_w tests...")
    test_pubkeys()
    print("All ec_w tests passed")


def test_pubkeys():
    for curve in _CURVES:
        ec_key = ec_w.construct(curve)

        key_info = badkeys.detectandcheck(ec_key.public_key().export_key(format="PEM"))
        assert not key_info.get("results"), f"{key_info.get('results')}"


if __name__ == "__main__":
    main()
