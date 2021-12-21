""" Various functions providing Diffie-Hellman symmetric key agreement. """
import primes
import secrets
import math
import hashlib
import util

q_bit_len = 256
min_p_bit_len = 2048
secure_random = secrets.SystemRandom()

def main():
    print("Running tests...")
    p, q, g = generate_parameters(2048)
    validate_parameters(p, q, g)
    print("validate_parameters passed")
    
    k_priv_1, k_pub_1 = generate_keypair(g, q, p)
    validate_pub_key(k_pub_1, q, p)
    print("validate_pub_key 1 passed")

    k_priv_2, k_pub_2 = generate_keypair(g, q, p)
    validate_pub_key(k_pub_2, q, p)
    print("validate_pub_key 2 passed")

    k_secret1 = util.fast_mod_exp(k_pub_2, k_priv_1, p)
    k_secret2 = util.fast_mod_exp(k_pub_1, k_priv_2, p)
    assert k_secret1 == k_secret2, "Secrets don't match"

    k_hashed1 = hash_key(k_secret1)
    k_hashed2 = hash_key(k_secret2)
    assert k_hashed1 == k_hashed2, "Hashed secrets don't match"
    print("secrets match")

    print("all tests passed")

def generate_parameters(p_bit_len):
    """
    Returns the domain (i.e., public) parameters of the Diffie-Hellman setup.
    These are p, the modulus; q, the order (size) of the the only non-trivial
    subgroup modulo p; and g, a generator of that subgroup.
    """
    assert p_bit_len >= min_p_bit_len, f"Modulus p bit-length must be >= {min_p_bit_len}"

    # Generate q; a 256-bit prime which is the order of the only non-trivial
    # subgroup modulo p.
    q = primes.generate_prime(q_bit_len)
    
    # Find an n and p satisfying the equation p = q*n+1, where p is prime, and
    # the only non-trivial subgroup modulo p is of order q.
    n, p = generate_p(q, p_bit_len)
    
    # Find a generator g that generates all elements of the subgroup modulo p
    # of order q.
    g = generate_g(q, n, p)

    return p, q, g

def generate_p(q, p_bit_len):
    """
    Return the numbers p and n that satisfy the equation p = q*n+1, where p is prime,
    and the only non-trivial subgroup modulo p is the order (size) of q (the trivial
    subgroups being a) the subgroup containing just the number 1, b) the subgroup
    consisting of 1 and p-1 and c) the full group of size q*n). Since q is prime,
    q itself has no non-trivial subgroups.
    """
    # Compute bounds from which to select a random n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    tries = 100 * math.floor(math.log2(u)+1) # TODO: Find a better estimate for tries.
    for _ in range(tries):
        while True:
            # Don't bother if n is not even, because if it is not, then p cannot be odd
            # (and even numbers can't be prime).
            n = secure_random.randrange(l, u)
            if n % 2 == 0:
                break

        p = q * n + 1

        # In addition to primality, check p for bit-length, as it might be less than
        # that requested if n is small enough.
        if p.bit_length() == p_bit_len and primes.is_prime(p):
            break
        
    return n, p

def generate_g(q, n, p):
    """
    Returns a generator g that generates the entire subgroup modulo p of order (size) q.
    """
    while True:
        a = secure_random.randrange(2, p-2)
        g = util.fast_mod_exp(a, n, p)
        #x = util.fast_mod_exp(g, q, p)
        #assert x == 1
        # TODO: Should always be 1, right?
        if g != 1: # and util.fast_mod_exp(g, q, p) == 1:
            break

    return g

def generate_keypair(g, q, p):
    """
    Returns a private key k_priv randomly selected from the set (1, ..., q-1), and
    a public key of the form g**k_priv % p.
    """
    k_priv = secure_random.randrange(1, q-1)
    return k_priv, util.fast_mod_exp(g, k_priv, p)

def hash_key(k):
    """
    Returns the input k (a large integer key) as a hashed byte array.
    """
    return hashlib.sha256(str(k).encode()).digest()

def validate_pub_key(k, q, p):
    """
    Validates the public key k.
    """
    assert 1 < k < p, f"Public key is out of range"
    assert util.fast_mod_exp(k, q, p) == 1, f"public key is invalid"

def validate_parameters(p, q, g):
    """
    Validates the public parameters p, q and g.
    """
    assert p.bit_length() >= min_p_bit_len, f"p.bit_length() {p.bit_length()} \
is less than min_p_bit_len {min_p_bit_len}"
    assert q.bit_length() == q_bit_len, f"q.bit_length() {q.bit_length()} does \
not equal q_bit_len {q_bit_len}"
    assert primes.is_prime(p), f"p is not prime"
    assert primes.is_prime(q), f"q is not prime"
    assert (p - 1) % q == 0, f"q is not a divisor of p-1"
    assert g != 1, f"g has illegal value"
    #assert util.fast_mod_exp(g, q, p) == 1, f"g has illegal value"

if __name__ == '__main__':
    main()