import basic
def sqrt(x):
    """
    Return the square root of x.
    Real and complex arguement 

    >>> from riyazi import* 
    >>> sqrt(4)
    2.0
    >>> sqrt(-4)
    2j
    >>> sqrt(2+3j)
    (1.67414922803554+0.8959774761298382j)
    >>> sqrt(2j+3j)
    (1.5811388300841898+1.5811388300841898j)
    >>> sqrt(-3j) # Result negative some problem

    >>> sqrt(inf)
    inf
    >>> sqrt(-inf)

    Refrence:
    ::
    # Wikipedia
    # --------

    """
    return sqrt(x)


def square(x):
    """
    Return the square of x. 

    >>> from riyazi import*
    >>> square(2)
    4
    >>> square(2+3j)
    (0.6075666647314784-0.308756018097902j)
    >>> square(2j)
    (0.007927894711475971+0.04248048042515221j)
    >>> square(-2j)
    (0.007927894711475971-0.04248048042515221j)
    >>> square(2j+3j)
    (-7.453816615815512e-05+0.00038098003796102734j)
    >>> square(inf)
    inf
    >>> square(-inf)

    Refrence:
    ::
    # Wikipedia 
    # --------
    """
    return square(x)

def  power(a,x):
    """
    Return the power of a raised to x . 

    >>> from riyazi import* 
    >>> power(2,3)
    8
    >>> power(-2,3)
    -8
    >>> power(2,-3)
    0.125
    >>> pow(-2,-3)
    -0.125
    >>> power(2j,3j)
    (-0.004374812582252155+0.007846052028917017j)
    >>> power(-2j,-3j)
    (-0.004374812582252155-0.007846052028917017j)
    >>> power(2j,-4)
    (0.0625+0j)
    >>> power(2,-4j)
    (-0.9326870768360711-0.360686590689181j)
    
    Refrence:
    ::
    # Wikipedia
    # ---------
    """
    return pow(a,x)


def table(x,rng=11):
    """
    Return the table of any no. 

    >>> from riyazi import* 
    >>> table (2)
    2 * 1 = 2
    ....
    2 * 10 = 20
    >>> table(-2)
    -2 * 1 = -2
    ....
    -2 * 10 = -20
    >>> table(2j)
    2j * 1 = 2j
    ....
    2j * 10 = 20j
    >>> table(-2j)
    (-0-2j) * 1 = -2j
    ....
    (-0-2j) * 10 = -20j

    Refrence:
    ::
    # Wikipedia

    """
    return table(x,rng=11)


def fab(n):
    return basic.fabonaci(n)

def fabs(x):
    """
    Return the absolute value of the float x.

    >>> from riyazi import* 
    >>> fabs(-4)
    4.0
    >>> fabs(2)
    2.0
    >>> fabs(-2j)
    2.0
    >>> fabs(2+3j)
    3.605551275463989
    >>> fabs(2-3j)
    3.605551275463989
    >>> fabs(inf)
    inf
    >>> fabs(-inf)
    inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return basic.fabs(x)


def factorial(n):
    """
    Find x!.
    
    Raise a ValueError if x is negative or non-integral.
    
    >>> factorial(0)
    1
    >>> factorial(-1)
    you must enter a non-negative integer
    >>> factorial(2.5) # some error 
    factorial() only accepts integral values

    """
    return basic.factorial(n)


def is_prime(n):
    return basic.is_prime(n)

def root(n, root=2):
    """
    find any root like a sqrt(),cbrt() 
    
    >>> from riyazi import * 
    >>> root(8,2)
    2.8284271247461903
    >>> root(8,3) 
    2.0
    >>> root(8,2j)
    2.8284271247461903
    >>> root(8,3j)
    (0.7692389013639722-0.6389612763136348j)

    Refrence:
    ::
    # --------
    
    """
    return basic.root(n,root)


def gcd(*integers):
    """
    Greatest Common Divisor.
    
    >>> from riyazi import* 
    >>> gdc(122,12)
    2
    >>> gcd(4,8)
    4
    >>> gcd(2.3,4)
    8.881784197001252e-16
    >>> gcd(2.3,1.2)
    1.1102230246251565e-15
    >>> gcd(-2,4)
    -2
    >>> gcd(-2,-4)
    -2
    >>> gcd(2,-4)
    -2 

    Refrence:
    ::
    # Wikipedia 
    # Wolframe 
    
    """
    return basic.gcd(*integers)


def lcm(*integers):
    """
     Least Common Multiple.

     >>> from riyazi import * 
     >>> lcm(4,8)
     8
     >>> lcm(2,4,6,8)
     24
     >>> lcm(4,5,2)
     20
     >>> lcm(-2,-4,-8)
     -8
     >>> lcm(-2,4,8)
     8
     >>> lcm(-2,-4,8)
     8

     Refrence:
     ::
     # Wikipedai 
     # Wolframe 
    
    """
    return basic.lcm(*integers)



def ceil(x):
    """
    Return the ceiling of x as an Integral.
    This is the smallest integer >= x.

    >>> from riyazi import* 
    >>> ceil(4.2)
    5
    >>> ceil(3)
    3
    >>> ceil(5.9)
    6
    >>> ceil(-5.9) # error
    >>> ceil(-2.1)
    -1
    >>> ceil(-2.9)
    -2
    >>> ceil(-3.1)
    -2
    >>> ceil(-3.1)
    -2

    Refrence:
    ::
    # Wolframe 
    # Wikipedia

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return basic.ceil(x)


