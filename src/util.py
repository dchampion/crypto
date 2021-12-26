""" Crypto helper functions """
import euclid

def fast_mod_exp(b, e, n):
    """
    A fast algorithm for modular exponentiation (see square-and-multiply).
    """
    assert b >= 1 and e >= 1 and n >= 1,   "b, e and n must all be > 0"

    result = b if (e & 1) else 1
    exp_bit_len = e.bit_length()

    for x in range(1, exp_bit_len):
        b = (b ** 2) % n
        if (e >> x) & 1:
            result = (result * b) % n

    return result

def fast_mod_exp_crt(b, e, p, q):
    """
    A fast algorithm for modular exponentiation, where the modulus is a large,
    semi-prime number; i.e., the product of two very large prime factors (p and q),
    the primary use-case for which is RSA. When exponentiating very large bases
    to very large powers modulo a semi-prime number, this function provides a
    factor of 3-4 time savings over fast_mod_exp.
    """
    a = fast_mod_exp(b, e % (p - 1), p)
    b = fast_mod_exp(b, e % (q - 1), q)

    return ab_to_x(a, b, p, q)

def ab_to_x(a, b, p, q):
    """
    Given a CRT representation (x mod p, x mod q) of some integer x mod pq,
    returns x mod pq (CRT -> Chinese Remainder Theorem).
    """
    inv = euclid.inverse(q, p)

    # Use Garner's formula to compute x mod pq
    return (((a - b) * inv) % p) * q + b

def x_to_ab(x, p, q):
    """
    Given some integer x mod pq, returns the CRT representation (x mod p, x mod q)
    (CRT -> Chinese Remainder Theorem).
    """
    return x % p, x % q