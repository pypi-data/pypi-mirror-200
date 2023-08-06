import numpy as np
import scipy.special as sp

__all__ =['sph_jn','sph_yn', 'sph_i1n', 'sph_i2n','sph_h1n', 'sph_h2n',
'sph_kn']

# jn()
def sph_jn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.jv(n + 0.5, z)

# yn()
def sph_yn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.yv(n + 0.5, z)

# iv1()
def sph_i1n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.iv(n + 0.5, z)

# iv2()
def sph_i2n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.iv(-n - 0.5, z)

# hankel1()
def sph_h1n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.hankel1(n + 0.5, z)

# hankel2()
def sph_h2n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.hankel2(n + 0.5, z)

# kn()
def sph_kn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.kv(n + 0.5, z)