def exp(x):
    """
    Return the e riased  to the power of x. 

    >>> from riyazi import* 
    >>> exp(2)
    7.3890560989306495
    >>> exp(4)
    54.59815003314423
    >>> exp(2j)
    (-0.4161468365471424+0.9092974268256817j)
    >>> exp(-2j)
    (-0.4161468365471424-0.9092974268256817j)
    >>> exp(2+3j)
    (-7.315110094901102+1.0427436562359043j)
    >>> exp(inf)
    inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.exp(x)

def radians(x):
    """
    Convert angle x from degrees to radians.
    
    >>> from riyazi import* 

    >>> radians(0.3)
    0.005235987755982988
    >>> radians(2)
    0.03490658503988659
    >>> radians(2j)
    0.03490658503988659j
    >>> radians(2+3j)
    (0.03490658503988659+0.05235987755982989j)
    >>> radians(-2j)
    -0.03490658503988659j
    >>> radians(inf)
    inf
    >>> radians(-inf)
    -inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe

    
    """
    return basic.radians(x)


def degrees(x):
    """
    Convert angle x from radians to degrees.

    >>> degrees(3)
    171.88733853924697
    >>> degrees(pi/2)
    90.0
    >>> degrees(3j)
    171.88733853924697j
    >>> degrees(-3j)
    -171.88733853924697j
    >>> degrees(2+3j)
    (114.59155902616465+171.88733853924697j)
    >>> degrees(inf)
    inf
    >>> degrees(-inf)
    -inf

    Refrence:
    ::

    # Wikipedia
    #  Wolframe 



    """
    return basic.degrees(x)

def expm1(x,/):
    """
    Return  exp(x)-1.

    This function avoids the loss of precision involved 
    in the direct evaluation of exp(x)-1 for small x.

    >>>from riyazi import*
    >>> expm1(2)

    >>> expm1(pi/2)

    >>> exmp1(2+3j)

    >>> exmp1(2j+3j)

    >>> expm1(-2j)

    >>> expm1(inf)

    >>> exmp1(-inf)

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
  
    return basic.expm1(x)
    

def ldexp(x,i):
    """
    Return x * (2**i).

    This is essentially the inverse of frexp().
    
    >>> from riyazi import* 
    >>> ldexp(2,2)
    8.0
    >>> ldexp(2,3)
    16.0
    >>> ldexp(2,23)
    16777216.0
    >>> ldexp(2,2.3)
    
    >>> ldexp(2,2j)

    >>> ldexp(2j, 3j)

    >>> ldexp(-2j, 3j)

    >>> ldexp(inf,-inf)

    Refrence:
    ::
    # Wolframe 
    # Wikipedia
     
    
    """
    return basic.ldexp(x,i)



def comb(n,k):
    """
    Number of ways to choose k items from n items without
    repetition and without order.

    Evaluates to n! / (k! * (n - k)!) when k <= n and evaluates
    to zero when k > n.

    Also called the binomial coefficient because it is equivalent
    to the coefficient of k-th term in polynomial expansion of the
    expression (1 + x)**n.

    Raises TypeError if either of the arguments are not integers.
    Raises ValueError if either of the arguments are negative.
    
    ValueError: n must be a non-negative integer
    ValueError: k must be a non-negative integer
    TypeError: 'float' object cannot be interpreted as an integer



    >>> from riyazi import* 
    >>> comb(4,3)
    4.0
    >>> comb(9,2)
    36.0

    Refrence:
    ::
    # Wiki
    # Wolframe

    """
    return basic.comb(n,k)



