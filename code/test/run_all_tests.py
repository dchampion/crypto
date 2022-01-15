import dh_test
import euclid_test
import primes_test
import rsa_test
import util_test
import ec_test

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