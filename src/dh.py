""" Various functions providing Diffie-Hellman symmetric key agreement. """
import primes
import secrets
import math
import time

q_bit_len = 256
min_p_bit_len = 2048
secure_random = secrets.SystemRandom()

def main():
    print("Running tests...")
    p, q, g = generate_parameters(2048)
    validate_parameters(p, q, g)
    print("validate_parameters() passed")
    
    k_priv_1, k_pub_1 = generate_keypair(g, q, p)
    validate_pub_key(k_pub_1, q, p)
    print("validate_pub_key() 1 passed")

    k_priv_2, k_pub_2 = generate_keypair(g, q, p)
    validate_pub_key(k_pub_2, q, p)
    print("validate_pub_key() 2 passed")

    k_secret1 = primes.fast_mod_exp(k_pub_2, k_priv_1, p)
    k_secret2 = primes.fast_mod_exp(k_pub_1, k_priv_2, p)

    # Keys should be hashed (see 14.6)
    assert k_secret1 == k_secret2, "Secrets don't match"
    print("Secrets match; all tests passed")

def generate_parameters(p_bit_len):
    """
    Returns the domain (i.e., public) parameters p (the modulus), q (the subgroup
    from which private exponents are selected and g (the generator of the subgroup)
    to set up symmetric key agreement between 2 parties.
    """
    assert p_bit_len >= min_p_bit_len, f"Modulus p bit-length must be >= {min_p_bit_len}"

    # Generate a 256-bit prime, which is the upper bound of the subgroup to which
    # all powers of the generator g will belong (and the subgroup from which
    # parties will select private exponents).
    q = primes.generate_prime(q_bit_len)
    
    # Find an n and p satisfying the equation p = q*n+1, where p is prime, and
    # the only non-trivial subgroup of p-1 is of size q, and consists of the elements
    # 1, ..., q-1.
    n, p = generate_p(q, p_bit_len)
    
    # Find a generator g that generates all elements of the subgroup 1, ..., q-1.
    g = generate_g(q, n, p)

    # Return the public parameters to be used by both parties for the DH setup.
    return p, q, g

def generate_p(q, p_bit_len):
    """
    Return the numbers p and n that satisfy the equation p = q*n+1, where p is prime,
    and the only non-trivial subgroup of p-1 is the size of q (the trivial subgroups
    being a) the subgroup containing the number 1, b) the subgroup consisting of 1 and
    p-1 and c) the full group of size q*n). It is to this non-trivial subgroup that any
    public parameter that is a power of the generator g (e.g. public keys) will belong.
    Since q is prime, it has no non-trivial subgroups.
    """
    # Compute lower and upper bounds from which to select a random n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    tries = 100 * math.floor(math.log2(u)+1)
    for _ in range(tries):
        while True:
            # Don't bother if n is not even (because if it is not, then p cannot be odd).
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
    Returns a generator g, which is a primitive root of the group 1, ..., q-1;
    that is, it generates every member of the group.
    """
    while True:
        a = secure_random.randrange(2, p-2)
        g = primes.fast_mod_exp(a, n, p)
        if g != 1 and primes.fast_mod_exp(g, q, p) == 1:
            break

    return g

def generate_keypair(g, q, p):
    """
    Returns a private key k_priv randomly selected from the group 1, ..., q-1, and
    a public key of the form g**k_priv % p.
    """
    k_priv = secure_random.randrange(1, q-1)
    return k_priv, primes.fast_mod_exp(g, k_priv, p)

def validate_pub_key(k, q, p):
    """
    Validates the public key.
    """
    assert 1 < k < p, f"Public key is out of range"
    assert primes.fast_mod_exp(k, q, p) == 1, f"public key is invalid"

def validate_parameters(p, q, g):
    """
    Validates the public parameters.
    """
    assert p.bit_length() >= min_p_bit_len, f"p.bit_length() {p.bit_length()} \
        is less than min_p_bit_len {min_p_bit_len}"
    assert q.bit_length() == q_bit_len, f"q.bit_length() {q.bit_length()} does \
        not equal q_bit_len {q_bit_len}"
    assert primes.is_prime(p), f"p is not prime"
    assert primes.is_prime(q), f"q is not prime"
    assert (p - 1) % q == 0, f"q is not a divisor of p-1"
    # TODO Make sure second test is not an unnecessary duplicate of the previous assert.
    assert g != 1 and primes.fast_mod_exp(g, q, p) == 1, f"g has illegal value"

if __name__ == '__main__':
    main()