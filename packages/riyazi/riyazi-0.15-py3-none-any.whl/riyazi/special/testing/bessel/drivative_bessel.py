from mpmath import besselj,bessely,besselk,besseli,hankel1,hankel2


__all__ = ['jvp','yvp','kvp','ivp','h1vp','h2vp']

def jvp(n,x):
    return (0.5*(besselj(n-1,x)- besselj(n+1,x)))

def yvp(n,x):
    return (0.5*(bessely(n-1,x)- bessely(n+1,x)))


def kvp(n,x):
    return (-0.5*(besselk(n-1,x)+ besselk(n+1,x)))

def ivp(n,x):
    return (0.5*(besseli(n-1,x)+ besseli(n+1,x)))

def h1vp(v,z,n=1):
    return  (v*hankel1(v,z)/z)- (hankel1(v+1,z))


def h2vp(v,z,n=2):
    return  0.5*((hankel2(v-1,z))- (hankel2(v+1,z)))
