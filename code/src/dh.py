""" An implementation of Diffie-Hellman """
import primes
import secrets
import hashlib
import util

# Bit length of a large subgroup modulo p (where p is the prime DH modulus).
q_bit_len = 256

# Minimum bit length of the prime DH modulus.
min_p_bit_len = 2048

def generate_parameters(p_bit_len):
    """
    Returns the domain (i.e., public) parameters [q, p, g] required for two
    parties to negotiate a shared, private key to be used to encrypt data using
    a symmetric cipher (e.g., AES). These are the order (or size) of a large
    subgroup modulo p [q], the modulus [p], and a generator of the subgroup
    modulo p [g].
    """
    assert isinstance(p_bit_len, int) and p_bit_len >= min_p_bit_len

    # Generate q; a 256-bit prime, which will be the order (or size) of a
    # large subgroup modulo p within which the public keys exchanged between
    # communicating parties must fall.
    q = primes.generate_prime(q_bit_len)
    
    # Find values for n and p that satisfy the equation p = q * n + 1, where
    # p (a p_bit_len prime), will serve as the DH modulus. This ensures that
    # the public keys used in the secret key agreement will fall into the
    # subgroup of order (or size) q. The order of this subgroup must be large
    # (256 bits, to provide 128-bit security) in order to thwart collision-
    # style attacks.
    n, p = _generate_p(q, p_bit_len)

    # Find a generator g that generates all elements of the subgroup of order
    # (or size) q.
    g = _generate_g(n, p)

    return q, p, g

def _generate_p(q, p_bit_len):
    """
    Returns positive integers [n, p] that satisfy the equation p = q * n + 1, where
    p will serve as a prime modulus of length p_bit_len. The value n returned from
    this function will be used as input to the computation of a generator of the
    subgroup modulo p that is of order (or size) q.
    """
    assert isinstance(q, int) and q.bit_length() >= q_bit_len
    assert isinstance(p_bit_len, int) and p_bit_len >= min_p_bit_len

    # Compute bounds from which to select a random factor n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    secure_random = secrets.SystemRandom()
    tries = 100 * p_bit_len
    for i in range(tries):
        n = secure_random.randrange(l, u)
        p = q * n + 1
        if primes.is_prime(p):
            break

    if i == tries - 1:
        raise Exception("Unable to generate a suitable prime")

    return n, p

def _generate_g(n, p):
    """
    Returns a generator g that generates the entire subgroup modulo p of order
    (or size) q.
    """
    assert isinstance(p, int) and p.bit_length() >= min_p_bit_len - 1
    assert isinstance(n, int) and (p - 1) % n == 0

    secure_random = secrets.SystemRandom()
    while True:
        # Pick a random base in the full range of the modulus.
        a = secure_random.randrange(2, p-2)

        # Any such base raised to the power of n modulo p should yield either 1,
        # or a generator of the entire subgroup of order (or size) q.
        g = util.fast_mod_exp(a, n, p)

        # If g is not 1, it must be a generator of the subgroup.
        if g != 1:
            break

    return g

def generate_keypair(q, p, g):
    """
    Returns a private key randomly selected from the set (1, ..., q-1), and a
    public key of the form (g**k_prv) % p, where g is the generator of the subgroup
    modulo p of order (or size) q. The private key k_prv returned by this function
    must be kept secret.
    """
    _validate_parameters(q, p, g)

    # Select a random, private key in the range of q.
    secure_random = secrets.SystemRandom()
    k_prv = secure_random.randrange(1, q-1)

    # Compute a public key based on this private key.
    k_pub = util.fast_mod_exp(g, k_prv, p)

    # Validate the publid key.
    validate_pub_key(k_pub, q, p)

    return k_prv, k_pub

def generate_session_key(k_pub, k_prv, p):
    """
    Returns a hashed byte array to be used as a session key in a symmetric cipher
    agreed upon by both parties in the setup phase. This key must be kept secret.
    """
    assert isinstance(k_pub, int)
    assert isinstance(k_prv, int)
    assert isinstance(p, int) and p.bit_length() >= min_p_bit_len - 1

    # Compute a session key using the essential property of DH (i.e., raising
    # the other party's public key to the power of this party's private key modulo p).
    ki = util.fast_mod_exp(k_pub, k_prv, p)

    # The session key is hashed in order to obscure any mathematical structure
    # in ki that could be exploited by an adversary if it were to be leaked.
    return _hash_key(ki)

def _hash_key(k):
    """
    Returns a hashed byte array of the positive integer k.
    """
    assert isinstance(k, int)

    return hashlib.sha256(str(k).encode()).digest()

def validate_pub_key(k, q, p):
    """
    Validates a public key k given the public parameters q and p. Must be called,
    without raising an exception, by a receiving party before proceding with a session.
    If this function raises an exception, the public key is invalid and the protocol should
    be halted.
    """
    assert isinstance(k, int)
    assert isinstance(q, int)
    assert isinstance(p, int)

    # Check that
    # (1) k is in range, and
    # (2) k is in the subgroup of order (or size) q.
    valid = False
    if 1 < k < p and\
       util.fast_mod_exp(k, q, p) == 1:
        valid = True

    if not valid:
        raise Exception("Invalid key")

def _validate_parameters(q, p, g):
    """
    Validates the public parameters [q, p, g]. Must be called, without raising
    an exception, by a receiving party before proceeding with a session. If this
    function raises an exception, the parameters are invalid and the protocol should
    be halted.
    """
    assert isinstance(q, int)
    assert isinstance(p, int)
    assert isinstance(g, int)

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