#from ._trig import _sin
#from ._trig import (_sin,_cos,_tan,_csc,_sec,_cot)
from ._trig import*


__all__= [
    
    'sin','cos','tan','csc','sec','cot',
    'asin', 'acos','atan', 'acsc', 'asec', 'acot',
    'sinh','cosh','tanh','csch','sech','coth',
    'asinh','acosh','atanh','acsch','asech','acoth',

]



# Trigonometry functions  

def sin(x,/):
    """
     Return the sine of x,(measured in radians).

    >>> from riyazi import *
    >>> sin(90)
    0.8939966636005579
    >>> sin(2+1j)
    1.4031192506220405-0.48905625904129363j)
    >>> sin(3j)
    10.0178749274099j
    >>> sin(3)
    0.1411200080598672
    >>> sin(3j+3j)
    201.71315737027916j
    >>> sin(100000001)
    0.1975887055794969
    >>> sin(2+3j)
    (9.154499146911427-4.168906959966564j)
    >>> sin(inf)
    nan 


    Refrences:
    ::
    # wikipedia 
    # function.walframe 
    """

    return _sin(x)


def cos(x,/):
    """
    Return the cosine of x (measured in radians).

    >>> cos(90)
    -0.4480736161291701
    >>> cos(2+3j)
    (-4.189625690968806-9.109227893755335j)
    >>> cos(2j+3j)
    (74.20994852478783+0j)
    >>> cos(5j)
    (74.20994852478783+0j)
    >>> cos(2j-3j)
    (1.5430806348152437+0j)
    >>> cos(inf)
    nan
    
    Refrences:
    ::
    # Wikipedia 
    # function walframe

    """

    return _cos(x)



def tan(x,/):
    """
    Return the tangent of x (measured in radians).
    >>> from riyazi import *
    >>> tan(pi/3)
    1.7320508075688767
    >>> tan(2+3j)
    (-0.003764025641504106+1.0032386273536098j)
    >>> tan(-2j)
    -0.964027580075817j
    >>> tan(5j/5j)
    (1.557407724654902+0j)
    >>> tan(inf)
    nan


    Refrence:
    ::
    # Wikipedia 
    # Wolframe 

    """
    return _tan(x)


def csc(x,/):
    """
    Return the cosec of x,(measured in radians).
    >>> from riyazi import *
    >>> csc(pi/2)
    1.0
    >>> csc(2+3j)
    (0.09047320975320745+0.041200986288574146j)
    >>> csc(inf)
    nan


    Refrence:
    ::
    # Wekipedia 
    # functions Wolframe 

    """
    return  _csc(x)



def sec(x,/):
    """
    Return the sec of x,(measured in radians).
    >>> from riyazi import *
    >>> sec(pi/2)
    1.633123935319537e+16
    >>> sec(2j+3j)
    (0.01347528222130456+0j)
    >>> sec(2+3j)
    (-0.04167496441114427+0.09061113719623762j)
    >>> sec(inf)
    nan
    
    Refrence:
    ::
    # Wikepedia 
    # Wolframe 
    
    """
    return  _sec(x)
    

def cot(x,/):
    """
    Return the cot of x,(measured in radians).

    >>> from riyazi import *
    >>> cot(pi/3)
    0.577350269189626
    >>> cot(2j+3j)
    -1.0000908039820195j
    >>> cot(2+3j)
    (-0.003739710376336816-0.9967577965693584j)
    >>> cot(inf)
    nan

    Refrence :
    ::
    # Wikipedia 
    # Wolframe 

    """
    return  _cot(x)

    
# Inverse Trigonometry 


def asin(x,/):
    """
    Return  the inverse sine or arcsine of (measured in radians) of x.
   
   
    The result is between -pi/2 and pi/2.
    
    >>> from riyazi import* 
    >>> asin(-1)
    -1.5707963267948966
    >>> asin(0)
    0.0
    >>> asin(1)
    1.5707963267948966
    >>> asin(2j)
    >>> asin(2+3j)
    >>> asin(2j+3j)
    >>> asin(inf)

    Refrence:
    ::
    # Wikipedia 
    # Wolframe 

    """
    return _asin(x)


