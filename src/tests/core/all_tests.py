""" Tests all functions in all modules of core. """

from . import dh_test
from . import euclid_test
from . import ec_test
from . import primes_test
from . import rsa_test
from . import util_test


def main():
    dh_test.main()
    ec_test.main()
    euclid_test.main()
    primes_test.main()
    rsa_test.main()
    util_test.main()


if __name__ == "__main__":
    main()
