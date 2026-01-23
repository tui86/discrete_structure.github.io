import math
import cmath
def prime(start, end, print_solution=False):
    """Find and output prime numbers from start to end."""
    prime=[i for i in range(min(start, end), max(start, end)+1) if is_prime(i, 0)]
    if print_solution:
        print(prime)
    return prime                 
def is_prime(number, print_solution=False):
    if number<=1: 
        if print_solution: print("NO")
        return False
    if number==2:
        if print_solution: print("YES")
        return True
    for b in range(2, math.ceil(math.sqrt(number)+1)):
        if  number%b==0: 
            if print_solution: print("NO")
            return False
    else: 
        if print_solution: print("YES")
        return True              
def fibonacci(quantily, print_solution=False):
    f=[]
    if not quantily:
        if print_solution: print("0")
        return f
    f=[0, 1]
    while(len(f)<quantily):
        f.append(f[-1]+f[-2])
    if print_solution: print(f)
    return f    
def is_fibonacci(number, print_solution=False):
    b=1
    c=0
    while(number< b):
        c, b= b, b+c
    if number==b:
        if print_solution: print("YES")
        return True
    else:
        if print_solution: print("NO")
        return False
def solve_linear(a, b, print_solution=False):
    if a==0:
        if b==0:
            if print_solution: print("countless solutions")
            return 0
        elif b!=0:
            if print_solution: print("no solution")
            return 0
    else:
        if print_solution: print("value is: ", (-b)/a)
        return (-b)/a
def slove_quadratic(a, b, c, print_solution=False):
     if a==0:
        solve_linear(b, c, True)
     delta= b*b-4*a*c
     if delta<0:
        x1=((-b)-cmath.sqrt(delta))/(2*a)
        x2=((-b)+cmath.sqrt(delta))/(2*a)
        if print_solution: print("x1= ", x1)
        if print_solution: print("x2= ", x2)
        return x1, x2
     else:   
        x1=((-b)-math.sqrt(delta))/(2*a)
        x2=((-b)+math.sqrt(delta))/(2*a)
        if print_solution: print("x1= ", x1)
        if print_solution: print("x2= ", x2)
        return x1, x2
def palindrome(start, end, print_solution=False):
    f=[]
    for c in range(start, end+1):
        e=c
        d=0
        while(e):
            d=e%10+d*10
            e=e//10   
        if d==c: 
            if print_solution: print(c, end=" ")
            f.append(c)
    return f        
def is_palindrome(number, print_solution=False):
    if str(number)==str(number)[::-1]:
        if print_solution: print("YES")
        return True
    else:
        if print_solution: print("NO")
        return False
def square_number(start, end, print_solution=False):
    d=[]
    for c in range(start, end+1):
        if math.sqrt(c)==round(math.sqrt(c)):
            if print_solution: print(c, end=" ")
            d.append(c)
    return d        
def is_square_number(number, print_solution=False):
    if math.sqrt(number)==round(math.sqrt(number)):
        if print_solution: print("YES", end=" ")
        return True
    else:
        if print_solution: print("NO", end=" ")
        return False
def divisor(number, print_solution=False):
    c=[]
    for b in range(1, round(number/2+1)):
         if number%b==0: 
            if print_solution: print(b, end=" ")
            c.append(b)
    if print_solution: print(number)
    if number not in c:
        c.append(number)
    return c
def multiples(number, quantily, print_solution=False):
    d=[]
    for c in range(1, quantily+1):
        if print_solution: print(c*number, end=" ")
        d.append(c*number)
    return d    
__all__=["prime", "is_prime","fibonacci", "is_fibonacci", "slove_linear", "slove_quadratic", "palidrome", "is_paridrome", "square_number", "is_square_number", "divisor", "multiples"]
if __name__=="__main__":
    print(divisor(1))