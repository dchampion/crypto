""" Tests all functions in all modules of api. """

from . import dh_w_test
from . import rsa_w_test
from . import ec_w_test


def main():
    dh_w_test.main()
    rsa_w_test.main()
    ec_w_test.main()


if __name__ == "__main__":
    main()
