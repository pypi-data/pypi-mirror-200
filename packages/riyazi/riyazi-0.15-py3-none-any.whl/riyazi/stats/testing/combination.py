from Riyazi.Module.numeric import factorial 
# from Riyazi.Module import * 

def combination(n,m):
    if (n >= m):
        minus = (n-m)
        n = factorial(n)
        m = factorial(m)* factorial(minus)
        
        return ((n/m))