
from mpmath import besselj,bessely,besselk,besseli
from cmath import exp
from math import factorial,gamma

__all__ = ['jv','jve','yn','yv','yve','kn','kv','kve',
'iv','ive','hankel1','hankel1e','hankel2','hankel2e',
'wright_bessel', 'lmbda'
]


def jv(v,z):
    return besselj(v,z)

def jve(v,z):
    return jv(v, z) * exp(-abs(z.imag))

def yn(n,x):
    return bessely(n,x)


def yv(v,z):
    return bessely(v,z)

def yve(v,z):
    return yv(v, z) * exp(-abs(z.imag))


def kn(n,x):
    return besselk(n,x)


def kv(v,x):
    return besselk(v,x)

def kve(v,z):
    return kv(v, z) * exp(z)

def iv(v,z):
    return besseli(v,z)

def ive(v,z):
    return iv(v, z) * exp(-abs(z.real))


def hankel1(n,x,**kwargs):
    return besselj(n,x,**kwargs) + 1j*bessely(n,x,**kwargs)

def hankel1e(v,z):
    return hankel1(v, z) * exp(-1j * z)

def hankel2(n,x,**kwargs):
    return besselj(n,x,**kwargs) - 1j*bessely(n,x,**kwargs)

def hankel2e(v,z):
    return  hankel2(v, z) * exp(1j * z)

def wright_bessel(a,b,x):
    res =0.0
    for k in range(100):
        res += pow(x,k) / ( factorial(k)*gamma((a*k)+b))
    return res

def lmbda(v,z):
    pass


