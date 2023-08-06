from itertools import count, islice
import numpy as np 
from numpy import isscalar
from math import sin,log,sqrt
from scipy.integrate import quad 
import numpy as np
from math import factorial as _factorial

__all__=['agm','bernoulli','binom','diric','euler',
'expn','exp1','expi','factorial','factorial2','factorialk',
'shichi','sici','softmax','log_softmax','spence','zeta','zetac']


# https://en.wikipedia.org/wiki/Arithmetic%E2%80%93geometric_mean

def agm(a,b):
    a, b = (a+b)/2, sqrt(a*b)
    return sqrt(a*b)

# https://en.wikipedia.org/wiki/Bernoulli_number
def bernoulli(n):
   pass


def binom(n, k):
    v = 1
    for i in range(k):
        v *= (n - i) / (i + 1)
    return v

def diric(x,n):
    return sin(x * n/2) / (n * sin(x / 2))


def euler(n):
    pass




# https://en.wikipedia.org/wiki/List_of_integrals_of_exponential_functions


def expn():
    pass


def exp1(z):
    pass


def expi(x, minfloat=1e-7, maxfloat=10000):
    """Ei integral function."""
    minfloat = min(np.abs(x), minfloat)
    maxfloat = max(np.abs(x), maxfloat)
    def f(t):
        return np.exp(t) / t
    if x > 0:
        return (quad(f, -maxfloat, -minfloat)[0] + quad(f, minfloat, x)[0])
    else:
        return quad(f, -maxfloat, x)[0]



def factorial(n):
    return _factorial(n)

def factorial2(num: int) -> int:
    if not isinstance(num, int):
        raise ValueError("double_factorial() only accepts integral values")
    if num < 0:
        raise ValueError("double_factorial() not defined for negative values")
    value = 1
    for i in range(num, 0, -2):
        value *= i
    return value



def factorialk(n, k, exact=True):
    
    if exact:
        if n < 1-k:
            return 0
        if n <= 0:
            return 1
        val = 1
        for j in range(n, 0, -k):
            val = val*j
        return val
    else:
        raise NotImplementedError



def shichi(x):
    pass


def sici(x):
    pass




def softmax(x):
    return np.exp(x)/sum(np.exp(x))

def log_softmax(x):
    return log(softmax(x))


def spence(z):
    pass



def zeta(s, t=100):
    if s == 1: return complex("inf")
    term = (1 / 2 ** (n + 1) * sum((-1) ** k * binom(n, k) * (k + 1) ** -s 
                                   for k in range(n + 1)) for n in count(0))
    return sum(islice(term, t)) / (1 - 2 ** (1 - s))


def zetac(x):
    return zeta(x)-1





