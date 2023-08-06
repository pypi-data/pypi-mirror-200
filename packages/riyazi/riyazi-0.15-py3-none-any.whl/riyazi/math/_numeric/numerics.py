import math 

__all__= ['add','sub','mul','div','sqrt','square','power','table','fab','factorial',
  'is_prime','root','lerp','compound_interest','Heron','is_triangle','factors',
  'Triangle','solve_quad','gcd','lcm','sign','theta','ceil','fmod','exp',
  'remainder','radians','modf','degress','expm1','comb','perm','copysign','dist','ldexp',
  'fsum','isqrt','trunc','atan2','inf','isfinite','isinf','nan','isnan','erf','erfc','successor',
  'predecessor','zeta','is_complex','is_real','transform','erfi','product','isEven','isOdd',
  'isPrime','tau','pi','eta','e','gammas','gamma','integrand','hypot','norm','unitvector','relu',
  'sum_of_series','celsius','fahrenheit','gaussian','sigmoid','infj','nanj','polynomial']


def add(*args):
    """
    Addition  program
    >>> add(5,6,7,8)
    >>>  26

    """
    sum = 0
    for x in args:
        sum +=x 
    return sum 

def sub(a,b):
    """
    subtraction 
    >>> sub(5,7)
    """
    return a-b

def mul(a,b):
    """
    Multiplication 
    >>> mul(4,5)
    """
    return a*b

def div(a,b):
    """
    Division program 
    >>> div(a,b)
    
    """
    return a/b

def sqrt(x):
    if(type(x) == complex):
        return (-1*x)**0.5*1j
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return x**0.5

def square(x):
    """
    Square calculate
    >>> square(x)
    """
    return pow(x,x)

def  power(a,x):
    """
    power calculate
    >>> pow(2,5)
    """
    return pow(a,x) 


#print table of any no 

def table(a):
    """
    print table of any no 
    >>> table(2)
    """
    for i in range(1,11):
        n = a*i
        print(a, "*",i, "=", n)

# Fibonaci
def fab(n):
    a,b = 0,1
    while a<n:
        print(a, end='')
        a,b = b, a+b 

# factorial 
def factorial(n):
    return 1 if(n==1 or n==0) else n*factorial(n-1)

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


def root(num, root = 2):
    return num**(1/root)

def lerp(num1, num2, t):
    return num1 + ((num2 -num1)*t)

def compound_interest(principal,rate,years):
    amount=principal*(1+rate/100)**years
    return amount 

from math import gamma # , sqrt
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

def Triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        if(a==b and b==c):
            print("Equalteral triangle")
        elif (a==b or b==c or a==c):
            print("Isoceles triangle")
        else:
            print("scalene triangle")
    else:
        print("Not a triangle")

#from math import sqrt
from cmath import tau #sqrt as csqrt, tau 
def solve_quad(a,b,c):
    if(a==b):
        if(b!=0):
            x1= -c/b
            print(f"it has only one root, x1 ={x1}")
        else:
            print("it has no root")
    else:
        d=b**2-4*a*c
        if(d>0):
            print('Roots are real')
            x1=(-b+sqrt(b**2-4*a*c))/(2*a)
            x2=(-b-sqrt(b**2-4*a*c))/(2*a)
            print(f'The roots of are {x1} and {x2}')

def gcd(*integers):
    """Greatest Common Divisor."""
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


def sign(x):
    return x / -x

def theta(x):
    if 0 < x:
        return 1
    else:
        return 0

def ceil(x,/):
    """
    Return the ceiling of x as an Integral.
    This is the smallest integer >= x.
    """
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


e=2.7182818284
def exp(x,/):
    if x is x.imag:
        return e**2+0j
    else:
        x = e**x
        return x

def remainder(x,y,/):
    """
    positive is your remainder
    negative is your need if you want to x multiple of y.
    Difference between x and the closest integer multiple of y.
    """
    r = x%y
    c = int (-1 * (y/r))
    print("(remainder, Difference closest integer multiply of y.)")
    return r,c


def radians(x,/):
    """Convert angle x from degrees to radians."""
    r= 0.017453292519943295
    r = x*r
    return r


def modf(x):
    a = int(x)
    b = (x%a)
    x = float(a)
    decimal_places='%.1f'
    b = float(decimal_places %b)
    return  b, x


