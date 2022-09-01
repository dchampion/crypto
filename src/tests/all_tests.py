from . import dh_test
from . import euclid_test
from . import ec_test
from . import primes_test
from . import rsa_test
from . import util_test

def main():
    print("Running all tests...")
    dh_test.main()
    euclid_test.main()
    primes_test.main()
    rsa_test.main()
    util_test.main()
    ec_test.main()
    print("all tests passed")

if __name__ == "__main__":
    main()