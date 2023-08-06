__all__ = ['sqrt','square','power','table','fabonaci','fabs','factorial',
    'is_prime','root','lerp','compound_interest','gcd','exp','conjugate','conj']

from math import e 
from math import gamma # , sqrt
import math 
from math import inf 

# square root of x 
def sqrt(x):
    if(type(x) == complex):
        return (-1*x)**0.5*1j
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return x**0.5

"""
def sqrt(x):
    # complex number handle 
    if(type(x) == complex):
        return  (pow(-x,0.5j)*1j)
    # negative number handle 
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return pow(x,0.5) # non-negative number handle 


"""

# Find Out Square  of x.
def square(x):
    return pow(x,x)


# Find Out Power of a raised to the power x. 
def  power(a,x):
    return pow(a,x)


# print the table of any numbers. 
def table(x, rng = 11):
    for i in range(1,rng):
        n = x*i
        print(x, "*",i, "=", n)

# print the Fibonaci series 
def fabonaci(n):
    a,b = 0,1
    while a<n:
        print(a, end=' ')
        a,b = b, a+b

# Floating absolute 
def fabs(x,/):
    return float(abs(x))

# Find factorial of n!
def factorial(n):
    if n<0:
        raise ValueError('you must enter a non-negative integer')
    factorial=1
    for i in range(2,n+1):
        factorial *=i
    return factorial

def is_prime(n):
    if n==2:
        return 1
    if n<2 or n%2==0:
        return 0
    i=3
    while i*i<=n:
        if n%i==0:
            return 0
        i+=2
    return 1

def root(n, root=2):
    return pow(n,1/root)

def lerp(num1, num2, t):
    return num1 + ((num2 -num1)*t)

def compound_interest(principal,rate,years):
    amount=principal*(1+rate/100)**years
    return amount


def Heron(a,b,c):
    s=(a+b+c)/2.0
    A=sqrt(s*(s-a)*(s-b)*(s-c))
    return A

def is_triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        return True
    else:
        return False


def factors(a):
    for i in range(1, a+1):
        if a % i == 0:
            lists = ( print(i))
    return lists 


def gcd(*integers):
    if len(integers) <= 1:
        return integers[0]
    n, k, *others = integers
    if k > n:
        n, k = k, n
    while k != 0:
        k, n = n % k, k
    return gcd(n, *others)



def lcm(*integers):
    """Least Common Multiple."""
    args_max = max(integers)
    n = 1
    while True:
        for k in integers:
            if args_max * n % k != 0:
                n += 1
                break
        else:
            return args_max * n



def ceil(x,/):
    if (int == type(x)):
        return x 
    elif (float == type(x)):
        i= int(x)
        if(x == i):
            return i
        else:
            
            return (i+1)

def fmod(x,y,/):
    z =float (x%y) 
    return z 


def exp(x,/):
    if x is x.imag:
        return pow(e,2+0j)
    else:
        x = pow(e,x)
        return x 

def radians(x,/):
    r= 0.017453292519943295
    return (x*r)

def degrees(x,/):
    dv = 57.29577951308232
    return (x*dv)


def expm1(x,/):
    x = exp(x)-1
    return x 

def ldexp(x,i,/):
    return (float (x*(2**i)))

def frexp(x,/):
    pass

def comb(n,k):
    if (n >= k):
        minus = (n-k)
        n = factorial(n)
        k = factorial(k)* factorial(minus)
        return ((n/k))
    else:
        return 0


def perm(n,k):
    if(n >= k):
        minus = (n-k)
        n = factorial(n)
        k = factorial(minus)
        return (n/k)
    else:
        return 0.0



def copysign(x,y):
    if(y<=0):
        return (abs(x)*(-1))
    else:
        return float(abs(x))   



def dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))     

def fsum(seq):
    return float(sum(seq))


def isqrt(x):
    return int(pow(x,0.5))

def trunc(x):
    return int(x)

def atan2(y,x,/):
    return math.atan(y/x)


def isfinite(x,/):
    if(x == inf):
        return False 
    else:
        return True 


def isinf(x,/):
    if(x == inf):
        return True 
    else:
        return False


def isnan(x,/):
    if (x != x):
        return True
    else:
        return False


def prod(iterable,/,*,start=1):
    prod =1.0 
    for num in iterable:
        prod *=num
    return prod*start 


def conjugate(x):
    return complex(x.real, -x.imag)

def conj(x):
    return complex(x.real,-x.imag)