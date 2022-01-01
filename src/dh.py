""" Various functions providing Diffie-Hellman symmetric key agreement. """
import primes
import secrets
import math
import hashlib
import util

# Bit length of a large subgroup modulo p (where p is the prime DH modulus).
q_bit_len = 256

# Minimum bit length of the prime DH modulus.
min_p_bit_len = 2048

def generate_parameters(p_bit_len):
    """
    Returns the domain (i.e., public) parameters [p, q, g] for the shared,
    symmetric (private) key negotiation. These are the modulus [p], the
    order (or size) of a large subgroup modulo p [q], and a generator of
    that subgroup [g].
    """
    assert p_bit_len >= min_p_bit_len, f"p_bit_len must be >= {min_p_bit_len}"

    # Generate q; a 256-bit prime, which will be the order (or size) of a
    # large subgroup modulo p within which the public keys exchanged between
    # communicating parties will fall.
    q = primes.generate_prime(q_bit_len)
    
    # Find values for n and p that satisfy the equation p = q * n + 1, where
    # p (a p_bit_len prime), will serve as the DH modulus. This ensures that
    # the public keys used in the secret key agreement will fall into the
    # subgroup of order (or size) q. The order of this subgroup must be large
    # (256 bits, to provide 128-bit security) in order to thwart collision-
    # style attacks.
    n, p = generate_p(q, p_bit_len)

    # Find a generator g that generates all elements of the subgroup of order
    # (or size) q.
    g = generate_g(n, p)

    return p, q, g

def generate_p(q, p_bit_len):
    """
    Returns the numbers [n, p] that satisfy the equation p = q * n + 1, where p is
    a prime DH modulus of length p_bit_len, and n will be used in the computation
    of a generator of the subroup modulo p that is of order (or size) q (see
    function genetate_g).
    """
    # Compute bounds from which to select a random factor n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    secure_random = secrets.SystemRandom()
    tries = 100 * math.floor(math.log2(u)+1) # TODO: Find a better estimate for tries.
    for i in range(tries):
        while True:

            # If n is not even, try again (because p cannot then be odd in the
            # equation p = q * n + 1).
            n = secure_random.randrange(l, u)
            if n % 2 == 0:
                break

        p = q * n + 1
        if primes.is_prime(p):
            break

    assert i < tries-1, "unable to generate a suitable prime"

    return n, p

def generate_g(n, p):
    """
    Returns a generator [g] that generates the entire subgroup modulo p of order
    (or size) q.
    """
    secure_random = secrets.SystemRandom()
    while True:
        # Pick a random base in the full range of the modulus.
        a = secure_random.randrange(2, p-2)

        # Any such base raised to the power of n modulo p should yield either 1,
        # or a generator of the entire group of order (or size) q.
        g = util.fast_mod_exp(a, n, p)

        # If g is not 1, it must be a generator of the subgroup.
        if g != 1:
            break

    return g

def generate_keypair(g, q, p):
    """
    Returns a private key randomly selected from the set (1, ..., q-1), and a
    public key of the form (g**kPriv) % p, where g is the generator of the subgroup
    modulo p of order (or size) q. The private key [kPriv] returned by this function
    must be kept secret.
    """
    # Select a random, private key in the range of q.
    secure_random = secrets.SystemRandom()
    kPriv = secure_random.randrange(1, q-1)

    # Compute a public key based on this private key.
    kPub = util.fast_mod_exp(g, kPriv, p)

    # Validate the publid key.
    validate_pub_key(kPub, q, p)

    return kPriv, kPub

def generate_session_key(kPub, kPriv, p):
    """
    Returns a hashed byte array to be used as a session key in a symmetric cipher
    that is agreed upon by both parties in the setup phase. This key must be kept
    secret.
    """
    # Compute a session key using the essential property of DH (i.e., raising
    # the other communicant's public key to the power of this communicant's
    # private key modulo p).
    ki = util.fast_mod_exp(kPub, kPriv, p)

    # The session key is hashed in order to obscure any mathematical structure
    # in ki that could be exploited by an attacker if it were to be leaked.
    return _hash_key(ki)

def _hash_key(k):
    """
    Returns the input k (a large integer) as a hashed byte array.
    """
    return hashlib.sha256(str(k).encode()).digest()

def validate_pub_key(k, q, p):
    """
    Validates the public key k. Must be called without raising an exception
    by a receiving party before proceding with a session.
    """
    # Check that
    # (1) k is in range, and
    # (2) k is in the subgroup of order (or size) q.
    valid = False
    if 1 < k < p and\
       util.fast_mod_exp(k, q, p) == 1:
        valid = True

    if not valid:
        raise Exception("Invalid key")

def validate_parameters(p, q, g):
    """
    Validates the public parameters [p, q, g]. Must be called without raising
    an exception by a receiving party before proceeding with a session.
    """

    # Check that
    # (1) the bit length of the modulus [p] is as big as that requested,
    # (2) the bit length of [q] (the order of the subgroup modulo p within
    # which public keys must fall) is big enough,
    # (3) p is prime,
    # (4) q is prime,
    # (5) q is a divisor of p-1,
    # (6) the generator [g] is not 1, and
    # (7) (g**q) % p is 1

    valid = False
    if p.bit_length() >= min_p_bit_len-1 and\
       q.bit_length() == q_bit_len and\
       primes.is_prime(p) and\
       primes.is_prime(q) and\
       (p - 1) % q == 0 and\
       g != 1 and\
       util.fast_mod_exp(g, q, p) == 1:
        valid = True

    if not valid:
        raise Exception("Invalid parameters")