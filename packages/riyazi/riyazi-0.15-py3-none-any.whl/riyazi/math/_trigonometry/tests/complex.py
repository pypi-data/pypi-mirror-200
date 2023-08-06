def e() -> float:
    """
    "e()" returns the constant e.
    The value is approximately 2.7182818284590452353602874713527.
    """
    return 2.7182818284590452353602874713527

def exp(x):
    """
    "exp(x)" returns the value of e power x.
    """
    return e() ** x

def sin(z):
    return ((exp(z*1j) - exp(z*(-1j))) / 2j)

def cos(z):
    return (exp(z * 1j) + exp(z * -1j)) / 2

def tan(z):
    return (sin(z) / cos(z))

def csc(z):
    return (1 / sin(z))

def sec(z):
    return (1 / cos(z))

def cot(z):
    return (1 / tan(z))
