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
    m_bytes = str(m).encode("utf-8")
    m_int = int.from_bytes(m_bytes, byteorder="big")
    k_bytes = k if isinstance(k, bytes) else str(k).encode("utf-8")
    k_int = int.from_bytes(k_bytes, byteorder="big")
    return k_int ^ m_int

def decrypt(k, c):
    """
    Given a key k and a ciphertext c, returns the plaintext of c. Use c = encrypt(k, m),
    where k is the key passed to this function, and m is the plaintext returned by this
    function, to encrypt m.
    """
    k_bytes = k if isinstance(k, bytes) else str(k).encode("utf-8")
    k_int = int.from_bytes(k_bytes, byteorder="big")
    d = k_int ^ c
    d_bytes = d.to_bytes((c.bit_length()+7) // 8, byteorder="big")
    d_str = d_bytes.decode("utf-8").lstrip("\x00")
    return d_str