def degress(x,/):
    """Convert angle x from radians to degrees."""
    dv = 57.29577951308232
    deg = x*dv
    return deg

def expm1(x,/):
    """Return exp(x)-1."""
    x = exp(x)-1
    return x 


def ldexp(x,i,/):
    
    x =float (x*(2**i))
    return x 

def comb(n,k):
    if (n >= k):
        minus = (n-k)
        n = factorial(n)
        k = factorial(k)* factorial(minus)
        
        return ((n/k))


def perm(n,k):
    if(n >= k):
        minus = (n-k)
        n = factorial(n)
        k = factorial(minus)
        
        return (n/k)


def copysign(x,y):
    
    
    """
    Return a float with the magnitude (absolute value) of x but the sign of y.
    """
    if(y<=0):
        return (abs(x)*(-1))
    else:
        return float(abs(x))

import math
def dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def fsum(seq):
    return sum(seq)

def isqrt(x):
    x = x**0.5
    return int(x)

def trunc(x):
    return int(x)

def atan2(y,x,/):
    return math.atan(y/x)

inf = type(float('inf'))

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

nan = (float('nan'))


def isnan(x,/):
    if (x != x):
        return True
    else:
        return False


def erf(z):
    t = 1.0 / (1.0 + 0.5 * abs(z))
        # use Horner's method
    ans = 1 - t * math.exp( -z*z -  1.26551223 +
                            t * ( 1.00002368 +
                            t * ( 0.37409196 + 
                            t * ( 0.09678418 + 
                            t * (-0.18628806 + 
                            t * ( 0.27886807 + 
                            t * (-1.13520398 + 
                            t * ( 1.48851587 + 
                            t * (-0.82215223 + 
                            t * ( 0.17087277))))))))))
    if z >= 0.0:
        return ans
    else:
        return -ans


def erfc(x):
    return 1 - math.erf(x)


def successor(x):
    x = x+1 
    return x 

def predecessor(x):
    x = x-1
    return x 

def zeta(x):
    """
    "zeta(x)" returns the value of ζx.
    """
    if x == 1:
        return inf
    a = [0.5 / (1 - (2 ** (1 - x)))]
    b = [a[0]]
    for n in range(1, 200):
        for k in range(n):
            a[k] = a[k] * n / (n - k) / 2
        a += [-(n / (n + 1)) ** x * a[-1] / n]
        b += [sum(a)]
        if 1.0e+4 < abs(b[-1]) < 1.0e-6:
             break           
    return sum(b)

def is_complex(_x):
    """
    "complex(x)" returns whether x is a complex number.
    """
    try:
        a = _x.imag
        if a == 0:
            return False
        else:
            return True
    except:
        return True



def is_real(x):
    try:
        a =x.real
        if a == 0:
            return False
        else:
            return True
    except:
        return True


def transform(p):
    x,y  = p
    x1 = y + 1.0 - 1.4*x**2
    y1 = 0.3*x

    return x1, y1

