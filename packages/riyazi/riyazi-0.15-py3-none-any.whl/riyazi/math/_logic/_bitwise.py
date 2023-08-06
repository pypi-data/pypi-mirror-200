def logical_and(x1,x2):
    return (x1&x2)

def logical_not(x):
    return not x 

def logical_or(x1,x2):
    return (x1|x2)

def logical_xor(x1,x2):
    return (x1^x2)

def bitwise_and(x1,x2):
    return (logical_and(x1,x2))

def bitwise_not(x):
    return logical_not(x)

def bitwise_or(x1,x2):
    return logical_or(x1,x2)


def bitwise_xor(x1,x2):
    return logical_xor(x1,x2)