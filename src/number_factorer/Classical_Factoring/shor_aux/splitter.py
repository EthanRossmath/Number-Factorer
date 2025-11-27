import gmpy2
import random
from typing import List, Tuple

def splitter(number: int, order_finder) -> List[Tuple[int, int]]:
        """
        The splitting algorithm presented by Shor in REFERENCE. Takes an integer number
        and returns a pair [a, b] of non-trivial factors of number. Requires an order
        finding algorithm.
        """
        if number % 2 == 0:
            return [2, number // 2]
    
        for _ in range(10):  
            a = random.randint(2, number - 1)
            factor = gmpy2.gcd(a, number)

            if factor != 1:
                return [factor, number // factor]

            order = order_finder.find_order(a, number)
            if order is None or order % 2 != 0:
                continue

            x = pow(a, order // 2, number) - 1
            factor = gmpy2.gcd(x, number)
            
            if factor != 1 and factor != number:
                return [factor, number // factor]

        return None  
