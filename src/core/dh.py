"""
An implementation of the Diffie-Hellman key agreement protocol based on
mulitplicative-group arithmetic.
"""

import hashlib

from . import primes
from . import prng
from . import util

# Bit length of a prime number q that is the order (or size) of large subgroup
# modulo p, where p is a (much larger) prime number that is the order of the full
# group modulo p.
_Q_BIT_LEN = 256

# Minimum bit length of a prime modulus p.
_P_MIN_BIT_LEN = 2048
# Maximum bit length of a prime modulus p.
_P_MAX_BIT_LEN = 3072


class DHParameters:
    """
    This class represents the public parameters of a Diffie-Hellman integer
    group. These are the group's generator (g), the group's modulus (p), and
    the order of the smallest subgroup of the entire group modulo p (q).

    Do not instantiate this class directly; instead use the dh module function
    make_parameters().
    """
    def __init__(self, size: int=_P_MIN_BIT_LEN):
        self._q, self._p, self._g = generate_parameters(size)
        validate_parameters(self._q, self._p, self._g)

    @property
    def q(self) -> int:
        """The order of this group's smallest subgroup modulo p."""
        return self._q

    @property
    def p(self) -> int:
        """This group's modulus."""
        return self._p

    @property
    def g(self) -> int:
        """This group's generator."""
        return self._g

    def __eq__(self, other):
        return self._q == other._q and\
               self._p == other._p and\
               self._g == other._g

    def __hash__(self):
        return hash((self._q, self._p, self._g))

    def __ne__(self, other):
        return not self == other

class DHKey:
    """
    This class represents a Diffie-Hellman keypair consisting of a public
    and private key.

    Do not instantiate this class directly; instead use the dh module function
    make_key().
    """
    def __init__(self, params: DHParameters):
        self._params = params
        self._x, self._y = \
            generate_keypair(self._params.q, self._params.p, self._params.g)

    def public_key(self) -> int:
        """
        Returns the public key of this keypair. This key may be shared freely.
        """
        return self._y

    def public_parameters(self) -> DHParameters:
        """
        Returns the group parameters used to derive this keypair. These
        parameters may be shared freely.
        """
        return self._params

    def size(self) -> int:
        """
        Returns the size, in bits, of this keypair (or, more specifically,
        the size of the modulus p).
        """
        return self._params.p.bit_length()

    def make_session_key(self, y: int, hash_obj=None) -> bytes:
        """
        Given a public key supplied by another party, and a hash function
        provided by hash_obj (optional), computes a shared key to be used by
        two parties in a symmetric cipher. This key must be kept secret. If
        present, hash_obj must conform to the standard interface for hash
        objects specified in the Python standard library module hashlib.
        """
        return generate_session_key( \
            y, self._x, self._params.q, self._params.p, hash_obj)

    def __eq__(self, other):
        return self._params == other._params and\
               self._x == other._x and\
               self._y == other._y

    def __hash__(self):
        return hash((self._params, self._x, self._y))

    def __ne__(self, other):
        return not self == other


def make_parameters(size: int=_P_MIN_BIT_LEN) -> DHParameters:
    """
    Returns a new DHParameters instance based on the supplied modulus size
    (the default is 2048 if none is specified). These consist of the group
    parameters required for a secure key negotiation.
    """
    return DHParameters(size)


# mypy: no_implicit_optional=False
def make_key(params: DHParameters=None) -> DHKey:
    """
    Returns a new DHKey instance consisting of a public and private key. This
    kepair will be derived from the supplied group parameters (optional). If
    no group parameters are supplied, new ones will be generated based on a
    default modulus size of 2048 bits. Note that for two parties to negotiate
    a shared symmetric key, both party's keypairs must share the same group
    parameters.
    """
    if params is None:
        return DHKey(make_parameters())
    return DHKey(params)


