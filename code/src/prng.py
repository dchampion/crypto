""" A cryptographically strong pseudo-random number generator (PRNG). """
import secrets

# TODO: Flesh this thing out, and then use it for all the implementations in
# this repo.

def randbits(k):
    return secrets.randbits(k)