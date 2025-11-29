import random
import time
import gmpy2

from number_factorer.Order_Finding.Classical.babygiantsteps import baby_giant_order

from number_factorer.Order_Finding.Quantum.quantum_aux.QFT import QFT
from number_factorer.Order_Finding.Quantum.quantum_aux.mod_multiply import shorU

from number_factorer.Classical_Factoring.ekera_factorizer import primes_below_cutoff
from number_factorer.Classical_Factoring.ekera_aux.factor_list_helpers import add_factor, power_refine, factorization_complete

def ekera_estimate_time(number: int, order_algo, bit_cutoff: int = 2, factoring_rounds: int = 40):
    """
    Factors number with one call to an order finding algorithm. An implementation
    of the algorithm found in "On completely factoring any integer efficiently in 
    a single run of an order-finding algorithm" by Martin Ekera
    """
    start = time.perf_counter()
    #0. Initialize list of factors
    factor_list = [(number, 1)]

    #1. Randomly choose an invertible element of {0, ..., number - 1}

    g = random.randint(2, number - 1)

    while gmpy2.gcd(g, number) != 1:
        g = random.randint(2, number - 1)

    #2. Call the order finding algorithm 
    l1 = time.perf_counter()
    r = baby_giant_order(g, number)
    nbits = number.bit_length()

    extra_time = 0
    if order_algo == 'ShorOrder':
        depth = (2 * nbits) * shorU(g, number, nbits).decompose().decompose().decompose().depth() + QFT(2 * nbits).depth()
        extra_time = (500e-09 * (4 * nbits + 1) * depth) + (1e-09) * (nbits ** 3)
    
    if order_algo == 'BeauregardOrder':
        depth = (2 * nbits) * shorU(g, number, nbits).decompose().decompose().decompose().depth() + 4 * (nbits +  (nbits ** 2))
        extra_time = (500e-09 * (2 * nbits + 2) * depth) + (1e-09) * (nbits ** 3)

    l2 = time.perf_counter()

    #3. Compute the cut-off for finding primes
    m = bit_cutoff * (number.bit_length())


    #4. Combine all possible factors
    prime_list = primes_below_cutoff(m)

    for q in prime_list:
        exponent = 0
        x = 1

        while x < m:
            x = x * q
            exponent += 1

        factor = q ** (exponent - 1)

        r = r * factor
    
    #5. Extract the highest power of 2 dividing r and the remaining odd part
    even_exponent = 0
    while (r % 2) == 0:
        r = r // 2
        even_exponent += 1
    
    
    
    #6. Find the factors 

    for _ in range(1, factoring_rounds + 1):

        # compute potential source of factors
        x = random.randint(2, number - 1)

        while gmpy2.gcd(g, number) != 1:
            x = random.randint(2, number - 1)

        # raise to maximal odd power
        x = pow(x, r, number)

        if x == 1:
            continue

        for i in range(even_exponent + 1):

            # potential factor
            d = gmpy2.gcd(x - 1, number)

            # add to list if non-trivial, return reduced list
            if d > 1:
                factor_list = add_factor(factor_list, d)
            
            # reduce any powers
            factor_list = power_refine(factor_list)
            
            # halt if full factorization is complete
            if factorization_complete(factor_list):
                end = time.perf_counter()
                return (end - start) - (l2 - l1) + extra_time
            
            else:
                x = pow(x, 2, number)
            
            if x == 1:
                break

    #7. Return factor list

    end = time.perf_counter()
    return (end - start) - (l2 - l1) + extra_time