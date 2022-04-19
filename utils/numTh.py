import math
import random
import numpy as np
from sympy import isprime, nextprime
from sympy.ntheory.residue_ntheory import nthroot_mod


def findPrimes(prime_bit, num):
    primes = []
    total_bits = 0
    prime = pow(2, prime_bit - 1)
    while len(primes) != num:
        prime = nextprime(prime)
        primes.append(prime)

    return primes, total_bits


def findPrimitiveNthRoot(M, N):
    """
    Generate the smallest primitive Nth root of unity (expect 1).
    Find w s.t w^N = 1 mod M and there are not other numbers k (k < N) 
    s.t w^k = 1 mod M 

    """
    roots = nthroot_mod(1, N, M, True)[1:]  # find Nth root of unity
    for root in roots:  # find primitive Nth root of unity
        is_primitive = True
        for k in range(1, N):
            if pow(root, k, M) == 1:
                is_primitive = False
        if is_primitive:
            return root
    return None


def isPrimitiveNthRoot(M, N, beta):
    """
    verify B^N = 1 (mod M)
    """
    return pow(beta, N, M) == 1     # modular(M).modExponent(beta, N) == 1


def uniform_sample(upper, num):
    """
    Sample num values uniformly between [0,upper).
    """
    sample = []
    for i in range(num):
        value = random.randint(0, upper - 1)
        sample.append(value)
    return sample


def gauss_sample(num, stdev):
    """
    Sample num values from gaussian distribution
    mean = 0, standard deviation = stdev 
    """
    sample = np.random.normal(0, stdev, num)
    sample = sample.round().astype(int)
    return sample


def hamming_sample(num):
    """
    Sample a vector uniformly at random from -1, 0, +1,
    subject to the condition that it has exactly hwt nonzero entries. 
    """
    i = 0
    sample = []
    while i < num:
        coeff = random.randint(-1, 1)
        sample.append(coeff)
        i += 1
    return sample

def small_sample(num):
    """
    Sample vectors with entires -1, 0, +1.
    Each element is 0 with probabilty 0.5 and +-1 with probabilty 0.25. 
    """
    sample = [0] * num
    for i in range(num):
        u = random.randint(0, 3)
        if u == 3:
            sample[i] = -1
        if u == 2:
            sample[i] = 1
    return sample

# Not used
