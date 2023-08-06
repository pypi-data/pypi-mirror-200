class GG:
    """ Gaussian integer x+iy """
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        if self.y == 0: return str(self.x)
        elif self.x == 0: return str(self.y) + 'j'
        elif self.y < 0:
            return '(' + str(self.x) + str(self.y) + 'j)'
        else:
            return '(' + str(self.x) + '+' + str(self.y) + 'j)'

    def __hash__(self):
        return self.x ^ self.y

    def __neg__(self):
        return GG(-self.x, -self.y)

    def __add__(self, a):
        if isinstance(a, GG):
            return GG(self.x + a.x, self.y + a.y)
        else:
            return GG(self.x + a, self.y)

    def __sub__(self, a):
        if isinstance(a, GG):
            return GG(self.x - a.x, self.y - a.y)
        else:
            return GG(self.x - a, self.y)

    def __mul__(self, a):
        if isinstance(a, GG):
            s = self.x*a.x
            t = self.y*a.y
            u = (self.x - self.y)*(a.y - a.x)
            return GG(s-t, s+t+u)
        else:
            return GG(a*self.x, a*self.y)

    def __truediv__(self, a):
        """ self = aq + r, norm(r) <= norm(a)/2 """
        if isinstance(a, GG):
            self *= conj(a)
            a = norm(a)
        elif a<0: self,a = -self,-a
        x,r = divmod(self.x, a)
        y,s = divmod(self.y, a)
        a2 = a//2
        if r > a2: x += 1
        if s > a2: y += 1
        return GG(x,y)

    def __mod__(self, a):
        q = self/a
        return self - a*q

    def __divmod__(self, a):
        q = self/a
        return q, self - a*q

    def __pow__(self, e):
        """ assume e>=0 """
        if e==0: return GG(1)
        n = (1<<(e.bit_length()-1))>>1
        a = self
        while n:
            a *= a
            if e&n: a *= self
            n>>=1
        return a

    def __eq__(self, a):
        if isinstance(a, GG):
            return self.x == a.x and self.y == a.y
        else:
            return self.x == a and self.y == 0

    def __ne__(self, a):
        return not self.__eq__(a)

    def __radd__(self, a):
        return GG(a + self.x, self.y)

    def __rsub__(self, a):
        return GG(a - self.x, -self.y)

    def __rmul__(self, a):
        return GG(a*self.x, a*self.y)

    def __rtruediv__(self, a):
        return GG(a).__truediv__(self)

    def __rmod__(self, a):
        return GG(a).__mod__(self)

    def __rdivmod__(self, a):
        return GG(a).__divmod__(self)

    def __complex__(self):
        return complex(self.x, self.y)

def real(a): return a.x
def imag(a): return a.y
def norm(a): return a.x**2 + a.y**2

def conj(a): return GG(a.x, -a.y)
def IsUnit(a): return (a.y==0 and abs(a.x)==1)\
                   or (a.x==0 and abs(a.y)==1)
def mul_i(a): return GG(-a.y, a.x) # a*i
def div_i(a): return GG(a.y, -a.x) # a/i

def IsAssoc(a, b, exponent=False):
    """ test if a == b*i^e for some e (e=0,1,2,3)
    if exponent is False, return True or False
    else if a is associate of b, return e
    else return -1
    """
    if   a == b: e=0
    elif a == -b: e=2
    elif a == mul_i(b): e=1
    elif a == div_i(b): e=3
    else: e=-1
    if exponent: return e
    else: return e>=0

def mul_ipow(a,e):
    """ a*i^e """
    e &= 3
    if   e==2: return -a
    elif e==1: return mul_i(a)
    elif e==3: return div_i(a)
    else: return a

def quadrant(a):
    """ return -1 if a==0,
    0 if Re(a)>0 and Im(a)>=0,
    1 if Re(a)<=0 and Im(a)>0,
    2 if Re(a)<0 and Im(a)<=0,
    3 if Re(a)>=0 and Im(a)<0
    """
    if a.x==0:
        if a.y==0: return -1
        elif a.y>0: return 1
        else: return 3
    elif a.x>0:
        if a.y<0: return 3
        else: return 0
    elif a.y>0: return 1
    else: return 2

