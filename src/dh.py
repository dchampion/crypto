""" Various functions providing Diffie-Hellman symmetric key agreement. """
import primes
import secrets
import math
import time

q_bit_len = 256
min_p_bit_len = 2048
secure_random = secrets.SystemRandom()

def main():
    start = time.perf_counter_ns()
    p, q, g = generate_parameters(2048)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    validate_parameters(p, q, g)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)
    
    start = time.perf_counter_ns()
    k_priv_1, k_pub_1 = gen_keypair(g, q, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    validate_pub_key(k_pub_1, q, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    k_priv_2, k_pub_2 = gen_keypair(g, q, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    validate_pub_key(k_pub_2, q, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    k_secret1 = primes.fast_mod_exp(k_pub_2, k_priv_1, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    start = time.perf_counter_ns()
    k_secret2 = primes.fast_mod_exp(k_pub_1, k_priv_2, p)
    end = time.perf_counter_ns()
    print((end - start) / 1000000)

    assert k_secret1 == k_secret2 # Keys should be hashed (see 14.6)

def generate_parameters(p_bit_len):
    """
    Generates the domain (i.e., public) parameters to set up a key agreement between
    parties.
    """
    assert p_bit_len >= min_p_bit_len, f"Modulus p bit-length must be >= {min_p_bit_len}"

    # Generate a 256-bit prime
    q = primes.generate_prime(q_bit_len-1, q_bit_len)
    
    # Generate 
    n, p = generate_p(q, p_bit_len)
    g = generate_g(q, n, p)

    return p, q, g

def generate_p(q, p_bit_len):
    n_bit_len = p_bit_len - q.bit_length()
    l, u = 2**(n_bit_len-1), 2**n_bit_len

    p, n, i, tries = 4, 1, 0, 100 * math.floor(math.log2(u)+1)
    while i < tries and not primes.is_prime(p):
        i += 1
        while True:
            n = secure_random.randrange(l, u)
            if n % 2 == 0:
                break

        p = q * n + 1
        if p.bit_length() < p_bit_len:
            continue
        print(p.bit_length(), n.bit_length(), q.bit_length())

    return n, p

def generate_g(q, n, p):
    while True:
        a = secure_random.randrange(2, p - 2)
        g = primes.fast_mod_exp(a, n, p)
        if g != 1 and primes.fast_mod_exp(g, q, p) == 1:
            break

    return g

def gen_keypair(g, q, p):
    k_priv = secure_random.randrange(1, q - 1)
    return k_priv, primes.fast_mod_exp(g, k_priv, p)

def validate_pub_key(k, q, p):
    assert 1 < k < p
    assert primes.fast_mod_exp(k, q, p) == 1

def validate_parameters(p, q, g):
    assert p.bit_length() >= min_p_bit_len, f"{p.bit_length()}"
    assert q.bit_length() == q_bit_len
    assert primes.is_prime(p)
    assert primes.is_prime(q)
    assert (p - 1) % q == 0
    # TODO Make sure second test is not an unnecessary duplicate of the previous assert.
    assert g != 1 and primes.fast_mod_exp(g, q, p) == 1

def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides a, then a|p = 0) Returns 1 if a has a
        square root modulo p, -1 otherwise.
    """
    ls = primes.fast_mod_exp(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

if __name__ == '__main__':
    main()