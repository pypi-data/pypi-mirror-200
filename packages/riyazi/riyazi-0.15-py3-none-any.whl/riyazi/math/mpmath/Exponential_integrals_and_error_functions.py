__all__ = ['gammainc','ei','e1','expint','li','ci','si','chi','shi',
'erf','erfc','erfi','erfinv','npdf','ncdf','fresnels','fresnelc']

import math 

def gammainc(z, a=0, b=None, regularized=False):
    return math.factorial(z-1)