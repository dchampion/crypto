"""
A symmetric cipher that should be used for only for testing the public-key primitives in
this package.
"""


def encrypt(k, m):
    """
    Given a key k and a message m, returns the ciphertext of m. Use m = decrypt(k, c),
    where k is key passed to this function, and c is the ciphertext returned by this
    function, to recover m.
    """
    return _to_int(k) ^ _to_int(m)


def decrypt(k, c):
    """
    Given a key k and a ciphertext c, returns the plaintext of c. Use c = encrypt(k, m),
    where k is the key passed to this function, and m is the plaintext returned by this
    function, to encrypt m.
    """
    return _to_str(_to_int(k) ^ c)


def _to_int(s):
    s_bytes = s if isinstance(s, bytes) else str(s).encode("utf-8")
    return int.from_bytes(s_bytes, byteorder="big")


def _to_str(i):
    i_bytes = i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")
    return i_bytes.decode("utf-8").lstrip("\x00")
