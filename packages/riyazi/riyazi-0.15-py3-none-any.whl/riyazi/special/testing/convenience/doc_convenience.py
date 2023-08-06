from .convenience import* 



__all__ =['cbrt', 'exp10', 'exp2','radian','cosdg','sindg','tandg','cotdg','log1p','expm1','cosm1',
'around','xlogy','xlog1py','logsumexp','exprel','sinc']

def cbrt(x):
    """
    cbrt(x)
    Element-Wise cube root of 'x'
    
    parameters
    ----------
    x:
    `x` must contain real numbers.

    Returns
    -------
    float
        The cube root of each value in `x`.
    
    Examples
    --------
    >>> from riyazi.special import cbrt 
    >>> cbrt(8)
    2.0
    >>> cbrt(-8)
    -2.0
    >>> cbrt(27)
    3.0
    >>> cbrtt(-27)
    -3.0

    Refrence:
    ::
    # Wikipedia

    # Wolframe 


    """
    return _cbrt(x)


def exp10(x):
    """
    exp10(x)
    Compute ``10**x`` element-Wise.

    parameters
    ----------
    x:
        `x` must containt real number

    Returns
    -----
    float
        ``10**x``, Compute element-Wise.

    Examples
    --------
    >>> from riyazi.special import exp10
    >>> exp10(3)
    1000.0
    >>> exp10(-3)
    0.001
    >>> exp10(2)
    100
    >>> exp10(-2)
    0.01
    Refrence:
    ::
    # Wikipedia

    # Wolframe 
    
    """
    return _exp10


def exp2(x):
    """
    exp2(x)
    
    Compute ``2**x`` element-Wise

    parameters
    ----------
    x:
        `x` must containt real numbers.

    Returns
    ------
    float
        ``2**x``, computed element -Wise 

    Examples
    --------
    >>> from riyazi.special import exp2 
    >>> exp2(3)
    8
    >>> exp2(-3)
    0.125
    >>> exp2(2j)
    (0.18345697474330172+0.9830277404112437j)
    >>> exp2(-2j)
    (0.18345697474330172-0.9830277404112437j)
    >>> exp2(2+3j)
    (-1.947977671863125+3.493620327099486j)


    Refrence:
    ---------
    # Wikipedia
    # Wolframe 

    
    """
    return _exp2(x)


def radian(d,m,s):
    """
    
    radian(d,m,s)

    Convert from degrees to radians.

    Returns the angle given in (d)egrees, (m)inutes, and (s)econds in
    radians.
    
    Parameters
    ----------
    d : 
    Degrees, can be real-valued and imag-valued.
    m : 
    Minutes, can be real-valued and imag-valued.
    s :
    Seconds, can be real-valued and img-valued.
   
    Returns
    ------
    scalar 
        Value of the input in radians.

    Examples
    --------
    >>> import riyazi.special as rs 
    
    There are many ways to specify an angle.

    >>> rs.radian(90,0,0)
    1.5707963267948966
    >>> rs.radian(0,60*90,0)
    1.5707963267948966
    >>> rs.radian(0,0,60**2*90)
    1.5707963267948966
    >>> rs.radian()
    >>> rs.radian()

    Refrence:
    --------

    # Wikipedia
    # Wolframe 
    
    """
    return _radian(d,m,s)


def cosdg(x):
    """
    
    
    >>> from riyazi.special as rs
    >>> rs.cosdg(90)
    0.0

    Refrence:
    --------
    # Wikipedia
    # Wolframe 

    """
    return _cosdg(x)


def sindg(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.sindg(90)


    Refrence:
    ----------

    # Wikipedia
    # Wolframe 

    """
    return _sindg(x)



def tandg(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.tandg()


    Refrence:
    -------

    # Wikipedia
    # Wolframe 

    
    """
    return _tandg(x)


def cotdg(x):
    """
    >>> from riyazi.special as rs
    >>> rs.cotdg

    Refrence:
    -------

    # Wolframe
    # Wikipedia

    
    """
    return _cotdg(x)


def log1p(x):
    """
    >>> from riyazi.special as rs
    >>> rs.log1p()

    Refrence:
    ---------

    # Wolframe
    # Wikipedia

    
    """
    return _log1p(x)



def expm1(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.expm1()


    Refrence:
    -------
    # Wikipedia
    # Wolframe
    
    """
    return _expm1(x)


def cosm1(x,/):
    """
    
    >>> from riyazi.special as rs
    >>> rs.expm1()


    Refrence:
    --------

    # Wikipedia
    # Wolframe

    
    """
    return _cosm1(x)



def around(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.around(1)


    Refrence:
    ---------
    # Wikipeida
    # Wolframe 
    
    
    """
    return _around(x)



def xlogy(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.xlogy()


    Refrence:
    --------

    # Wikipedia
    # Wolframe 
    
    
    """
    return _xlogy(x)


def xlog1py(x):
    """
    
    
    >>> from riyazi.special as rs
    >>> rs.xlog1py()

    
    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    
    """
    return _xlog1py(x)



def logsumexp(x):
    """
    
    
    >>> from riyazi.special as rs
    >>> rs.logsumexp()


    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return _logsumexp(x)




def exprel(x):
    """
    
    >>> from riyazi.special as rs
    >>> rs.exprel()


    Refrence:
    ::

    # Wikipedia

    # Wolframe 
    
    
    
    """
    return _exprel(x)



def sinc(x):
    """
    
    
    >>> from riyazi.special as rs
    >>> rs.sinc()


    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    
    
    
    """
    return _sinc(x)



