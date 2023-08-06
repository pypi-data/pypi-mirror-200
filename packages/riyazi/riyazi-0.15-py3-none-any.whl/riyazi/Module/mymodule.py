def compound_interest(principal,rate,years):
    amount=principal*(1+rate/100)**years
    return amount 


from math import sqrt
def Heron(a,b,c):
    s=(a+b+c)/2.0
    A=sqrt(s*(s-a)*(s-b)*(s-c))
    return A

def is_triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        return True
    else:
        return False
def Triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        if(a==b and b==c):
            print("Equalteral triangle")
        elif (a==b or b==c or a==c):
            print("Isoceles triangle")
        else:
            print("scalene triangle")
    else:
        print("Not a triangle")


from math import sqrt
from cmath import sqrt as csqrt 
def solve_quad(a,b,c):
    if(a==b):
        if(b!=0):
            x1= -c/b
            print(f"it has only one root, x1 ={x1}")
        else:
            print("it has no root")
    else:
        d=b**2-4*a*c
        if(d>0):
            print('Roots are real')
            x1=(-b+sqrt(b**2-4*a*c))/(2*a)
            x2=(-b-csqrt(b**2-4*a*c))/(2*a)
            print(f'The roots of are {x1} and {x2}')

def isPrime(n):
    if n<2:
        return False
    if n==2:
        return True
    if n%2==0:
        return False
    for k in range(3,int(n**0.5)+1,2):
        if n%k ==0:
            return False
        return True


def mygcd(a,b):
    a, b = abs(a), abs(b)
    if(a==0):
        if(b==0):
            
            gcd='gcd does not exist'
        else:
            gcd=b
    else:
        if(b==0):
            gcd=a
        else:
            if(a<b):
                a,b=b,a
            while(a%b!=0):
                a,b=b,a%b
            gcd=b
    return gcd


def Newton_raphson(f, df ,x0, max_it=20, tol=1e-5):
    f0 = f(x0)
    itr = 0
    while(abs(f(x0))>=tol and itr<=max_it):
        x1 = x0-f0/df(x0)
        x0 = x1
        f0 = f(x0)
        itr +=1
        converged = itr<max_it
        return x0,converged, itr
    
    
from math import exp
f = lambda x: x**2-3*x+exp(-2*x)
df = lambda x: 2*x-3-2*exp(-2*x)
sol, converged, itr = Newton_raphson(f, df, 100, tol=1e-5)
if converged:
    print(f'Newtons method converged in {itr} iterrations')
    print(f'The solution is {sol}')
else:
    print(f'Newtons method did not converge ')
    