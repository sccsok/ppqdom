import math
from utils.primes import *


def invmod(a, p, maxiter=1000000):
    """The multiplicitive inverse of a in the integers modulo p:
         a * b == 1 mod p      求乘法逆元
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p              ### ‘//’运算  5 / 2.0 = 2.5   5 // 2.0 = 2.0
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def modpow(base, exponent, modulus):
    """Modular exponent:
         c = b ^ e mod m
       Returns c.
       (http://www.programmish.com/?p=34)"""
    result = 1
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

class PrivateKey(object):

    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invmod(self.l, n)

    def __repr__(self):
        return '<PrivateKey: %s %s>' % (self.l, self.m)

class PublicKey(object):

    @classmethod
    def from_n(cls, n):
        return cls(n)

    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1

    def __repr__(self):
        return '<PublicKey: %s>' % self.n

def generate_keypair(bits):
    p = generate_prime(bits / 2)
    q = generate_prime(bits / 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

def encrypt(pub, plain):
    while True:
        r = generate_prime(round(math.log(pub.n, 2)))
        if r > 0 and r < pub.n:
            break
    # p1 = pow(r, pub.n)
    # x = p1 % pub.n_sq
    # p2 = pow(pub.g, plain)
    # cipher = ((p2 % pub.n_sq) * x) % pub.n_sq
    #x = pow(r, pub.n, pub.n_sq)
    x = modpow(r, pub.n, pub.n_sq)
    cipher = (modpow(pub.g, plain, pub.n_sq) * x) % pub.n_sq

    return cipher

def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a * b % pub.n_sq

def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * modpow(pub.g, n, pub.n_sq) % pub.n_sq

def e_mul_const(pub, a, n):
    """Multiplies an ancrypted integer by a constant"""
    return modpow(a, n, pub.n_sq)

def decrypt(priv, pub, cipher):
    # p = pow(cipher, priv.l)
    # x = (p % pub.n_sq) - 1
    #x = pow(cipher, priv.l, pub.n_sq) - 1
    x = modpow(cipher, priv.l, pub.n_sq) - 1
    plain = ((x // pub.n) * priv.m) % pub.n
    return plain

# priv, pub = generate_keypair(32)
# print(encrypt(pub, 0))
# print(decrypt(priv, pub, encrypt(pub, 0)))