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
    """
    square root 
    >>> sqrt(5)
    """
    return x**0.5



def square(x):
    """
    Square calculate
    >>> square(x)
    """
    return x*x 


def  pow(a,x):
    """
    power calculate
    >>> pow(2,5)
    """
    return a**x 



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






























