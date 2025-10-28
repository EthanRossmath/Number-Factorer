import gmpy2
from Classical_Factoring.classical_shor_auxillaries.is_power import kroot
from Classical_Factoring.classical_shor_auxillaries.power_of_two import power_of_two
from Classical_Factoring.classical_shor_auxillaries.refine import consolidate_pairs
from Classical_Factoring.classical_shor_auxillaries.splitter import splitter

def full_factorizer(n):
    prime_list = []
    factor_list = []

    if (n % 2) == 0:
        even, odd = power_of_two(n)
        prime_list.append(even)
        factor_list.append(odd)
    
    else:
        factor_list.append((n, 1))
    
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
                x, y = splitter(a[0])
                new_list.extend([(x, a[1]), (y, a[1])])
        factor_list = consolidate_pairs(new_list)
    return consolidate_pairs(prime_list)