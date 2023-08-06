import math 


__all__ = ['entr','rel_entr','kl_div','hubber','pseudo_huber']

def entr(x):
    if x == 0:
        return 0.0
    elif(x < 0):
        return -math.inf
    else:
        return (-x*math.log(x))


def rel_entr(x,y):
    if (x==0 and y>=0):
        return 0.0
    elif(x > 0 and y>0):
        return (x*math.log(x/y))
    else:
        return math.inf


def kl_div(x,y):
    if(x ==0 and y>=0):
        return float(y)
    elif(x > 0 and y>0):
        return (x*math.log(x/y)-x+y)
    else:
        return math.inf


def hubber(delta,r):
    if(0 <= delta and (abs(r)<=delta)):
        return (1/2)*r**2
    elif(delta <0):
        return math.inf
    else:
        return ((abs(r)-0.5*delta))


def pseudo_huber(delta,r):
    return pow(delta,2)* (math.sqrt(1+((4/3)**2))-1)