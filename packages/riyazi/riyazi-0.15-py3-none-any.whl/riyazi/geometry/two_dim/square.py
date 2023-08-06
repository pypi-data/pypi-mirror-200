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
        
        
 
    
        
        
