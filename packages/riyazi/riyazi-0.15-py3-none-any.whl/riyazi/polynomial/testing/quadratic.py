from riyazi.Module.numeric import sqrt , pow 



def quadratic(a, b, c):
    """
    Quadratic formula: (-b + or - sqrt(b^2 - 4ac)) / 2a
    :a, b, c: coefficents

    """
    disc_root =sqrt(pow(b, 2) - 4 * a * c)
    denom = (2 * a)
    root_1 = (-b + disc_root) / denom
    root_2 = (b - disc_root) / denom

    return root_1,  root_2