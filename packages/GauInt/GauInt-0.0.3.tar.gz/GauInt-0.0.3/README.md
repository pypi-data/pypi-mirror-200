# GauInt: Gaussian integers
```
GG(x=0, y=0):
construct gaussian integer x+iy
where x and y are ordinary integers and i is imaginary unit.
|x| and |y| can be arbitrarily large.

Addition a+b, subtraction a-b, multiplication a*b,
division a/b, remainder a%b, division with remainder divmod(a,b),
equality testing a==b, inequality testing a!=b
can be performed on two GG objects a and b. On these operations,
one of a and b can be an ordinary integer (built in python).
Division with remainder q,r = a/b,a%b is such that a = b*q + r
and norm(r) <= norm(b)/2, where norm(a) = Re(a)**2 + Im(a)**2.
Exponentiation a**e can be performed on GG object a and
non-negative ordinary integer e.
-------------------------------------------------------------
Utility functions:

real(a): real part Re(a) of a
imag(a): imaginary part Im(a) of a
norm(a): norm Re(a)**2 + Im(a)**2 of a
conj(a): conjugate Re(a) - i*Im(a) of a
IsUnit(a): test if norm(a)==1
mul_i(a): a*i
div_i(a): a/i
mul_ipow(a,e): a*i**e

complex(a):
convert GG object to floating-point complex number.

IsAssoc(a, b, exponent=False):
test if a==b*i**e for some e (e=0,1,2,3).
If exponent is False, return True or False,
else if a is associate of b, return e,
else return -1.

quadrant(a):
return -1 if a==0,
return 0 if Re(a)>0 and Im(a)>=0,
return 1 if Re(a)<=0 and Im(a)>0,
return 2 if Re(a)<0 and Im(a)<=0,
return 3 if Re(a)>=0 and Im(a)<0.

FirstQuad(a, exponent=False):
return b = a*i^e for some e (e=0,1,2,3)
in first quadrant Re(b)>0 and Im(b)>=0.
If exponent is True, return b and e.
If a is zero, then b=0 and e=0.

GCD(a,b):
return d = greatest common divisor of a and b
in first quadrant Re(d)>0 and Im(d)>=0.
If a and b are both zero, then d=0.

XGCD(a,b):
compute d = greatest common divisor of a and b
in first quadrant Re(d)>0 and Im(d)>=0,
and return d,s,t such that d = s*a + t*b.
If a and b are both zero, then d,s,t=0,1,0.

factor(a):
factorize a into gaussian primes, and
return dictionary of (prime, exponent) pair
such that product of p**e is associate of a.
Real factors are positive and
imaginary factors are in first quadrant.

IsPrime(a):
test if a is gaussian prime,
and return True or False

GenPrime(l):
generate random gaussian prime p
such that bit length of norm(p) is l and
p is in first quadrant Re(p)>0 and Im(p)>0.
l must be larger than 1.
```
# example usage:
```
>>> from GG import GG,GCD,XGCD
>>> a,b,c = GG(2,3), GG(4,5), GG(6,7)
>>> a *= c; b *= c
>>> d = GCD(a,b)
>>> print(d)
(6+7j)
>>> d,s,t = XGCD(a,b)
>>> print(d == s*a + t*b)
True
```
# example usage:
```
>>> from GG import IsPrime,factor
>>> IsPrime(5), IsPrime(7)
(False, True)
>>> factor(5), factor(7)
({(2+1j): 1, (1+2j): 1}, {7: 1})
```
# example usage:
```
>>> from GG import GenPrime,factor,IsAssoc
>>> a,b,c = GenPrime(8), GenPrime(8), GenPrime(8)
>>> a = a**2 * b**3 * c**4
>>> print(a)
(-12320219833+13665386778j)
>>> f = factor(a)
>>> print(f)
{(11+6j): 3, (14+1j): 4, (15+4j): 2}
>>> b = 1
>>> for k in f: b *= k**f[k]
...
>>> print(IsAssoc(a,b))
True
```