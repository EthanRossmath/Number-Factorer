import numpy as np
import random

def random_order_finder(number: int, modulus: int):

    order = random.randint(2, modulus - 1)

    while pow(number, order, modulus) != 1:
        order = random.randint(2, modulus - 1)
    
    return order
