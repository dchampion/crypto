""" Euclidean algorithms and support functions. """

def gcd(a: int, b: int) -> int:
    """Returns the greatest common divisor (or gcd) of positive
    integers a and b."""
    _validate_params(a, b)

    while b:
        a, b = b, a % b

    return a


def _gcd(a: int, b: int) -> int:
    """
    Returns the greatest common divisor (or gcd) of positive
    integers a and b. Note this function uses recursion, which
    can cause stack overflow if its inputs a and/or b are too large.
    A safer alternative is to use gcd(a,b) instead.
    """
    _validate_params(a, b)

    if b == 0:
        return a

    return _gcd(b, a % b)


def gcdx(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns the greatest common divisor (or gcd) of positive
    integers a and b, and the x and y solutions for the relation
    ax + by = gcd(a,b) (see Bezout's identity).
    """
    _validate_params(a, b)

    a1, b1, x, y = 1, 0, 1, 0
    while b:
        q = a // b
        a, b = b, a - q * b

        x, b1 = b1, x - q * b1
        y, a1 = a1, y - q * a1

    return a, x, y


def _gcdx(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns the greatest common divisor (or gcd) of positive integers
    a and b, and the x and y solutions for the relation ax + by = gcd(a,b)
    (see Bezout's identity). Note this function uses recursion, which can
    cause stack overflow if its inputs a and/or b are too large. A safer
    alternative is to use gcdx(a,b) instead.
    """
    _validate_params(a, b)

    if a == 0:
        return b, 0, 1

    gcd_var, x, y = _gcdx(b % a, a)

    x, y = y - (b // a) * x, x

    return gcd_var, x, y


def lcm(a: int, b: int) -> int:
    """Returns the least common multiple (or lcm) of positive integers
    a and b."""
    _validate_params(a, b)

    return (a * b) // gcd(a, b)


def inverse(a: int, b: int) -> int:
    """
    Returns the modular multiplicative inverse of a modulo b, where
    a and b are positive integers; if no such inverse exists, raises a
    ValueError.
    """
    _validate_params(a, b)

    gcd_var, x, _ = gcdx(a, b)
    if gcd_var != 1:
        err_str = f"{a} has no inverse modulo {b}"
        raise ValueError(err_str)

    return x % b


def _validate_params(a: int, b: int) -> None:
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert a >= 0
    assert b >= 0
