from math import pi,sqrt
import mpmath as mp 
import scipy.special as sp 
from cmath import exp ,sqrt

__all__ = ['airy','airye','ai_zeros','bi_zeros','itairy']



def ai(z):
    return ((1/pi) * sqrt(z/3))* mp.besselk(1/3,(2/3)*(z**(3/2)))

def aip(z):
    return ((-z/(pi*sqrt(3))) * mp.besselk(2/3,(2/3)*(z**(3/2))))

def bi(z):
    return (sqrt(z/3))*( mp.besseli(-1/3,(2/3)*(z**(3/2)))+mp.besseli(1/3,(2/3)*(z**(3/2))) )

def bip(z):
    return (z/sqrt(3))*( mp.besseli(-2/3,(2/3)*(z**(3/2)))+mp.besseli(2/3,(2/3)*(z**(3/2))))



def airy(z):
    return (ai(z),aip(z),bi(z),bip(z))




def airye(z):
    Ai,Aip,Bi,Bip = sp.airy(z)
    eAi  = Ai  * exp(2.0/3.0*z*sqrt(z)).real
    eAip = Aip * exp(2.0/3.0*z*sqrt(z)).real
    eBi  = Bi  * exp(-abs(2.0/3.0*(z*sqrt(z)).real)).real
    eBip = Bip * exp(-abs(2.0/3.0*(z*sqrt(z)).real)).real
    return eAi,eAip,eBi,eBip





def ai_zeros(nt):
    pass

def bi_zeros(nt):
    pass

def itairy(x):
    pass