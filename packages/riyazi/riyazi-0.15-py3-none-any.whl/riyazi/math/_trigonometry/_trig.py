#from cmath import sqrt,log

#import math
from .._logarithms import ln as log 
# from ..numeric import sqrt # Runtime error 7 , numpy from import 

from .._numeric.basic import sqrt 
"""
def sqrt(x):
    if(type(x) == complex):
        return (-1*x)**0.5*1j
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return x**0.5
"""
__all__=[
    
    '_sin','_cos','_tan','_csc','_sec','_cot',
    '_asin', '_acos','_atan', '_acsc', '_asec', '_acot',
    '_sinh','_cosh','_tanh','_csch','_sech','_coth',
    '_arsinh','_arcosh','_artanh','_arcsch','_arsech','_arcoth',

]



def eu():
    """
    "e()" returns the constant e.
    The value is approximately 2.7182818284590452353602874713527.
    """
    return 2.7182818284590452353602874713527

def exp(x):
    """
    "exp(x)" returns the value of e power x.
    """
    return eu()**x

def _sin(x):
    
    if x is x.real:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j).real
    else:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j)

def _cos(x):
    if x is x.real:
        return ((exp(x * 1j) + exp(x * -1j)) / 2).real 
    else:
        return ((exp(x * 1j) + exp(x * -1j)) / 2)

def _tan(x):
    return (_sin(x) / _cos(x))

def _csc(x):
    return (1 / _sin(x))

def _sec(x):
    return (1 / _cos(x))

def _cot(x):
    return (1 / _tan(x))



# Inverse Trigonometry 


def _asin(x):
    if not (-1 <= x <= 1):
        raise ValueError("math domain error not in [-1,1]")
    return (-1j * log(1j * x + sqrt(1 - (x ** 2)))).real 


def _acos(x):
    return (1j * log(x- 1j * sqrt(1 - (x ** 2)))).real #  here remove negetive 


def _atan(x):
    return (1j * (log(1 - x * 1j) - log(1 + x * 1j)) / 2).real

def divide(x,y):
    return(x/y)


def _acsc(x):
    return _asin(divide(1 , x))

def _asec(x):
    return _acos(divide(1 , x))

def _acot(x):
    return _atan(divide(1 , x))


# Hyperbolic Trigonometry 

e=2.7182818284590452353
def _sinh(x,/):
    """Return the hyperbolic sine of x."""
    x = (e**x - e**(-x))/2
    return x 


def _cosh(x,/):
    """Return the hyperbolic sine of x."""
    x = (e**x + e**(-x))/2
    return x 

def _tanh(x,/):
    x = (e**x - e**(-x)) / (e**x + e**(-x))
    return x

def _coth(x,/):
    x = (e**x + e**(-x)) / (e**x - e**(-x))
    return x

def _sech(x,/):
    x = 2/ (e**x + e**(-x)) # 1/ ((e**x + e**(-x))/2)
    return x

def _csch(x,/):
    if ( x != 0):
        x = 1 / ((e**x - e**(-x))/2)
        return x 
    else:
        print("Domain error")


# Inverse Hyperbolic Trigonometry 



def _arsinh(x,/):
    x = log(x + (x**2+1)**0.5)
    return x 


def _arcosh(x,/):
    x = log(x + (x**2-1)**0.5)
    return x 


def _artanh(x,/):
    x = 0.5 * log((1+x) / (1-x))
    return x 

def _arcoth(x,/):
    x = (1/2)* log((x+1) / (x-1))
    return x 

def _arsech(x,/):
    x = log((1+(1-x**2)**0.5) /x)
    return x 

def _arcsch(x,/):
    x = log((1/x)+ ((1/x**2)+1)**0.5)
    return x 