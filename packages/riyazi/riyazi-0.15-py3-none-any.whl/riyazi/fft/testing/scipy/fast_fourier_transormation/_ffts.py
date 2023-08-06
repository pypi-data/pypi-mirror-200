__all__ = ['fft','ifft','fft2','ifft2', 'fftn', 'ifftn', 'rfft', 'irfft', 'rfft2','irfft2',
'rfftn', 'irfftn', 'hfft', 'ihfft', 'hfft2', 'ihfft2', 'hfftn','ihfftn']



import numpy as np 
def fft(x):
    """
    A recursive implementation of 
    the 1D Cooley-Tukey FFT, the 
    input should have a length of 
    power of 2. 
    """
    N = len(x)
    
    if N == 1:
        return x
    else:
        X_even = fft(x[::2])
        X_odd = fft(x[1::2])
        factor = \
          np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate(\
            [X_even+factor[:int(N/2)]*X_odd,
             X_even+factor[int(N/2):]*X_odd])
        return X

def ifft(X):
    ''' IFFT of 1-d signals
    usage x = ifft(X) 
    unpadding must be done implicitly'''

    x = fft([x.conjugate() for x in X])
    return [x.conjugate()/len(X) for x in x]

import cmath
import numpy as np
from math import log, ceil
def pad2(x):
    m, n = np.shape(x)
    M, N = 2 ** int(ceil(log(m, 2))), 2 ** int(ceil(log(n, 2)))
    F = np.zeros((M,N), dtype = x.dtype)
    F[0:m, 0:n] = x
    return F, m, n

def fft2(f):
    '''FFT of 2-d signals/images with padding
    usage X, m, n = fft2(x), where m and n are dimensions of original signal'''

    f, m, n = pad2(f)
    return np.transpose(fft(np.transpose(fft(f))))



def ifft2():
    pass

def fftn():
    pass

def ifftn():
    pass

def rfft():
    pass

def irfft():
    pass
def rfft2():
    pass

def irfft():
    pass

def rfft2():
    pass


def irfft2():
    pass

def rfftn():
    pass

def irfftn():
    pass

def hfft():
    pass

def ihfft():
    pass

def hfft2():
    pass
def ihfft2():
    pass

def hfftn():
    pass

def ihfftn():
    pass

