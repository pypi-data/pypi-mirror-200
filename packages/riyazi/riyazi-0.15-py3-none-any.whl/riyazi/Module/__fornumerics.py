__all__ = ['around','argmax','amax','argmin','amin','size']

def around(x):
    return round(x)

def amax(arr):
    return max(arr)


def argmax(arr):
    arr = list(arr)
    lists  = max(arr)
    return arr.index(lists)

def argmin(arr):
    arr = list(arr)
    lists  = min(arr)
    return arr.index(lists)

def amin(arr):
    return min(arr)



def size(arr):
    for x in arr:
        cout = x
    return cout