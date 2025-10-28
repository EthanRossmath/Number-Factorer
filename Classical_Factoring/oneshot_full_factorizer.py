import math
from Order_Finding.Classical.bad_order_finder import bad_order_finder
from one_shot_auxillaries.adding_factors import add_factor
from one_shot_auxillaries.random_invertible import random_invertible
from one_shot_auxillaries.prime_below_cutoff import primes_below_cutoff
from one_shot_auxillaries.largest_exponent import largest_exponent
from one_shot_auxillaries.power_refine import power_refine
from one_shot_auxillaries.is_complete_factor import factorization_complete




def one_shot_factorizer(number: int, bit_cutoff: int = 2, factoring_rounds: int = 40):
    """
    Factors number with one call to an order finding algorithm. An implementation
    of the algorithm found in "On completely factoring any integer efficiently in 
    a single run of an order-finding algorithm" by Martin Ekera
    """
    #0. Initialize list of factors
    factor_list = [(number, 1)]

    #1. Randomly choose an invertible element of {0, ..., number - 1}
    g = random_invertible(number)

    #2. Call the order finding algorithm (in this case my very inefficient classical algorithm)
    r = bad_order_finder(g, number)

    #3. Compute the cut-off for finding primes
    m = bit_cutoff * (number.bit_length())


    #4. Combine all possible factors
    prime_list = primes_below_cutoff(m)

    for q in prime_list:
        factor = q ** largest_exponent(q, m)

        r = r * factor
    
    #5. Extract the highest power of 2 dividing r and the remaining odd part
    even_exponent = 0
    while (r % 2) == 0:
        r = r // 2
        even_exponent += 1
    
    #6. Find the factors 

    for _ in range(1, factoring_rounds + 1):

        # compute potential source of factors
        x = random_invertible(number)

        # raise to maximal odd power
        x = pow(x, r, number)

        if x == 1:
            continue

        for i in range(even_exponent + 1):

            # potential factor
            d = math.gcd(x - 1, number)

            # add to list if non-trivial, return reduced list
            if d > 1:
                factor_list = add_factor(factor_list, d)
            
            # reduce any powers
            factor_list = power_refine(factor_list)
            
            # halt if full factorization is complete
            if factorization_complete(factor_list):
                return factor_list
            
            else:
                x = pow(x, 2, number)
            
            if x == 1:
                break

    #7. Return factor list
    return factor_list