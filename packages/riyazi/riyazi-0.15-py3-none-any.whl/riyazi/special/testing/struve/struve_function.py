
from math import gamma

__all__ = ['struve','modstruve',
 'itstruve0','it2struve0','itmodstruve0']


def struve(v,x):
    res = 0
    for k in range(20):
        res +=(pow(x/2,v+1)) * ( pow(-1,k)*pow(x/2,2*k)) / (gamma(k+(3/2)) * gamma(k+v+(3/2)))
    return res
 
def modstruve(v,x):
    res = 0
    for k in range(10):
        res += ( pow(x/2,v+1)) * (pow(x/2,2*k) )/ (gamma(k+(3/2))*gamma(k+v+(3/2)))
    return res


def itstruve0(x):
    pass

def it2struve0():
    pass 



def itmodstruve0():
    pass   
