import math

"""
An attempt to implement the Algorithm found in 

DETECTING PERFECT POWERS  IN ESSENTIALLY LINEAR TIME
by DANIEL J. BERNSTEIN

This is supposedly the fastest known algorithm for determining
if an integer a can be written a = x ^ k for some integers x and k.

Issue: the way floating point arithmetic is handled in that paper
and how Python handles floating point arithmetic are not compatible.
Fortunately, the python library gmpy2 implements this algorithm.
Will have to come back and try to do this myself later on.
"""

# Floating point madness
def div(b, r, k):

    m, e = math.frexp(r)
    n = m * 2 
    a = e - 1

    f =  math.ceil(math.log2(n)) 
    lk = (k - 1).bit_length()

    exp1 = a + f - lk - b
    exp2 = f - lk - b

    return (2 ** exp1) * math.floor(n / ((2 ** exp2) * k))

def trunc(b, r):
    return div(b, r, 1)

def pow_approx(b, r, k):
    """
    Gives a b-bit approximation of the kth power of r
    """
    p = trunc(b, r)
    i = k

    while i > 1:
        if (i % 2) == 0:
            p = trunc(b, p * p) 
            i //= 2
        else:
            p = trunc(b, p * trunc(b, r))
            i -= 1
    return p

# approximating roots

def nrootsmall(b, y, k):
    """
    Computes a b-bit approximation to y ** (-1/k) for 1 <= b <= ceil(log_2(8k))
    """
    g = math.ceil(math.log2(y))
    a = -g // k
    B = math.ceil(math.log2(66 * (2 * k + 1)))

    z = (2 ** a) + (2 ** (a - 1))
    j = 1

    while j != b:
        r = trunc(B, pow_approx(B, z, k) * trunc(B, y))

        if r <= 993 / 1024:
            z = z + 2 ** (a - j - 1)
        
        if r > 1:
            z = z - 2 ** (a - j - 1)
        
        j += 1
    
    return z

def nrootbig(b, y, k):
    """
    Computes a b-bit approximation to y ** (-1/k) for 4 + ceil(log_2(k)) <= b 
    """
    # Precomputation
    l8k = math.ceil(math.log2(8 * k))
    l2k = math.ceil(math.log2(2 * k))
    lk = math.ceil(math.log2(k))

    b_prime = l2k + math.ceil((b - l2k) / 2)
    B = 2 * b_prime + 4 - lk

    if b_prime <= l8k:
        z = nrootsmall(b_prime, y, k)
    else:
        z = nrootbig(b_prime, y, k)
    
    r_2 = trunc(B, z) * (k + 1)
    r_3 = trunc(B, pow_approx(B, z, k + 1) * trunc(B, y))

    return div(B, r_2 - r_3, k)
    
def nroot(b, y, k):
    """
    Computes a b-bit approximation to y ** (-1/k)
    """

    l8k = math.ceil(math.log2(8 * k))

    if b <= l8k:
        return nrootsmall(b, y, k)
    else:
        return nrootbig(b, y, k)
    
def power_check(n, k):

    #Precomputing
    f = math.floor(math.log2(2 * n))
    b = 3 + math.ceil(f / k)
    y = 1 / n

    # The algo
    r = nroot(b, y, k)
    print(r)
    x = 0

    for i in range(math.floor(r - (5 / 8)), math.ceil(r + (5 / 8))+1):
        if n == (i ** k):
            x = i
        if (i == 0) or (-0.25 <= r - i <= 0.25):
            continue

    return x
    
