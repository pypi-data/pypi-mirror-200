import math 
from math import gamma,log

__all__=['gamma','gammaln','loggamma','gammasgn','gammainc',
'gammaincinv','gammaincc','gammainccinv', 'beta', 'betaln',
'betainc','betaincinv','psi','rgamma','polygamma','multigammaln',
'digamma','poch']


def gamma(x):
    return math.gamma(x)

def gammaln(x):
    return math.log(math.gamma(x))

def loggamma(x):
    return math.log(math.gamma(x))

def gammasgn(x):
    if x >= 0:
        return 1.0
    else:
        return -1

def gammainc(a,x):
    pass



def gammaincinv(a,y):
    pass 

def gammaincc(a,x):
    pass 

def gammainccinv(a,y):
    pass


def beta(a,b):
    return (gamma(a)* gamma(b)) / gamma(a+b)

def betaln(a,b):
    return log(abs(beta(a,b)))


def betainc():
    pass

def betaincinv():
    pass 


def psi():
    pass




def rgamma(z):
    return (1/gamma(z))

def polygamma():
    pass

def multigammaln():
    pass

def digamma():
    pass


def poch(z,m):
    return gamma(z+m)/gamma(z)

