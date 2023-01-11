"""
A symmetric, xor-based cipher that should be used for only for testing
the public-key primitives in this package.
"""


def encrypt(k: bytes, m: object) -> int:
    """
    Given a key k and a message m, returns the ciphertext of m.

    Use decrypt(k, c), where k is key passed to this function, and c is
    the ciphertext returned by this function, to recover m.

    If the bit length of the message m exceeds that of the key k, raises
    a ValueError.
    """
    k_int = _to_int(k)
    m_int = _to_int(m)
    if k_int.bit_length() < m_int.bit_length():
        raise ValueError("Bit length of message exceeds bit length of key")

    return k_int ^ m_int


def decrypt(k: bytes, c: int, decode: bool=True) -> str | bytes:
    """
    Given a key k, a ciphertext c, and an optional boolean parameter
    decode (default=True), returns the plaintext of c. The return type
    is str if decode is True; otherwise the return type is bytes.

    Use encrypt(k, m), where k is the key passed to this function, and
    m is the plaintext returned by this function, to encrypt m.
    """
    as_bytes = _to_bytes(_to_int(k) ^ c)
    return as_bytes.decode("utf-8") if decode else as_bytes

def _to_int(s: object) -> int:
    s_bytes = s if isinstance(s, bytes) else str(s).encode("utf-8")
    return int.from_bytes(s_bytes, byteorder="big")


def _to_bytes(i: int) -> bytes:
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")
