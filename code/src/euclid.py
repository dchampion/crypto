""" Euclidean algorithms and support functions. """

def swap(a, b):
    """ Returns positive integers a and b in increasing order. """
    _validate_params(a, b)

    if a > b:
        return b, a
    return a, b

def gcd(a, b):
    """ Returns the greatest common divisor (or gcd) of positive
    integers a and b. """
    _validate_params(a, b)

    while b != 0:
        a, b = swap(a, b)
        b = b % a

    return a

def _gcd(a, b):
    """
    Returns the greatest common divisor (or gcd) of positive
    integers a and b. Note this function uses recursion, which
    can cause stack overflow if its inputs a and/or b are too large.
    A safer alternative is to use gcd(a,b) instead.
    """
    _validate_params(a, b)

    if b == 0:
        return a
    
    a, b = swap(a, b)

    return gcd(a, b % a)

def gcdx(a, b):
    """
    Returns the greatest common divisor (or gcd) of positive
    integers a and b, and the x and y solutions for the relation
    ax = bx = gcd(a,b) (see Bezout's identity).
    """
    _validate_params(a, b)

    a, b = swap(a, b)

    a1, b1, x1, y1 = 1, 0, 1, 0
    while b != 0:
        q = a // b
        temp = b

        b = a - q * b
        a = temp

        temp = a1
        a1 = y1 - q * a1
        y1 = temp

        temp = b1
        b1 = x1 - q * b1
        x1 = temp

    return a, x1, y1

def _gcdx(a, b):
    """
    Returns the greatest common divisor (or gcd) of positive integers
    a and b, and the x and y solutions for the relation ax = bx = gcd(a,b)
    (see Bezout's identity). Note this function uses recursion, which can
    cause stack overflow if its inputs a and/or b are too large. A safer
    alternative is to use gcdx(a,b) instead.
    """
    _validate_params(a, b)

    if b == 0:
        return a, 0, 1
    
    a, b = swap(a, b)

    gcd, x1, y1 = gcdx(a, b % a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

def lcm(a, b):
    """ Returns the least common multiple (or lcm) of positive integers
    a and b. """
    _validate_params(a, b)

    return (a*b) // gcd(a, b)

def inverse(a, b):
    """
    Returns the modular multiplicative inverse of a modulo b, where
    a and b are positive integers; if no such inverse exists, raises an
    exception.
    """
    _validate_params(a, b)

    gcd, x, y = gcdx(a, b)
    if gcd != 1:
        err_str = "a has no inverse modulo b"
        raise Exception(err_str)
    
    inverse = x if a < b else y

    return (inverse % b + b) % b

def _validate_params(a, b):
    assert isinstance(a, int)
    assert isinstance(b, int)