
__all__ = ['inv', 'solve', 'solve_banded', 'solveh_banded', 'solve_circulant', 'solve_triangular',
'solve_toeplitz', 'matmul_toeplitz', 'det', 'norm', 'lstsq1', 'pinv', 'pinvh', 'kron','khatri_rao',
'tril', 'triu', 'orthogonal_procrustes', 'matrix_balance', 'subspace_angles', 'bandwidth', 
'issymmetric', 'ishermitian']


import numpy as np 
from scipy import linalg
def inv(a):
    determinant = linalg.det(a)
    if len(a) == 2:
        return np.array([[a[1][1]/determinant, -1*a[0][1]/determinant],
                [-1*a[1][0]/determinant, a[0][0]/determinant]])

def solve(a,b):
    import numpy.linalg as ln 
    x = ln.inv(a).dot(b)
    return np.array(x)