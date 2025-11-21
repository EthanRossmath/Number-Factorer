import random

def random_order_finder(number: int, modulus: int):

    lower = 2
    upper = modulus - 1
    order = random.randint(lower, upper)

    while pow(number, order, modulus) != 1:
        order = random.randint(lower, upper)
    
    upper = order 

    
    return order
