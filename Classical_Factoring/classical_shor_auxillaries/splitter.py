import gmpy2
import random

def splitter(number: int, order_finder):

    if number % 2 == 0:
        return [2, number // 2]
    
    for _ in range(10):  
        a = random.randint(2, number - 1)
        factor = gmpy2.gcd(a, number)

        if factor != 1:
            return [factor, number // factor]

        order = order_finder(a, number)

        if order is None or (order % 2) != 0:
            continue

        x = pow(a, order // 2, number) - 1
        factor = gmpy2.gcd(x, number)

        if factor != 1 and factor != number:
            return [factor, number // factor]

    return None  
