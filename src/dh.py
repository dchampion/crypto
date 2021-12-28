""" Various functions providing Diffie-Hellman symmetric key agreement. """
import primes
import secrets
import math
import hashlib
import util

# Bit length of the largest non-trivial subgroup modulo p (where p is the
# prime modulus).
q_bit_len = 256

# Minimum bit length of the prime modulus.
min_p_bit_len = 2048

# A cryptographically secure pseudo-random number generator (PRNG) for random
# key generation.
secure_random = secrets.SystemRandom()

def generate_parameters(p_bit_len):
    """
    Returns the domain (i.e., public) parameters for the shared key negotiation.
    These are the modulus (p), the order (or size) of the only non-trivial
    subgroup modulo p (q), and a generator of that subgroup (g).
    """
    assert p_bit_len >= min_p_bit_len, f"p_bit_len must be >= {min_p_bit_len}"

    # Generate q; a 256-bit prime which will be the order (or size) of the only
    # non-trivial subgroup modulo p.
    q = primes.generate_prime(q_bit_len)
    
    # Find values n and p that satisfy the equation p = q * n + 1, where p is prime;
    # this ensures that the only non-trivial subgroup modulo p is of order q.
    n, p = generate_p(q, p_bit_len)
    
    # Find a generator g that generates all elements of the subgroup of order q.
    g = generate_g(q, n, p)

    return p, q, g

def generate_p(q, p_bit_len):
    """
    Returns the numbers p and n that satisfy the equation p = q * n + 1, where p is
    prime, and the only non-trivial subgroup modulo p is the order (size) of q (the
    trivial subgroups being a) the subgroup containing just the number 1, b) the
    subgroup consisting of 1 and p-1 and c) the full group of size q*n).
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

        if primes.is_prime(p):
            break

    return n, p

def generate_g(q, n, p):
    """
    Returns a generator g that generates the entire subgroup modulo p of order
    (or size) q.
    """
    while True:
        a = secure_random.randrange(2, p-2)
        g = util.fast_mod_exp(a, n, p)

        # TODO: Should always be 1, right?
        x = util.fast_mod_exp(g, q, p)
        assert x == 1

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

def generate_session_key(kPub, kPriv, p):
    """
    Returns a hashed byte array to be used as a session key; this key must be kept
    secret.
    """
    ki = util.fast_mod_exp(kPub, kPriv, p)
    return _hash_key(ki)

def _hash_key(k):
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
    assert p.bit_length() >= min_p_bit_len-1, f"p.bit_length() {p.bit_length()} \
is less than min_p_bit_len {min_p_bit_len}"
    assert q.bit_length() == q_bit_len, f"q.bit_length() {q.bit_length()} does \
not equal q_bit_len {q_bit_len}"
    assert primes.is_prime(p), f"p is not prime"
    assert primes.is_prime(q), f"q is not prime"
    assert (p - 1) % q == 0, f"q is not a divisor of p-1"
    assert g != 1, f"g has illegal value"
    # TODO: Necessary?
    assert util.fast_mod_exp(g, q, p) == 1, f"g has illegal value"