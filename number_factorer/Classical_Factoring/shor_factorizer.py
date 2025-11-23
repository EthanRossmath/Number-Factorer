import gmpy2
from number_factorer.Classical_Factoring.shor_aux.is_power import kroot
from number_factorer.Classical_Factoring.shor_aux.refine import consolidate_pairs
from number_factorer.Classical_Factoring.shor_aux.splitter import splitter

def shor_factorizer(number: int, order_finder):

    prime_list = []
    factor_list = []

    if (number % 2) == 0:

        k = 0
        m = number 

        while (m % 2) == 0:
            k += 1
            m //= 2

        prime_list.append((2, k))
        factor_list.append((m, 1))
    
    else:
        factor_list.append((number, 1))
    
    while len(factor_list) > 0:

        new_list = []

        for a in factor_list:

            if gmpy2.is_prime(a[0]):

                prime_list.append(a)
                continue

            elif gmpy2.is_power(a[0]):

                b = kroot(a[0])
                b[1] = b[1] * a[1]
                new_list.append(tuple(b))

            else:
                x, y = splitter(a[0], order_finder)
                new_list.extend([(x, a[1]), (y, a[1])])

        factor_list = consolidate_pairs(new_list)

    final_list = consolidate_pairs(prime_list)
    return [(int(factor[0]), factor[1]) for factor in final_list]