def acos(x,/):
    """
    Return the inverse cosine or arccosine (measured in radians) of x.

    The result is between 0 and pi.

    >>> from riyazi import* 
    >>> acos(-1)
    3.141592653589793
    >>> acos(0.3)
    1.2661036727794992 # here result is positive, resolve ? 
    >>> acos(1)
    0.0
    >>> acos(2+3j)
    >>> acos(2j+3j)
    >>> acos(5j)
    >>> acos(inf)

    Refrence:
    ::
    # Wikipedia 
    # Wolframe function 
    """
    return _acos(x)


def atan(x,/):
    """
    Return the inverse tangent or arctangent measured in radians) of x.
    The result is between -pi/2 and pi/2.
    
    >>> from riyazi import* 
    >>> atan(-inf) # finite value math module 
    nan
    >>> atan(-1)
    -0.7853981633974483
    >>> atan(4)
    1.3258176636680326
    >>> atan(2+3j)
    >>> atan(2j+3j)
    >>> atan(3j)
    >>> atan(-5j)


    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 

    """
    return _atan(x)



def acsc(x,/):
    """
    Return  the inverse cosecant of x
    >>> acsc(3)
    0.3398369094541219
    >>> acsc(2j)
    >>> acsc(2+3j)
    >>> acsc(2j+3j)


    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 
    """
    return _acsc(x)

def asec(x,/):
    """
    Return  the inverse secant of `x`,
    >>> asec(2)
    -1.0471975511965976
    >>> asec(2j) # Real, Imagenary 
    >>> asec(2+3j)
    >>> asec(2j+3j)
    >>> asec(inf)

    Refrence:
    ::
    # Wikipedia
    # Wolframe mathe 


    """
    return _asec(x)




def acot(x,/):
    """
    Return the inverse cotangent of x 
    >>> acot(5)
    0.19739555984988078
    >>> acot(5j)
    >>> acot(2+3j)
    >>> acot(3j+4j)
    >>> acot(inf)

    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 
    """
    return _acot(x)



# Hyperbolic Trigonometry 

 

def sinh(x,/):
    """
    Return the hyperbolic sine of x.
    >>> from riyazi import * 
    >>> sinh(0)
    0.0
    >>> sinh(1)
    1.1752011936438014
    >>> sinh(2j)
    0.9092974268256817j
    >>> sinh(2+3j)
    (-3.5905645899857794+0.5309210862485197j)
    >>> sinh(2j+3j)
    -0.9589242746631385j
    >>> sinh(+inf)
    inf
    >>> sinh(-inf)
    -inf 

    Refrence:
    :: 
    # Wikipedia 
    # Wolframe math 

    """

    return _sinh(x)





def cosh(x,/):
    """
    Computes the hyperbolic cosine of `x`

    >>> from riyazi import * 
    >>> cosh(0)
    1.0
    >>> cosh(1)
    1.5430806348152437
    >>> cosh(2j)
    (-0.4161468365471424+0j)
    >>> cosh(2+3j)
    (-3.7245455049153224+0.5118225699873845j)
    >>> cosh(2j+3j)
    (0.28366218546322625+0j)
    >>> cosh(-inf)
    -inf
    >>> cosh(inf)
    inf 
    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 

    """
    return _cosh(x)



def tanh(x,/):
    """
    Return the hyperbolic tangent of x.
    >>> from riyazi import* 
    >>> tanh(0)
    0.0
    >>> tanh(1)
    0.7615941559557649
    >>> tanh(inf)
    nan
    >>> tanh(-inf)
    nan
    >>> tanh(2+3j)
    (0.965385879022133-0.00988437503832251j)
    >>> tanh(2j)
    -2.185039863261519j
    >>> tanh(-2j)
    (-0+2.185039863261519j)
    >>> tanh(2j+3j)
    -3.380515006246586j


    Refrence:
    ::
    # Wikipedia 
    # Wolframe 

    """
    return _tanh(x)





def csch(x,/):
    """
    Return the hyperbolic cosecant of `x`,
    >>> from math import * 
    >>> csch(2)
    0.27572056477178325
    >>> csch(2j)
    -1.0997501702946164j
    >>> csch(2j+3j)
    -0+1.0428352127714058j)
    >>> csch(2+3j)
    (-0.2725486614629402-0.04030057885689153j)
    >>> csch(inf)
    0.0
    >>> csch(-inf)
    -0.0

    Refrence:
    ::
    # Wikipedia 
    # Wolframe math
    """
    return _csch(x)





