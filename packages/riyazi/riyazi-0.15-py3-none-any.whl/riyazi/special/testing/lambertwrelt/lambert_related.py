import numpy as np
from cmath import log 

__all__ = ['lambert_w','wrightomega']

def lambert_w(x, tol=1e-6, maxiter=1000):
    """
    Lambert W function.
    Compute the Lambert W function for a given x.
    """
    # Initialize the iteration with a guess of W(x) = x
    w = x
    for _ in range(maxiter):
        # Compute the error between the current estimate of W(x) and the true value
        err = w*np.exp(w) - x
        # If the error is below the tolerance, return the estimate
        if np.abs(err) < tol:
            return w
        # Update the estimate using the Newton-Raphson method
        w -= err/(np.exp(w) + w)
    # If the maximum number of iterations is reached, return the final estimate
    return w


def omega():
    pass 


def wrightomega(z):
    """
    
    https://en.wikipedia.org/wiki/Omega_function
    """
    return omega(z)+log(omega(z))