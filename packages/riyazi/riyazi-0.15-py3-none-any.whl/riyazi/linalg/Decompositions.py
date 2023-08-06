
__all__ = ['lu','naive_lu_factor','lu_factor','ufsub','bsub']

import numpy as np 
def lu(A):

    # Return an error if matrix is not square
    if not A.shape[0]==A.shape[1]:
        raise ValueError("Input matrix must be square")

    n = A.shape[0] 

    L = np.zeros((n,n),dtype='float64') 
    U = np.zeros((n,n),dtype='float64') 
    U[:] = A 
    np.fill_diagonal(L,1) # fill the diagonal of L with 1

    for i in range(n-1):
        for j in range(i+1,n):
            L[j,i] = U[j,i]/U[i,i]
            U[j,i:] = U[j,i:]-L[j,i]*U[i,i:]
            U[j,i] = 0
    return (L,U)

def naive_lu_factor(A):
    """
        No pivoting.

        Overwrite A with:
            U (upper triangular) and (unit Lower triangular) L 
        Returns LU (Even though A is also overwritten)
    """
    n = A.shape[0]
    for k in range(n-1):                
        for i in range(k+1,n):          
            A[i,k] = A[i,k]/A[k,k]      # " L[i,k] = A[i,k]/A[k,k] "
            for j in range(k+1,n):      
                A[i,j] -= A[i,k]*A[k,j] # " U[i,j] -= L[i,k]*A[k,j] "

    return A # (if you want)


def lu_factor(A):
    """
        LU factorization with partial pivorting

        Overwrite A with: 
            U (upper triangular) and (unit Lower triangular) L 
        Return [LU,piv] 
            Where piv is 1d numpy array with row swap indices 
    """
    n = A.shape[0]
    piv = np.arange(0,n)
    for k in range(n-1):

        # piv
        max_row_index = np.argmax(abs(A[k:n,k])) + k
        piv[[k,max_row_index]] = piv[[max_row_index,k]]
        A[[k,max_row_index]] = A[[max_row_index,k]]

        # LU 
        for i in range(k+1,n):          
            A[i,k] = A[i,k]/A[k,k]      
            for j in range(k+1,n):      
                A[i,j] -= A[i,k]*A[k,j] 

    return [A,piv]


def ufsub(L,b):
    """ Unit row oriented forward substitution """
    for i in range(L.shape[0]): 
        for j in range(i):
            b[i] -= L[i,j]*b[j]
    return b


def bsub(U,y):
    """ Row oriented backward substitution """
    for i in range(U.shape[0]-1,-1,-1): 
        for j in range(i+1, U.shape[1]):
            y[i] -= U[i,j]*y[j]
        y[i] = y[i]/U[i,i]
    return y