def perm(n,k):
    """
    Number of ways to choose k items from n items without 
    repetition and with order.

    Evaluates to n! / (n - k)! when k <= n and evaluates
    to zero when k > n.

    If k is not specified or is None, then k defaults to n
    and the function returns n!.

    Raises TypeError if either of the arguments are not integers.
    Raises ValueError if either of the arguments are negative.
    
    >>> from riyazi import* 
    >>> perm(5,4)
    120.0
    >>> perm(5,2)
    20.0

    Refrence:
    ::
    # Wikipedia
    # Wolframe


    """
    return basic.perm(n,k)


def copysign(x,y):
    """
    Return a float with the magnitude (absolute value) of x but
    the sign of y.

    >>> from riyazi import*
    >>> copysign(1.0,-0.0)
    -1.0
    >>> copysign(4,3)
    4.0
    >>> copysign(-4,3)
    4.0
    >>> complex number n't handle 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.copysign(x,y)


def dist(p,q):
    """
    Return the Euclidean distance between two points p and q.

    The points should be specified as sequences (or iterables) of
    coordinates.  Both inputs must have the same dimension.

    Roughly equivalent to:
    sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    
    >>> from riyazi import* 

    >>> dist([3,4,5].[3,4,2])
    3.0
    >>> dist([3,4,5],[3,4])

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.dist(p,q)



def fsum(seq):
    """
    Return an accurate floating point sum of values in the iterable seq.

    Assumes IEEE-754 floating point arithmetic.
    
    >>> from riyazi  import* 
    >>> fsum([3,4,5])
    12.0
    >>> fsum([3,4,5.4])
    12.4

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return basic.fsum(seq)


def isqrt(x):
    """
    Return the integer part of the square root of the input.

    >>> from riyazi import* 
    >>> isqrt(2)
    1
    >>> isqrt(5)
    2
    >>> isqrt(12)
    3

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.isqrt(x)

def trunc(x):
    """
    Truncates the Real x to the nearest Integral toward 0.

    Uses the __trunc__ magic method.

    >>> from riyazi import* 
    >>> trunc(24.1)
    24
    >>> trunc(1.9)
    1
    >>> trunc(0.9)
    0

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return basic.trunc(x)


def atan2(y,x):
    """
    Return the arc tangent (measured in radians) of y/x.
        
    Unlike atan(y/x), the signs of both x and y are considered.
    
    >>> from riyazi import* 
    >>> atan2(5,4)
    0.8960553845713439
    >>> atan2(6,3)
    1.1071487177940904

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.atan2(y,x)


def isfinite(x):
    """
    Return True if x is neither an infinity nor a NaN,
    and False otherwise.
    >>> from riyazi  import * 
    >>> isifnite(4)
    True
    >>> isfinite(inf)
    False
    >>> isfinite(nan)

    >>> isfinite()


    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return basic.isfinite(x)


def isinf(x):
    """
    Return True if x is a positive or negative infinity,
     and False otherwise
    
    >>> from riyazi import * 
    >>> isinf(4)
    False
    >>> isinf(inf)
    True
    >>> isinf(nan)
    False 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return basic.isinf(x)


def isnan(x):
    """
    Return True if x is a NaN (not a number), 
    and False otherwise.

    >>> isnan(3)
    False
    >>> isnan(inf)
    False
    >>> isnan(nan)
    True 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return basic.isnan(x)


def prod(iterable,/,*,start=1):
    """
    Calculate the product of all the elements in the input iterable.

    The default start value for the product is 1.

    When the iterable is empty, return the start value.  
    This function is
    intended specifically for use with numeric values and may reject
    non-numeric types.
    
    >>> from riyazi import* 
    >>> prod()
    >>> prod()
    
    Refrence:
    ::
    # Wiki
    # Wolframe
    
    """
    return basic.prod(iterable,start=1)


def conjugate(x):
    return basic.conjugate(x)


def conj(x):
    return basic.conj(x)


























































