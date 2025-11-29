import random
import time
import gmpy2

from number_factorer.Classical_Factoring.shor_aux.is_power import kroot
from number_factorer.Classical_Factoring.shor_aux.refine import consolidate_pairs

from number_factorer.Order_Finding.Classical.babygiantsteps import baby_giant_order

from number_factorer.Order_Finding.Quantum.shor_circuit import shor_circuit
from number_factorer.Order_Finding.Quantum.beauregard_circuit import beauregard_circuit



def shor_estimate_time(number, quantum_order_name):
    start = time.perf_counter()
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
        if m > 1:
            factor_list.append((m, 1))
    
    else:
        factor_list.append((number, 1))
    
    # continually remove prime factors from factor_list until it is reduced to zero length
    lost_time = []
    gain_time = []
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
                l1 = time.perf_counter()
                subfactors = None
                inv = 1 
                order = 0
                algo_ran = False
                nbits = a[0].bit_length()

                for _ in range(10):  
                    r = random.randint(2, a[0] - 1)
                    factor = gmpy2.gcd(r, a[0])

                    if factor != 1:
                        subfactors = [factor, a[0] // factor]
                        break
                    
                    algo_ran = True
                    inv = r

                    order = baby_giant_order(r, a[0])
                    if order is None or order % 2 != 0:
                        continue

                    x = pow(r, order // 2, a[0]) - 1
                    factor = gmpy2.gcd(x, a[0])
            
                    if factor != 1 and factor != a[0]:
                        subfactors =  [factor, a[0] // factor]
                        break

                if subfactors is None:
                    new_list.append((a[0], a[1]))
                
                else:
                    new_list.extend([(subfactors[0], a[1]), (subfactors[1], a[1])])

                extra_time = 0
                if quantum_order_name == 'shor' and algo_ran:
                    qc = shor_circuit(inv, a[0], nbits)

                    extra_time = (500e-09) * (qc.depth()) * (qc.num_qubits)
                
                if quantum_order_name == 'beau' and algo_ran:
                    qc = beauregard_circuit(inv, a[0], nbits)

                    extra_time = (500e-09) * (qc.depth()) * (qc.num_qubits)
                
                gain_time.append(extra_time)

                lost_time.append(time.perf_counter() - l1)

        # update the factor list, combining repeated factors
        factor_list = consolidate_pairs(new_list)

    # run a consolidation to list of prime factors so each prime appears only once
    final_list = consolidate_pairs(prime_list)

    # convert each prime factor from mpz to int type
    end = time.perf_counter()

    return (end - start) + sum(gain_time) - sum(lost_time)