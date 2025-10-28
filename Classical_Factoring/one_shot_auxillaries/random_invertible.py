import random 
import math

def random_invertible(modulus):
    """
    Randomly selects an element of (Z/modulus * Z)^*
    """
    x = random.randint(2, modulus - 1)

    while math.gcd(x, modulus) != 1:
        x = random.randint(2, modulus - 1)
    
    return x