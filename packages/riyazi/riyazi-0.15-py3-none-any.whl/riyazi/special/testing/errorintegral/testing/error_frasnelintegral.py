
import math 
from cmath import exp
from scipy import special
__all__ = ['erf','erfc','erfcx','erfi', 'erfinv','erfcinv','wofz',
'dawsn','fresnel','fresnel_zeros','modfresnelp','modfresnelm',
'voigt_profile','erf_zeros','fresnelc_zeros','fresnels_zeros']


def erf(x):
    return math.erf(x)

def erfc(x):
    return 1-erf(x)

def erfcx(x):
    return math.exp(x**2)*erfc(x)

def erfi(z):
    return (-1j*special.erf(1j*z)).real

def erfinv(x):
    pass

def erfcinv(x):
    pass 


def wofz(z):
    return exp(-z**2) * erfc(-1j*z)

def dawsn():
    pass

def fresnel():
    pass

def fresnel_zeros():
    pass

def modfresnelp():
    pass

def modfresnelm():
    pass

def voigt_profile():
    pass

def erf_zeros():
    pass

def fresnelc_zeros():
    pass

def fresnels_zeros():
    pass









