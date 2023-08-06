from mpmath import hyp2f1
from math import sqrt,gamma,pi
from mpmath import hyp2f1 
from math import sqrt,factorial,pi,cos,e
import scipy.special as sp


__all__ = ['lpmv','sph_harm','clpmn','lpn','lqn','lpmn','lqmn']


def lpmv():
    pass

def sph_harm(m,n,theta,phi):
    root = sqrt( ((2*n+1)*factorial(n-m)) / ((4*pi)*factorial(n+m)))
    exp = pow(e,1j*m*theta)*sp.lpmv(m,n,cos(phi))
    return (root*exp) 

def clpmn():
    pass

def lpn(n,z):
    return hyp2f1(-n, n+1, 1, (1-z)/2)

def lqn(v,z):
    return (sqrt(pi)*gamma(v+1)*hyp2f1((v+1)/2,(v+2)/1,v+(3/2),(1/pow(z,2))))/(pow(2*z,v+1)*gamma(v+3/2))

def lpmn():
    pass

def lqmn():
    pass



