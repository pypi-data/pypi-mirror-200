def rectangle(length, width , area=None , diagonal=None , perimeter=None):
    A = length*width
    diagonal = (width**2+ length**2)**0.5
    p = 2*(length+width)
    
    return f"Area {A} , Diagonal {diagonal} , perimetre {p}"
    