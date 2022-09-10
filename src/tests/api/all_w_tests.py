""" Tests all functions in all modules of api. """

from . import dh_w_test
from . import rsa_w_test
from . import ec_w_test


def main():
    """Test all modules in api."""
    print("Running all tests...")
    dh_w_test.main()
    rsa_w_test.main()
    ec_w_test.main()
    print("all tests passed")


if __name__ == "__main__":
    main()
