import math
import random
from Order_Finding.Classical.bad_order_finder import bad_order_finder

def splitter(number: int):
    if number % 2 == 0:
        return [2, number // 2]
    
    for _ in range(10):  
        a = random.randint(2, number - 1)
        factor = math.gcd(a, number)
        if factor != 1:
            return [factor, number // factor]

        order = bad_order_finder(a, number)
        if order is None or order % 2 != 0:
            continue

        x = pow(a, order // 2, number) - 1
        factor = math.gcd(x, number)
        if factor != 1 and factor != number:
            return [factor, number // factor]

    return None  
