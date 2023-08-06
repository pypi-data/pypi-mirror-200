
import math


__all__  = ['itj0y0','it2j0y0','iti0k0','it2i0k0',
'besselpoly']



def itj0y0(x):
    res = 0 
    for k in range(20):
        res += (pow((-x**2)/4,k)/ math.factorial(k)**2)
    return res