def generate_parameters(p_bit_len: int) -> tuple[int, int, int]:
    """
    Returns the public parameters necessary for two parties to negotiate a shared,
    private key to be used in a symmetric cipher (e.g., 3DES, AES). The returned
    value is a tuple of the form (q, p, g), where q is a 256-bit prime number that
    is the order of the smallest subgroup modulo p, p is a "safe" prime of at least
    p_bit_len length (p_bit_len must be at least 2048 bits), and g is a generator
    of the subgroup.
    """

    assert isinstance(p_bit_len, int) and \
        (p_bit_len == _P_MIN_BIT_LEN or p_bit_len == _P_MAX_BIT_LEN)

    # Generate a 256-bit prime that will be the order (or size) of a large subgroup
    # modulo p. Public keys exchanged between communicating parties must fall within
    # this subgroup.
    q = primes.generate_prime(_Q_BIT_LEN)

    # Find values for n and p that satisfy the equation p = q * n + 1, where p is a
    # prime of p_bit_len length. This ensures that the public keys used in the secret
    # key agreement will fall into the subgroup of order (or size) q. The order of
    # this subgroup must be large enough (i.e., at least 256 bits) to thwart small
    # subgroup attacks.
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

    assert isinstance(q, int) and q.bit_length() == _Q_BIT_LEN
    assert isinstance(p_bit_len, int) and \
        (p_bit_len == _P_MIN_BIT_LEN or p_bit_len == _P_MAX_BIT_LEN)

    # Compute bounds from which to select a random factor n.
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2 ** (n_bit_len - 1), 2**n_bit_len

    max_tries = 100 * p_bit_len
    for tries in range(max_tries):
        n = prng.randrange(l, u)
        # n must be even for p to be prime (and test bit length for interoperability).
        if n % 2 == 0 and (q * n).bit_length() == p_bit_len:
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

    assert isinstance(n, int) and (p - 1) % n == 0
    assert isinstance(p, int) and \
        (p.bit_length() == _P_MIN_BIT_LEN or p.bit_length() == _P_MAX_BIT_LEN)

    while True:
        # Pick a random base in the full range of the modulus.
        a = prng.randrange(2, p - 2)

        # Any such base raised to the power of n modulo p should yield either 1,
        # or else a generator of the entire subgroup of order (or size) q.
        g = util.fast_mod_exp(a, n, p)

        # If g is not 1, it must be a generator of the subgroup.
        if g != 1:
            break

    return g


def generate_keypair(q: int, p: int, g: int) -> tuple[int, int]:
    """
    Given the public parameters q, p and g (which can be obtained from this
    module's generate_parameters function), returns a tuple of the form (x,
    y), where x is a private key randomly selected from the range
    (1, ..., q-1), and y is a public key of the form g^x % p. The private
    key x returned by this function must be kept secret; whereas the public
    key y may be shared freely.
    """

    validate_parameters(q, p, g)

    # Select a random, private key in the range of 1 to q-1.
    x = prng.randrange(1, q - 1)

    # Compute a public key based on this private key.
    y = util.fast_mod_exp(g, x % q, p)

    # Validate the public key.
    validate_pub_key(y, q, p)

    return x, y


def generate_session_key(y: int, x: int, q: int, p: int, hash_obj=None) -> bytes:
    """
    Given a private key x known only to the caller of this function, a public
    key y supplied by another party, domain parameters q and p (which can be
    obtained from this module's generate_parameters function or from another
    party), and a hash function provided by hash_obj (optional), returns a hashed
    byte array suitable for use as a session key to be used by both parties in a
    symmetric cipher (e.g., 3DES, AES). If present, hash_obj must conform to the
    standard interface for hash objects specified in the Python standard library
    module hashlib. The session key returned by this function must be kept secret.
    """

    assert isinstance(y, int)
    assert isinstance(x, int)
    assert isinstance(q, int) and q.bit_length() == _Q_BIT_LEN
    assert isinstance(p, int) and \
        (p.bit_length() == _P_MIN_BIT_LEN or p.bit_length() == _P_MAX_BIT_LEN)

    # Validate supplied public key.
    validate_pub_key(y, q, p)

    # Compute a session key using the essential property of DH (i.e., by raising
    # the other party's public key to the power of this party's private key modulo p).
    ki = util.fast_mod_exp(y, x % q, p)

    # The session key is hashed to obscure any mathematical structure that could be
    # exploited by an adversary if it were to be leaked.
    if hash_obj is None:
        hash_obj = hashlib.sha256()
    return util.digest(ki, hash_obj)


def validate_pub_key(y: int, q: int, p: int) -> None:
    """
    Validates a public key y given the public parameters q and p used to generate
    it. This function must be called, without raising an exception, by a party receiving
    the public key from another party before using the public key to generate a session
    key. If this function raises an exception, the public key should be considered invalid
    and the session halted.
    """

    assert isinstance(y, int)
    assert isinstance(q, int)
    assert isinstance(p, int)

    valid = True

    # y must be in the interval [2, p-1].
    if valid and not (2 <= y <= p-1):
        valid = False

    # y must be in the subgroup of order (or size) q.
    if valid and util.fast_mod_exp(y, q, p) != 1:
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

    # The bit length of p must be equal to _P_MIN_BIT_LEN or _P_MAX_BIT_LEN
    if valid and p.bit_length() != _P_MIN_BIT_LEN and p.bit_length() != _P_MAX_BIT_LEN:
        valid = False

    # The bit length of q must be equal to _Q_BIT_LEN.
    if valid and q.bit_length() != _Q_BIT_LEN:
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

    # The order of g must be q.
    if valid and util.fast_mod_exp(g, q, p) != 1:
        valid = False

    if not valid:
        raise ValueError("Invalid parameters")