def erfi(x : float) -> float:
    """Calculates  the imaginary error function at a specific point"""
    MULTIPLIER = 2 / math.sqrt(math.pi)
    total = 0
    for n in range(100):
        denominator = math.factorial(n) * (2*n+1)
        nominator = pow(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def product(*args):
    """Returns the product of float or ints
        product(3,4,5) -> 60
        product(*[3,4,5]) -> 60
    """
    prod = 1
    for num in args:
        prod*=num
    return prod

def isEven(num : int) -> bool:
    """Returns True if a number can be divded by 2"""
    return num%2==0

def isOdd(num : int) -> bool:
    """Returns True if a number cannot be divded by 2"""
    return not isEven(num)

def isPrime(num : int) -> bool:
    """Returns True if a number can divide num in the \n
       ** range(2,int(1+num**(1/2))) **
       """
    if num == 1:
        return False

    for i in range(2,int(1+num**(1/2))):
        if(num%i==0):
            return False
    return True

# Constants
tau = 6.28318530717958647
pi = 3.1415926535897932
eta = pi / 2
e = 2.71828182845904523
gammas = 0.57721566490153286

from scipy.integrate import quad


def gamma(num: float) -> float:
    """
    https://en.wikipedia.org/wiki/Gamma_function
    In mathematics, the gamma function is one commonly
    used extension of the factorial function to complex numbers.
    The gamma function is defined for all complex numbers except the non-positive
    integers


    >>> gamma(-1)
    Traceback (most recent call last):
        ...
    ValueError: math domain error



    >>> gamma(0)
    Traceback (most recent call last):
        ...
    ValueError: math domain error


    >>> gamma(9)
    40320.0


    >>> from math import gamma as math_gamma
    >>> gamma(3.3) - math_gamma(3.3) <= 0.00000001
    True
    """

    if num <= 0:
        raise ValueError("math domain error")

    return quad(integrand, 0, inf, args=(num))[0]


def integrand(x: float, z: float) -> float:
    return math.pow(x, z - 1) * math.exp(-x)


def hypot(*coordinates):
    """
    Multidimensional Euclidean distance from the origin to a point.
    >>> hypot(3.0, 4.0)

    """
    return math.sqrt(sum(x**2 for x in coordinates))


def norm(x):
    """returns the magnitude of a vector x"""
    return math.sqrt(sum(x**2 for x in x ))



def unitvector(x):
    """returns a unit vector x/|x|. x needs to be a numpy array."""
    xnorm = norm(x)
    if xnorm == 0:
        raise ValueError("Can't normalise vector with length 0")
    return sum(x) / norm(x)


import numpy as np


def relu(vector: list[float]):
    """
    https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
    Implements the relu function

    Parameters:
        vector (np.array,list,tuple): A  numpy array of shape (1,n)
        consisting of real values or a similar list,tuple


    Returns:
        relu_vec (np.array): The input numpy array, after applying
        relu.

    >>> vec = np.array([-1, 0, 5])
    >>> relu(vec)
    array([0, 0, 5])
    """

    # compare two arrays and then return element-wise maxima.
    return np.maximum(0, vector)


def sum_of_series(first_term, common_diff, num_of_terms):
    """
    Find the sum of n terms in an arithmetic progression.

    >>> sum_of_series(1, 1, 10)
    55.0
    >>> sum_of_series(1, 10, 100)
    49600.0
    """
    sums = (num_of_terms / 2) * (2 * first_term + (num_of_terms - 1) * common_diff)
    # formula for sum of series
    return sums


def celsius(f):
    return (f-32)*(5/9)

def fahrenheit(c):
    return (c*(9/5)+32)


"""
Reference: https://en.wikipedia.org/wiki/Gaussian_function
"""
from numpy import exp, pi , sqrt


def gaussian(x, mu: float = 0.0, sigma: float = 1.0) -> int:
    """
    >>> gaussian(1)
    0.24197072451914337

    >>> gaussian(24)
    3.342714441794458e-126

    >>> gaussian(1, 4, 2)
    0.06475879783294587

    >>> gaussian(1, 5, 3)
    0.05467002489199788

    Supports NumPy Arrays
    Use numpy.meshgrid with this to generate gaussian blur on images.
    >>> import numpy as np
    >>> x = np.arange(15)
    >>> gaussian(x)
    array([3.98942280e-01, 2.41970725e-01, 5.39909665e-02, 4.43184841e-03,
           1.33830226e-04, 1.48671951e-06, 6.07588285e-09, 9.13472041e-12,
           5.05227108e-15, 1.02797736e-18, 7.69459863e-23, 2.11881925e-27,
           2.14638374e-32, 7.99882776e-38, 1.09660656e-43])

    >>> gaussian(15)
    5.530709549844416e-50

    >>> gaussian([1,2, 'string'])
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for -: 'list' and 'float'

    >>> gaussian('hello world')
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for -: 'str' and 'float'

    >>> gaussian(10**234) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    OverflowError: (34, 'Result too large')

    >>> gaussian(10**-326)
    0.3989422804014327

    >>> gaussian(2523, mu=234234, sigma=3425)
    0.0
    """
    return 1 / sqrt(2 * pi * sigma**2) * exp(-((x - mu) ** 2) / (2 * sigma**2))


def sigmoid(u):
    return 1/(1+math.exp(-u))

infj = complex('infj')

nanj = complex('nanj')


def polynomial(coeff,x):
    """
    >>> polynomial([1,2,4],6)
    
    """
    deg = len(coeff) -1 
    return sum([c*(x**(deg-i)) for i , c in enumerate(coeff)])

