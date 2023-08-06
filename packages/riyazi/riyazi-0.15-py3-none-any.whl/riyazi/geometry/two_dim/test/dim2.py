__all__ = ['circle', 'rectangle', 'square', 'decagon', 'ellipse', 'hexagon', 'octagon',
'pentagon', 'pythagors', 'rhombus' ]


from cmath import pi 


def circle(area=None, r=None, c=None , d=None):
    if(area !=None):
        
        radius = (area/pi)**0.5
        circum = 2*pi*radius 
        d = 2*radius
    
        return print(f" Radius : {radius} , Circumference : {circum} , Diametre : {d}")
    if(r !=None):
        
        A = pi*r*r 
        c = 2*pi*r 
        d = 2* r 
 
        return print(f"Area : {A}  , Circumference : {c} , Diametre : {d}")

    if(c !=None):
        
        radius = (c/(2*pi))
        a  = pi*radius*radius 
        d = 2*radius
    
        return print(f"Radius : {radius} , Area :  {a} , Diamterer  {d}") 
    
    if(d != None):
        
        radius = d/2 
        a = pi*radius*radius
        circum = 2*pi*radius
        return print(f" Radius : {radius} , Area :  {a} , Circumference : {circum}")



def rectangle(length, width , area=None , diagonal=None , perimeter=None):
    A = length*width
    diagonal = (width**2+ length**2)**0.5
    p = 2*(length+width)
    
    return f"Area {A} , Diagonal {diagonal} , perimetre {p}"


def square(area= None, diagonal=None , perimeter= None, side=None):
    if(area !=None):
        
        side = area**0.5
        d = 2**0.5 * side 
        p = 4*side
    
        
        return print(f"Side : {side} , Diagonal : {d} , perimeter  {p}")

    
    elif(diagonal !=None):
        s = ((2**0.5)*diagonal/2)
        p = 4*s
        A = s**2
    
    
        return print(f"side : {s} , perimeter : {p} , Area : {A}")
    
    elif(perimeter !=None):
        s = perimeter/4
        A = s**2 
        d = 2**0.5 *s
    
        return print(f"Side : {s} , Area : {A} , Diagonal : {d}")
    
    elif(side !=None):
        
        A = side*side
        d = 2**0.5*side 
        p = 4*side
    
        return print(f"Area : {A} , Diagonal :  {d} , perimeter : {p}")


from math import cos , sqrt, pi 
def decagon(A=None, p=None , a=None):
    if(A !=None):
        a = sqrt(A/cos(pi/10)*2/5)
        p = 10*a
        return a,p 
    if(p !=None):
        a = p/10
        A= 5/2*pow(a,2)*cos(pi/10)
        return a,A
    if(a !=None):
        A = 5/2*pow(a,2)*cos(pi/10)
        p = 10*a
        return A, p 



def ellipse(A=None, a=None, b=None, c=None):
    if(a and b !=None):
        A = pi*a*b
        c = pi*(a+b) * ((3*(a-b)**2) / ((a+b)**2 * (-3*(a-b)**2) / ((a+b)**2)**0.5+4+10)+1)
        return A, c
    
    if(b and A !=None):
        a = A/(pi*b)
        return a
    
    if(a and A !=None):
        b = A/(pi*a)
        return b 


def hexagon(A=None, a=None, p=None, ):
    if(a !=None):
        A = ((3*3**0.5)/2) *a**2
        p = 6*a
        print("(Area , perimeter)")
        return A,p
    if (A !=None):
        a = (3**(1/4)) * (2*(A/9))**0.5
        p = 6*a
        print("(side, perimeter)")
        return a,p
    if(p !=None):
        a = p/6
        A = ((3*3**0.5)/2) *a**2
        print("(side , Area)")
        return a,A


def octagon(A=None, a=None, p=None):
    if(A !=None):
        a= ((2**0.5)*(A/2)-(A/2))
        p= 8*a
        print("(side, perimetre)")
        return a,p 
    if(a !=None):
        A=2*(1+(2**0.5))*a**2
        p = 8*a
        print("(Area , perimetre)")
        return A,p 
    if(p !=None):
        a = p/8
        A=2*(1+(2**0.5))*a**2
        print("(Side , Area)")
        return a,A


def pentagon(A=None , a=None, d=None, p=None):
    if(A !=None):
        a = 2*5**(3/4)* ((A**0.5) / (5*((20**0.5)+5)**(1/4)))
        d = ((1+ (5**0.5))/2 )*a
        p = 5*a
        print("(side , diameter, perimeter)")
        return a, d, p 
    
    if(a !=None):
        A = ((1/4) * (5*(5+(2*5**(0.5))))**0.5 * a**2)
        d = ((1+ (5**0.5))/2 )*a
        p = 5*a 
        print("(Area , diameter , perimeter)")
        return A, d, p 

    if(d !=None):
        a = d*(-1+(5**0.5))/2
        A = ((1/4) * (5*(5+(2*5**(0.5))))**0.5 * a**2)
        p = 5*a
        print("(Side, Area , perimeter)")
        return a , A , p 
    
    if(p !=None):
        a = p/5 
        d = ((1+ (5**0.5))/2 )*a
        A = ((1/4) * (5*(5+(2*5**(0.5))))**0.5 * a**2)
        print("(side , diameter , Area )")
        return a, d, A


import math
def pythagors(p=None,b=None,h=None):
    """
    input p,b return h 
    input h,p return b 
    input h,b return p 
    
    """
    if(p and b  !=None):
        
        h = math.sqrt(p**2 + b**2 )
        return h 
    if(h and p !=None):
        b = math.sqrt(h**2 - p**2)
        return b 
    if( h and b !=None):
        p = math.sqrt(h**2 - b**2)
        return p 


def rhombus(p=None, q=None, A=None, a=None):
    """
    Rhombus 2D shape function  Return value 
    p -> diagonal
    q -> diagonal 
    A -> Area
    a -> side
    p ->perimetre 
    
    """
    if(p and q !=None):
        A = p*q/2
        a = ((p**2+q**2)/2)**0.5
        p = 4*a
        print("(Area , side, perimetre)")
        return A, a, p
    if(q and A !=None):
        p = 2*(A/q)
        return p
    if(p and A !=None):
        q = 2*(A/p)
        return q
    if(a and q !=None):
        p = (4*a**2-q**2)
        return p 
    if(a and p !=None): 
        q = (4*a**2-p**2)
        return q
    if(a !=None):
        p = 4*a
        return p 
        
