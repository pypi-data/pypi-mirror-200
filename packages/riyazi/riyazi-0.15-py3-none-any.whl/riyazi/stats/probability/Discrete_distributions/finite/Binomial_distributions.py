from cmath import sqrt
import math 
class binom:
    
    def  pmf(k,n,p):
        
        return math.comb(n,k)*(p**k)*((1-p)**(n-k))

    def mean(n,p):
        return (n*p)

    def std(n,p):
        
        """
        Calculates the standard deviation
        :return std:
        """
        std = sqrt(n * p * (1-p))
        return std



n = 50
p = 0.9
r = list(range(n + 1))
dist = [pmf(k, n, p) for k in r]
import matplotlib.pyplot as plt

plt.bar(r, dist)
plt.show()