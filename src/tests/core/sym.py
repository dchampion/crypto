"""
A symmetric, xor-based cipher that should be used only for testing the
public-key primitives in this package.
"""


def encrypt(k: object, m: object) -> bytes:
    """
    Given a key k and a message m, returns the ciphertext of m.

    Use decrypt(k, c), where k is the key passed to this function, and c
    is the ciphertext returned by this function, to recover m.

    Raises a ValueError if the bit length of m exceeds the bit length of k.
    """
    k_int = _to_int(k)
    m_int = _to_int(m)
    if k_int.bit_length() < m_int.bit_length():
        raise ValueError("Bit length of message exceeds bit length of key")

    return _to_bytes(k_int ^ m_int)


def decrypt(k: object, c: object, decode: bool=True) -> str | bytes:
    """
    Given a key k, a ciphertext c and an optional parameter decode
    (default=True), returns the plaintext of c. If decode is True, the
    return type is str; otherwise it is bytes.

    Use encrypt(k, m), where k is the key passed to this function, and m
    is the plaintext returned by this function, to encrypt m.
    """
    decrypted = encrypt(k, c)
    return decrypted if not decode else decrypted.decode("utf-8")

def _to_int(o: object) -> int:
    if isinstance(o, int):
        return o
    elif isinstance(o, bytes):
        as_int = int.from_bytes(o, byteorder="big")
    else:
        as_int = int.from_bytes(str(o).encode("utf-8"), byteorder="big")

    return as_int


def _to_bytes(as_int: int) -> bytes:
    return as_int.to_bytes((as_int.bit_length() + 7) // 8, byteorder="big")
