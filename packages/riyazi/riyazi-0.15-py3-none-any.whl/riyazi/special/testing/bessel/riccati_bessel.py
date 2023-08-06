
from scipy.special import spherical_jn,spherical_yn

__all__ =['riccati_jn','riccati_yn']

def riccati_jn(n,x):
    for rng in range(0,n+1):
        c = (x*spherical_jn(rng,x))
        print(c)

def riccati_yn(n,x):
    for rng in range(0,n+1):
        c = (x*spherical_yn(rng,x))
        print(c)