import sys
sys.path.append("../src")

import dh
import util

def main():
    print("Running dh tests...")
    test_dh_setup()
    print("dh tests passed")
    
def test_dh_setup():
    p, q, g = dh.generate_parameters(2048)
    dh.validate_parameters(p, q, g)
    
    k_priv_1, k_pub_1 = dh.generate_keypair(g, q, p)
    dh.validate_pub_key(k_pub_1, q, p)

    k_priv_2, k_pub_2 = dh.generate_keypair(g, q, p)
    dh.validate_pub_key(k_pub_2, q, p)

    k_secret1 = util.fast_mod_exp(k_pub_2, k_priv_1, p)
    k_secret2 = util.fast_mod_exp(k_pub_1, k_priv_2, p)
    assert k_secret1 == k_secret2, "Secrets don't match"

    k_hashed1 = dh.hash_key(k_secret1)
    k_hashed2 = dh.hash_key(k_secret2)
    assert k_hashed1 == k_hashed2, "Hashed secrets don't match"

    print("dh setup passed")

if __name__ == "__main__":
    main()