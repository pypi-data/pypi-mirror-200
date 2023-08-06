from Riyazi.Module.numeric import factorial


def permutations(n,m):
    if(n >= m):
        minus = (n-m)
        n = factorial(n)
        m = factorial(minus)
        
        return (n/m)