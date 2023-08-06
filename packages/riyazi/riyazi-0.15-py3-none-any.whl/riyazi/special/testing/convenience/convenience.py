from math import pi
import math
def exp(x):
    return math.e**x

__all__ =['_cbrt', '_exp10', '_exp2','_radian','_cosdg','_sindg','_tandg','_cotdg','_log1p','_expm1','_cosm1',
'_around','_xlogy','_xlog1py','_logsumexp','_exprel','_sinc']

def _cbrt(x):
    if x<0:
        return (pow(abs(x),1/3)*(-1))
    else:
        return (pow(x,1/3))


def _exp10(x):  # *args, **kwargs
    return pow(10,x)

def _exp2(x):
    return pow(2,x)


def _radian(d,m,s):
    return (pi)* ((d+(m/60)+(s/3600))/180)


def _cosdg(x):
    if x == 90:
        return 0.0
    
    x = math.radians(x)
  
    if x is x.real:
        return ((exp(x * 1j) + exp(x * -1j)) / 2).real 
    else:
        return ((exp(x * 1j) + exp(x * -1j)) / 2)

def _sindg(x):
    x = math.radians(x)
    if x is x.real:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j).real
    else:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j)

def _tandg(x):
    if x == 90:
        return math.inf
    return (_sindg(x) / _cosdg(x))


def _cotdg(x):
    if x == 90:
        return 0.0
    return 1 / ((_sindg(x)/_cosdg(x)))

def _log1p(x):
    return (math.log(1+x))

def _expm1(x):
    return exp(x)-1

def _cosm1(x):
    return math.cos(x) - 1


def _around(x):
    return round(x)

def _xlogy(x,y):
    return x*math.log(y)

def _xlog1py(x,y):
    return _log1p(x,y)

def _logsumexp(x):
    import numpy as np 
    return np.log(np.sum(np.exp(x)))

def _exprel(x):
    return (exp(x)-1)/x

def _sinc():
    pass