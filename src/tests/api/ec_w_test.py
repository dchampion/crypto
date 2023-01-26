import badkeys

from api import ec_w
from core import curves
from tests.core import util

_CURVES = (
    curves.Secp192r1.__name__.lower(),
    curves.Secp224r1.__name__.lower(),
    curves.Secp256r1.__name__.lower(),
    curves.Secp384r1.__name__.lower(),
    curves.Secp521r1.__name__.lower(),
)


@util.test_log
def main():
    test_pubkeys()


@util.test_log
def test_pubkeys():
    for curve in _CURVES:
        ec_key = ec_w.construct(curve)

        key_info = badkeys.detectandcheck(ec_key.public_key().export_key(format="PEM"))
        assert not key_info.get("results"), f"{key_info.get('results')}"


if __name__ == "__main__":
    main()
