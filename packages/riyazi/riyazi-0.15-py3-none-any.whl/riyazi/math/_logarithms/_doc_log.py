from ._log import* 
__all__ = ['ln','log','log10','log2','log1p','logb']

def ln(x):
    """
    log(x, [base=math.e])
    Return the logarithm of x to the given base.

    If the base not specified, returns the natural logarithm 
    (base e) of x.
    
    >>>from riyazi import* 
    >>> ln(5)
    1.6094379124341003
    >>> ln(2**310)
    214.87562597358308
    >>> ln(factorial(256))

    >>> ln(2+3j)

    >>> ln(2j)

    >>> ln(-3j)

    >>> ln(-2j-3j)


    Refrence:
    ::

    # Wikipedia 

    # Wolframe 
    
    """

    return _ln(x)

def log(x):
    """
    log(x)==ln(x)
    """
    return _ln(x)




def log10(x):
    """
    Return the base 10 logarithm of x.

    >>> from riyazi import* 
    >>> log10(100)
    2.0
    >>> log10(2**310)
    93.31929865583416
    >>> log10(2+3j)

    >>> log10(2j)

    >>> log10(-3j-2j)

    >>> log10(inf)

    Refrence:
    ::

    # Wikipedia 
    # Wolframe 

    """
    return _log10(x)


def log2(x):
    """
    Return the base 2 logarithm of x.

    >>> from riyazi import* 
    >>> log2(100)
    6.6438561897747235
    >>> log2(2**310)
    309.99999999999994
    >>> log2(2+3j)

    >>> log2(2j+3j)

    >>> log2(-3j-2j)

    >>> log2(inf)

    Refrence:
    ::
    # Wikipedia
    # Wolframe mathe
    """
    return _log2(x)



def log1p(x):
    """
    Return the natural logarithm of 1+x (base e).

    The result is computed in a way which is accurate for x
    near zero
    
    >>> from riyazi import* 
    >>> log1p(100)
    4.6151205168412615
    >>> log1p(2**31)
    21.487562597823967
    >>> log1p(2+3j)

    >>> log1p(2j+3j)

    >>> log1p(-2j-3j)

    >>> log1p(inf)

    Refrence:
    ::
    # Wikipedia 

    # Wolframe 


    """
    return _log1p(x)



def logb(x,base):
    """
    doc
    """
    return _logb(x,base)





























