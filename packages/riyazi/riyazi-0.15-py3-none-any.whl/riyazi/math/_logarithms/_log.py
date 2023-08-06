__all__ = [ '_ln','_log10','_log2','_log1p','_logb']


def radical(x,y):
    if type(y) == int and type(x) == int:
        if y < 0 and x % 2 == 1:
            return -(abs(y) ** (1 / x))
    return y ** (1 / x)

def _ln(x):
    ans = x - 1
    ans_Pi = 1
    for n in range(1, 2000):
        ans_Pi *= 2 / (1 + radical(2 ** n , x))
    return ans * ans_Pi

def _log10(x):
    return (_ln(x) / _ln(10))

def _log2(x) :
    return (_ln(x)/_ln(2))

def _log1p(x):
    x = x+1
    return _ln(x)

def _logb(x,base):
    result = _ln(x)/_ln(base)
    return result