def sech(x,/):
    """
    >>> from math import * 
    >>> sech(0)
    1.0
    >>> sech(2)
    0.2658022288340797
    >>> sech(-2j)
    (-2.402997961722381-0j)
    >>> sech(2+3j)
    (-0.2635129751583893-0.036211636558768516j)
    >>> sech(2j+3j)
    (3.5253200858160887+0j)
    >>> sech(5j)
    (3.5253200858160887+0j)


    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 

    
    """
    return _sech(x)





def coth(x,/):
    """
    Return  the hyperbolic cotangent of `x` 
    
    >>> from riyazi import * 
    >>> coth(pi/3)
    1.2808780710450447
    >>> coth(2+3j)
    (1.0357466377649955+0.010604783470337114j)
    >>> coth(2j+3j)
    (-0+0.2958129155327455j)
    >>> coth(inf)
    nan
    >>> coth(-inf)
    nan 

    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 

    
    """
    return _coth(x)


# Inverse Hyperbolic Trigonometry 

def asinh(x,/):
    """
    Return the inverse hyperbolic sine of x.

    >>> from riyazi import * 
    >>> asinh(0)
    0.0
    >>> asinh(2)
    1.4436354751788103
    >>> asinh(2J)
    (1.3169578969248166+1.5707963267948966j)
    >>> asinh(2+3j)
    (1.9686379257930962+0.9646585044076029j)
    >>> asinh(2j+3j)
    (2.2924316695611777+1.5707963267948966j)
    >>> asinh(-5j)
    (-2.2924316695611733-1.5707963267948937j)
    >>> asinh(inf)
    nan
    >>> asinh(-inf)
    nan 

    Refrence:
    ::

    # Wikipedia 
    # Wolframe math 

    
    """
    return _arsinh(x)




def acosh(x,/):
    """
    Return the inverse hyperbolic cosine of x.

    >>> from riyazi import* 
    >>> acosh(2)
    1.3169578969248166
    >>> acosh(2j)
    >>> acosh(2+3j)
    >>> acosh(2j+3j)
    >>> acosh(-2j)
    >>> acosh(inf)


    Refrence:
    ::
    # Wikipedia 
    # Wolframe math 
    
    """
    return _arcosh(x)




def atanh(x,/):
    """
    Return the inverse hyperbolic tangent of x.

    >>> from riyazi import* 
    >>> atanh(0.3)
    0.3095196042031118
    >>> atanh(0.9)
    1.4722194895832204
    >>> atanh(2+3j)
    >>> atanh(2j+3j)
    >>> atanh(-5j)
    >>> atanh(inf)
    nan
    >>> atanh(-inf)
    nan

    Refrence:
    :::
    # Wikipedia 
    # Wolframe math 

    
    """
    return _artanh(x)




def acsch(x,/):
    """
    Return the inverse hyperbolic cosecant of x.

    >>> from riyazi import* 
    >>> acsch(2)
    0.48121182505960347
    >>> acsch(pi/2)
    0.599971479517857
    >>> acsch(2+3j)

    >>> acsch(2j+3j)

    >>> acsch(-3j)

    >>> acsch(inf)
    0.0

    Refrence:
    ::
    # Wikipeida 
    # Wolframe math 
    """
    return _arcsch(x)



def asech(x,/):
    """
    Return   the inverse hyperbolic secant of `x`,
    
    >>> from riyazi import * 
    >>> asech(0.4)
    1.5667992369724109
    >>> asech(1)
    0.0
    >>> asech(-1) # Comples

    >>> asech(2+3j)

    >>> asech(2j)

    >>> asech(-3j)

    >>> asech(pi/3) # Complex

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return _arsech(x)


def acoth(x,/):
    """
    Return the inverse hyperbolic cotangent of `x`, 

    >>> from riyazi import* 
    >>> acoth(2)
    0.5493061443340549
    >>> acoth(pi/3)
    1.8849425394276085
    >>> acoth(2j)

    >>> acoth(3+3j)

    >>> acoth(-4j)

    >>> acoth(inf)
    nan 


    Refrence: 
    ::
    # Wikipeida 
    # Wolfram math 

    
    """
    return _arcoth(x)



