import gmpy2
from number_factorer.Classical_Factoring.shor_aux.is_power import kroot
from number_factorer.Classical_Factoring.shor_aux.refine import consolidate_pairs
from number_factorer.Classical_Factoring.shor_aux.splitter import splitter

def shor_factorizer(number: int, order_finder):
    """
    Takes an integer number and produces a list [(p_1, a_1), ... , (p_k, a_k)]
    where p_1,...,p_k are the distinct prime factors of number and a_1,...,a_k
    are their multiplicities. 

    Works by repeatedly calling on an order finding algorithm to split number
    into increasingly smaller factors.
    """
    # initialize empty lists for the prime factors and remaining factors
    prime_list = []
    factor_list = []

    # remove powers of 2
    if (number % 2) == 0:

        k = 0
        m = number 

        while (m % 2) == 0:
            k += 1
            m //= 2

        # append 2 and its multiplicity to the prime list
        prime_list.append((2, k))

        # move the rest to the factor list
        factor_list.append((m, 1))
    
    else:
        factor_list.append((number, 1))
    
    # continually remove prime factors from factor_list until it is reduced to zero length
    while len(factor_list) > 0:

        # initialize empty list to record splittings of factors
        new_list = []

        for a in factor_list:

            # apply classical (probabalistic) primality test to each element of the factor list
            if gmpy2.is_prime(a[0]):

                prime_list.append(a)
                continue

            # apply classical perfect power test to refine factor list
            elif gmpy2.is_power(a[0]):

                b = kroot(a[0])
                b[1] = b[1] * a[1]
                new_list.append(tuple(b))

            # apply Shor's splitting algorithm to each remaining factor
            # splits factor a into two integers x, y with x * y == a
            else:
                x, y = splitter(a[0], order_finder)
                new_list.extend([(x, a[1]), (y, a[1])])

        # update the factor list, combining repeated factors
        factor_list = consolidate_pairs(new_list)

    # run a consolidation to list of prime factors so each prime appears only once
    final_list = consolidate_pairs(prime_list)

    # convert each prime factor from mpz to int type
    return [(int(factor[0]), factor[1]) for factor in final_list]

