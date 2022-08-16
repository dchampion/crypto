"""
An implementation of the Diffie-Hellman key agreement protocol based on
mulitplicative-group arithmetic.
"""

import primes
import util
import prng

# Bit length of a prime number q that is the order (or size) of large subgroup
# modulo p, where p is a (much larger) prime number that is the order of the full
# group modulo p.
_q_bit_len = 256

# Minimum bit length of a prime modulus p.
_p_min_bit_len = 2048

def generate_parameters(p_bit_len: int) -> tuple[int, int, int]:
    """
    Returns the public parameters necessary for two parties to negotiate a shared,
    private key to be used in a symmetric cipher (e.g., 3DES, AES). The returned
    value is a tuple of the form (q, p, g), where q is a 256-bit prime number that
    is the order of the smallest subgroup modulo p, p is a prime number of at least
    p_bit_len length (p_bit_len must be at least 2048 bits), and g is a generator
    of the subgroup of order q.
    """

    assert isinstance(p_bit_len, int) and p_bit_len >= _p_min_bit_len

    # Generate a 256-bit prime that will be the order (or size) of a large subgroup
    # modulo p. Public keys exchanged between communicating parties must fall within
    # this subgroup.
    q = primes.generate_prime(_q_bit_len)
    
    # Find values for n and p that satisfy the equation p = q * n + 1, where p is a
    # prime of p_bit_len length. This ensures that the public keys used in the secret
    # key agreement will fall into the subgroup of order (or size) q. The order of
    # this subgroup must be large enough (i.e., at least 256 bits) to thwart collision-
    # style attacks.
    n, p = _generate_p(q, p_bit_len)

    # Find a generator g that generates all elements of the subgroup of order
    # (or size) q.
    g = _generate_g(n, p)

    return q, p, g

def _generate_p(q: int, p_bit_len: int) -> tuple[int, int]:
    # Returns positive integers n and p which satisfy the equation p = q * n + 1,
    # where q is a 256-bit prime, and p is a p_bit_len prime. The value n returned from
    # this function will be used to find a generator of the subgroup modulo p that is
    # of order (or size) q.

    assert isinstance(q, int) and q.bit_length() >= _q_bit_len
    assert isinstance(p_bit_len, int) and p_bit_len >= _p_min_bit_len

    # Compute bounds from which to select a random factor n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    max_tries = 100 * p_bit_len
    for tries in range(max_tries):
        n = prng.randrange(l, u)
        if n % 2 == 0: # n must be even for p to be prime, so skip if n is odd.
            p = q * n + 1
            if primes.is_prime(p):
                break

    if tries == max_tries - 1:
        raise Exception("Unable to generate a suitable prime")

    return n, p

def _generate_g(n: int, p: int) -> int:
    # Returns a generator g that generates the entire subgroup modulo p of order
    # (or size) q, where p is a prime of at least 2048 bits in length, and q is a 256-
    # bit prime.

    assert isinstance(p, int) and p.bit_length() >= _p_min_bit_len - 1
    assert isinstance(n, int) and (p - 1) % n == 0

    while True:
        # Pick a random base in the full range of the modulus.
        b = prng.randrange(2, p-2)

        # Any such base raised to the power of n modulo p should yield either 1,
        # or else a generator of the entire subgroup of order (or size) q.
        g = util.fast_mod_exp(b, n, p)

        # If g is not 1, it must be a generator of the subgroup.
        if g != 1:
            break

    return g

def generate_keypair(q: int, p: int, g: int) -> tuple[int, int]:
    """
    Given the public parameters q, p and g (which can be obtained from this
    module's generate_parameters function), returns a tuple of the form (k_prv,
    k_pub), where k_prv is a private key randomly selected from the range
    (1, ..., q-1), and k_pub is a public key of the form g^k_prv % p. The
    private key k_prv returned by this function must be kept secret; whereas
    the public key k_pub may be shared freely.
    """

    validate_parameters(q, p, g)

    # Select a random, private key in the range of 1 to q-1.
    k_prv = prng.randrange(1, q-1)

    # Compute a public key based on this private key.
    k_pub = util.fast_mod_exp(g, k_prv % q, p)

    # Validate the public key.
    validate_pub_key(k_pub, q, p)

    return k_prv, k_pub

def generate_session_key(k_pub: int, k_prv: int, q: int, p: int) -> bytes:
    """
    Given a private key k_prv known only to the caller of this function, a public
    key k_pub supplied by another party, and domain parameters q and p (which can
    be obtained from this module's generate_parameters function, or from another
    party), returns a hashed byte array suitable for use as a session key to be
    used by both parties in a symmetric cipher (e.g., 3DES, AES). The session key
    returned by this function must be kept secret.
    """

    assert isinstance(k_pub, int)
    assert isinstance(k_prv, int)
    assert isinstance(p, int) and p.bit_length() >= _p_min_bit_len - 1
    assert isinstance(q, int) and q.bit_length() == _q_bit_len

    # Compute a session key using the essential property of DH (i.e., by raising
    # the other party's public key to the power of this party's private key modulo p).
    ki = util.fast_mod_exp(k_pub, k_prv % q, p)

    # The session key is hashed to obscure any mathematical structure that could be
    # exploited by an adversary if it were to be leaked.
    return util.hash(ki)

def validate_pub_key(k_pub: int, q: int, p: int) -> None:
    """
    Validates a public key k_pub given the public parameters q and p used to generate
    it. This function must be called, without raising an exception, by a party receiving
    the public key from another party before using the public key to generate a session
    key. If this function raises an exception, the public key should be considered invalid
    and the session halted.
    """

    assert isinstance(k_pub, int)
    assert isinstance(q, int)
    assert isinstance(p, int)

    valid = True

    # k_pub must be in the interval [2, p-1].
    if valid and k_pub <= 1 or k_pub >= p:
        valid = False

    # k_pub must be in the subgroup of order (or size) q.
    if valid and util.fast_mod_exp(k_pub, q, p) != 1:
        valid = False

    if not valid:
        raise ValueError("Invalid key")

def validate_parameters(q: int, p: int, g: int) -> None:
    """
    Validates the public parameters q, p and g returned from the function generate_parameters,
    or supplied to the caller by another party. If this function raises an exception, the
    parameters should be considered invalid and the session halted.
    """

    assert isinstance(q, int)
    assert isinstance(p, int)
    assert isinstance(g, int)

    valid = True

    # The bit length of modulus p must be greater than _p_min_bit_len - 1
    # (multiplication of 2 x-bit integers can produce a (2x-1)-bit result).
    if valid and p.bit_length() < _p_min_bit_len - 1:
        valid = False

    # The bit length of q must be equal to _q_bit_len.
    if valid and q.bit_length() != _q_bit_len:
        valid = False

    # p must be prime.
    if valid and not primes.is_prime(p):
        valid = False

    # q must be prime.
    if valid and not primes.is_prime(q):
        valid = False

    # q must divide p - 1.
    if valid and (p - 1) % q != 0:
        valid = False

    # g cannot be 1.
    if valid and g == 1:
        valid = False

    # The order of g must must be q.
    if valid and util.fast_mod_exp(g, q, p) != 1:
        valid = False

    if not valid:
        raise ValueError("Invalid parameters")