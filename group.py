import random

class listPerm:
    
    def __init__(self, n):
        self.start = random.randrange(n)
        self.n=n
        self.i=0
        g = random.randrange(1,n)
        while not isCoprime(n,g):  
            g = (g+1)%n
        self.g = g
    
    def next(self):
        if self.i >= self.n:
            return None
        p = (self.start + self.g*self.i)%self.n
        self.i+=1
        return p
        
    def reset(self):
        self.i=0
        
def isCoprime(a,b):
    if a ==1 or b==1:
        return True
    if a>b:
        return isCoprime(a-b,b)
    if b>a:
        return isCoprime(a,b-a)
    return False