__all__ = ['cbrt','unitroots','expj','expjpi','powm1', 'lambertw','agm','fac2','binomial']

from math import e
import math 
from math import pi 

def cbrt(x):
    return x**(1/3)

def unitroots(n):
    pass

# Exponentiation


def _exp(x):
    return e**(1j*x)
def expj(x):
    return ('real = ',_exp(x).real, 'imag = ',_exp(x).imag)

def expjpi(x):
    pass

def powm1(x,y):
    return pow(x,y)-1

def lambertw(z):
    return (z)/ (math.exp(z))

def agm(a,b):
    return (a*b)**0.5

def cospi():
    pass

def sinpi():
    pass

def sinc(x):
    if x == 0:
        return 1.0
    return (math.sin(x) /x)


def sincpi(x):
    if x == 0:
        return 1.0
    return math.sin(x*pi)/(pi*x)

def fac2(n):
    """
    Computes the double factorial `x!!`, defined for integers
    `x > 0` by
    """
    if(n == 0 or n == 1):
        return 1.0
    return n*fac2(n-2)

def binomial(n,k):

    if k>n:
        raise ValueError('Invalid Inputs, ensure that n >= k')
        #function is only defined for n>=k
    if k == 0 or n == k:
        #C(n,0) = C(n,n) = 1, so this is our base case.
        return 1
    if k > n/2:
        #C(n,k) = C(n,n-k), so if n/2 is sufficiently small, we can reduce the problem size.
        return binomial(n,n-k)
    else:
        #else, we know C(n,k) = (n/k)C(n-1,k-1), so we can use this to reduce our problem size.
        return ((n/k)*binomial(n-1,k-1))


def gamma(x):
    return math.factorial(x-1)


def rgamma(x):
    return 1/gamma(x)

def gammaprod(a,b):
    return gamma(a)/ gamma(b)

def loggamma(x):
    return math.log(gamma(x))

def rf(x,n):
    #return x**gamma(n)
    return gamma(x+n)/ gamma(x)

def ff(x,n):
    return gamma(x+1)/ gamma(x-n+1)




def beta(x,y):
    """
    Computes the beta function,
    `B(x,y) = \Gamma(x) \Gamma(y) / \Gamma(x+y)`.
    The beta function is also commonly defined by the integral
    representation
    """
    return (gamma(x) * gamma(y)) / gamma(x+y)

def betainc(a,b,x1=0,x2=1, regularized=False):
    return beta(a,b)



def superfac(n):
    """
    Computes the superfactorial, defined as the product of
    consecutive factorials
    1.http://oeis.org/A000178
    """
    x = 1
    for i in range(1,n+1):
        x *= math.factorial(i)
    return float(x) 


"""
def superfactorial(n):
    val = 1
    ans = []
    for i in range(1,n+1):
        val = val*i
        ans.append(val)
    arr = [1]
    for i in range(1,len(ans)):
        arr.append((arr[-1]* ans[i]))
    return arr


"""

def hyperfac(n):
    val = 1
    for i in range(1,n+1):
        val = val* pow(i,i)
    return float(val) 

def barnesg(x):
    """
    Evaluates the Barnes G-function
    """
    return superfac(x-2)

def harmonic(n):
    i = 1
    s = 0.0
    for i in range(1,n+1):
        s = s + 1/i
    return s 

def psi():
    pass

def digamma():
    pass
