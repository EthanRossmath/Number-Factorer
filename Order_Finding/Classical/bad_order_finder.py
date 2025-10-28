import math

"""
This is the simplest (and presumably least efficient) algorithm
for finding the order of an element of the multiplicative group
of the integers modulo N for any N. 
"""

def bad_order_finder(number: int, modulus: int):

    if math.gcd(number, modulus) !=1:
        return None
    
    exponent = 1

    while pow(number, exponent, modulus) != 1:
        exponent += 1

    return exponent