def FirstQuad(a, exponent=False):
    """ return b = a*i^e for some e (e=0,1,2,3)
    in first quadrant Re(b)>0 and Im(b)>=0
    if exponent is True, return b and e
    if a is zero, then b=0 and e=0
    """
    e = quadrant(a)
    e = 4-e if e>0 else 0
    b = mul_ipow(a,e)
    if exponent: return b,e
    else: return b

def GCD(a,b):
    """ d = greatest common divisor of a and b
    in first quadrant Re(d)>0 and Im(d)>=0
    by Euclidean algorithm
    if a and b are both zero, then d=0
    """
    while b!=0: a,b = b,a%b
    return FirstQuad(a)

def XGCD(a,b):
    """ d = greatest common divisor of a and b
    in first quadrant Re(d)>0 and Im(d)>=0
    by extended Euclidean algorithm
    return d,s,t such that d = s*a + t*b
    if a and b are both zero, then d,s,t=0,1,0
    """
    s,t = GG(1),GG(0)
    u,v = GG(0),GG(1)
    while b!=0:
        q,r = divmod(a,b)
        s,u = u, s-u*q
        t,v = v, t-v*q
        a,b = b,r
    d,e = FirstQuad(a, True)
    s = mul_ipow(s,e)
    t = mul_ipow(t,e)
    return d,s,t

#########################################################
from sympy import sqrt_mod, factorint, randprime, isprime
from fractions import gcd
from random import randrange

def SqrRoot(n):
    """ floor(sqrt(n)) for huge integer n """
    x,y = n+1,n
    while x>y: x,y = y, (y + n//y)//2
    return x

def cornacchia(p):
    """ given a prime number p where p==1 (mod 4),
    find x,y such that x*x + y*y = p and x>y>0
    by cornacchia algorithm
    referece: H. Wada
      "Prime Factorization by Computers" (in Japanese) p69
    """
    x,y = p, sqrt_mod(p-1, p)
    s = SqrRoot(p)
    while x>s: x,y = y,x%y
    return x,y

def factor(a):
    """ factorize a into gaussian primes
    return dictionary of (prime, exponent) pair
    such that product of p**e is associate of a
    real factors are positive and
    imaginary factors are in first quadrant
    """
    if not isinstance(a,GG): a = GG(a)
    f = {}
    if a==0 or IsUnit(a): return f
    d = abs(gcd(real(a), imag(a)))
    if d>1: a /= d
    g = factorint(norm(a))
    h = factorint(d)

    k = g.pop(2,0) + 2*h.pop(2,0)
    if k: f[GG(1,1)] = k
    for k in h:
        if k&3 == 3: f[k] = h[k]
        else:
            x,y = cornacchia(k)
            p,q = GG(x,y),GG(y,x)
            f[p],f[q] = h[k],h[k]
            if k in g:
                if a%p == 0: f[p] += g.pop(k)
                else:        f[q] += g.pop(k)
    for k in g:
        x,y = cornacchia(k)
        p = GG(x,y)
        if a%p != 0: p = GG(y,x)
        f[p] = g[k]

    return f

def IsPrime(a):
    """ test if a is gaussian prime """
    if not isinstance(a,GG): a = GG(a)
    if   imag(a)==0: b = abs(real(a))
    elif real(a)==0: b = abs(imag(a))
    else: b = -1
    if b>=0: return b&3 == 3 and isprime(b)
    b = norm(a)
    return b==2 or (b&3 == 1 and isprime(b))

def GenPrime(l):
    """ generate random gaussian prime p
    such that bit length of norm(p) is l and
    p is in first quadrant Re(p)>0 and Im(p)>0
    assume l>=2
    """
    while True:
        p = randprime(1<<(l-1), 1<<l)
        if p == 2: return GG(1,1)
        if p%4 == 1:
            x,y = cornacchia(p)
            if randrange(2): return GG(x,y)
            else:            return GG(y,x)
