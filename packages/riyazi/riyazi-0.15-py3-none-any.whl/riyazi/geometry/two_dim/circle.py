
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
        
        
        









