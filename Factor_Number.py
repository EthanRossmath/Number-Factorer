from abc import ABC, abstractmethod
from typing import List, Tuple
import math
import random
import gmpy2

#Classical processing for factorization
from .Classical_Factoring.ekera_factorizer import ekera_factorizer
from .Classical_Factoring.shor_factorizer import shor_factorizer

# Classical and quantum ordering finding methods
from .Order_Finding.Classical.babygiantsteps import baby_giant_order
from .Order_Finding.Classical.bad_order_finder import bad_order_finder
from .Order_Finding.Quantum.beauregard_circuit import beauregard_circuit
from .Order_Finding.Quantum.shor_circuit import shor_circuit
from .Order_Finding.Quantum.quantum_order_finder import quantum_order_finder




################################################
########### ORDER FINDING METHODS ##############
################################################

class OrderFindingAlgorithm(ABC):
    @abstractmethod
    def find_order(self, base: int, modulus: int) -> int:
        """Return the smallest integer k so that
            (base ** k) mod modulus == 1 
           base with given modulus."""
        pass

#############
# Classical #
#############

class ClassicalOrderFindingBad(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        """
        The most inefficient method possible for computing the order of an invertible
        in the integers modulo the given modulus. Compute invertible ** i mod modulus
        incrementally in i until 1 is achieved.
        """
        
        if math.gcd(invertible, modulus) !=1:
            return None
    
        exponent = 1

        while pow(invertible, exponent, modulus) != 1:
            exponent += 1

        return exponent
    
class ClassicalOrderFindingBabyGiant(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        """
        Finds the order of an invertible element in (Z/modulus * Z)^* using Baby Steps, Giant Steps
        algorithm due to Shanks.
        """
        b = math.ceil(math.sqrt(modulus - 1))

        look_up_dict = {1:invertible}
        baby_power = invertible

        for i in range(2, b + 1):
            baby_power = (invertible * baby_power) % modulus

            if baby_power == 1:
                return i
        
            else:
                look_up_dict[i] = baby_power
    

        exponent = 2 * b
        big_power = pow(baby_power, 2, modulus)

        while big_power not in look_up_dict.values():
            look_up_dict[exponent] = big_power

            big_power = (big_power * baby_power) % modulus
            exponent = exponent + b
    
        other_exponent = min((j for j in look_up_dict if look_up_dict[j] == big_power))

        return exponent - other_exponent

#############
## Quantum ##
#############

class QuantumShorOrderFinding(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        # placeholder for a quantum routine
        pass


################################################
############ CLASSICAL PROCESSING ##############
################################################

class FactorizationAlgorithm(ABC):
    @abstractmethod
    def factor(self, number: int, order_finder: OrderFindingAlgorithm) -> List[Tuple[int, int]]:
        pass

#############
#### Shor ###
#############

class ShorFactorization(FactorizationAlgorithm):

    ####################
    ## Static Methods ##
    ####################

    @staticmethod
    def power_of_two(number: int) -> List[Tuple[int, int]]:
        """
        Takes an integer and returns a list of pairs. If number is odd, then
        returns [(number, 1)]. If number is even, returns [(2, k), (m, 1)]
        where m is odd and number = (2 ** k) * m
        """

        if (number % 2) != 0:
            return [(number, 1)]
    
        k = 0
        m = number 

        while (m % 2) == 0:
            k += 1
            m //= 2
    
        return [(2, k), (m, 1)]
    
    @staticmethod
    def consolidate_pairs(factor_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Takes a list of pairs of integers [(a_1,n_1), ..., (a_k, n_k)] and consolidates
        them so that the first entries are unique.
        """
        combine_dict = {}
        for a in factor_list:
            if a[0] in combine_dict:
                combine_dict[a[0]] += a[1]
            else:
                combine_dict[a[0]] = a[1]
        combine_list = []
        for a in combine_dict:
            combine_list.append((a, combine_dict[a]))
    
        combine_list.sort(key=lambda x: x[0])
        return combine_list

    @staticmethod
    def kroot(number: int) -> list[int]:
        """
        Takes a number and determines if it is a perfect power. If so, returns
        list [base, exponent] where number = base ** exponent and exponent is
        maximal.
        """
        if not gmpy2.is_power(number):
            return False


        k = number.bit_length()
        exp = 1
        base = number

        for i in range(k, 1, -1):
            val, bool = gmpy2.iroot(number, i)
            if bool:
                exp = i
                base = int(val)
        return [base, exp]


    @staticmethod
    def splitter(number: int, order_finder: OrderFindingAlgorithm) -> List[Tuple[int, int]]:
        """
        The splitting algorithm presented by Shor in REFERENCE. Takes an integer number
        and returns a pair [a, b] of non-trivial factors of number. Requires an order
        finding algorithm.
        """
        if number % 2 == 0:
            return [2, number // 2]
    
        for _ in range(10):  
            a = random.randint(2, number - 1)
            factor = math.gcd(a, number)
            if factor != 1:
                return [factor, number // factor]

            order = order_finder.find_order(a, number)
            if order is None or order % 2 != 0:
                continue

            x = pow(a, order // 2, number) - 1
            factor = math.gcd(x, number)
            if factor != 1 and factor != number:
                return [factor, number // factor]

        return None  
    
    ####################
    ##### Factorer #####
    ####################

    def factor(self, number: int, order_finder: OrderFindingAlgorithm) -> List[Tuple[int, int]]:
        """
        The full factorization algorithm hinted at by Shor in REFERENCE. Takes an integer number
        and provides its full prime factorization in  the form 
        [(p_1, n_1), ..., (p_k, n_k)] where p_i are distinct primes and
        (p_1 ** n_1) * ... * (p_k ** n_k) = number
        """
        prime_list = []
        factor_list = []

        if (number % 2) == 0:
            even, odd = self.power_of_two(number)
            prime_list.append(even)
            factor_list.append(odd)
    
        else:
            factor_list.append((number, 1))
    
        while len(factor_list) > 0:
            new_list = []
            for a in factor_list:
                if gmpy2.is_prime(a[0]):
                    prime_list.append(a)
                    continue
                elif gmpy2.is_power(a[0]):
                    b = self.kroot(a[0])
                    b[1] = b[1] * a[1]
                    new_list.append(tuple(b))
                else:
                    x, y = self.splitter(a[0], order_finder)
                    new_list.extend([(x, a[1]), (y, a[1])])
            factor_list = self.consolidate_pairs(new_list)
        return self.consolidate_pairs(prime_list)
    

#############
### Ekera ###
#############
    
class EkeraFactorization(FactorizationAlgorithm):
    def __init__(self):
        self.smallprimeslist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

    ####################
    ## Static Methods ##
    ####################

    @staticmethod
    def refine(factors: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Based on the paper FACTOR REFINEMENT by Bach et. al. (1993). Takes a list
        of pairs of integers [(a_1, n_1), ..., (a_k, n_k)] and returns a new list
        [(b_1, m_1), ... , (b_r, m_r)] such that

            1) (a_1 ** n_1) * .. * (a_k ** n_k) = (b_1 ** b_1) * .. * (b_r ** m_r)

            2) b_1, ..., b_r are pairwise coprime
        """

        L = factors

        while True:
            pair = None 
            for i in range(len(L)):
                for j in range(i + 1, len(L)):
                    if math.gcd(L[i][0], L[j][0]) != 1:
                        pair = (i, j)
                        break
                if pair:
                    break
            if not pair:
                break 

            i, j = pair

            d = math.gcd(L[i][0], L[j][0])
            new1 = (L[i][0] // d, L[i][1])
            new2 = (d, L[i][1]+L[j][1])
            new3 = (L[j][0] // d, L[j][1])
            new_guys = [new1, new2, new3]

            for idx in sorted([i, j], reverse=True):
                del L[idx]
        
            for newer in new_guys:
                if newer[0] != 1:
                    L.append(newer)
    
        L.sort(key=lambda x: x[0])
        return L
    
    @staticmethod
    def random_invertible(modulus: int) -> int:
        """
        Randomly selects an element of (Z/modulus * Z)^*
        """
        x = random.randint(2, modulus - 1)

        while math.gcd(x, modulus) != 1:
            x = random.randint(2, modulus - 1)
    
        return x
    
    @staticmethod
    def largest_exponent(prime: int, upperbound: int) -> int:
        """
        Returns the largest positive integer a so that prime ** a <= upperbound
        """

        a = 0
        x = 1

        while x < upperbound:
            x = x * prime
            a += 1
    
        return a - 1
    
    @staticmethod
    def kroot(number: int) -> list[int]:
        """
        Takes a number and determines if it is a perfect power. If so, returns
        list [base, exponent] where number = base ** exponent and exponent is
        maximal.
        """
        if not gmpy2.is_power(number):
            return False


        k = number.bit_length()
        exp = 1
        base = number

        for i in range(k, 1, -1):
            val, bool = gmpy2.iroot(number, i)
            if bool:
                exp = i
                base = int(val)
        return [base, exp]
    
    @staticmethod
    def factorization_complete(factor_list: List[Tuple[int, int]]) -> bool:
        """
        Checks if a factorization is complete by checking if each distinct factor
        is prime. Returns True if complete, otherwise returns False.
        """
        for a in factor_list:
            if not gmpy2.is_prime(a[0]):
                return False
    
        return True
    
    ####################
    ## Utility Methods #
    ####################

    def power_refine(self, factor_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Takes a list of factors [(a_1, n_1), ..., (a_k, n_k)] and returns a new list
        [(b_1, m_1), ..., (b_k, m_k)] of the same length such that
            1) b_i ** m_i == a_i ** n_i for all i
            2) b_i <= a_i, m_i => n_i
            3) The m_i are maximal
        """

        new_list = []

        for a in factor_list:
            if gmpy2.is_power(a[0]):
                base, exponent = self.kroot(a[0])
                new_list.append((base, exponent * a[1]))
        
            else: 
                new_list.append(a)
    
        return new_list
    


    def primes_below_cutoff(self, cutoff: int):
        """
        Returns a list of all primes q with the property q < cutoff
        """
        prime_list = []
        for q in range(cutoff):
            if q in self.smallprimeslist:
                prime_list.append(q)
        
            elif gmpy2.is_prime(q):
                prime_list.append(q)
    
        return prime_list

    def add_factor(self, factor_list: List[Tuple[int, int]], new_factor: int) -> List[Tuple[int, int]]:
        """
        factor_list = [(a_1, n_1), ..., (a_k, n_k)] is a factorization of a number N, i.e.
        N = (a_1 ** n_1) * ... * (a_k ** n_k)
        and new_factor is a divisor of N. Outputs a new refined list
        """

        new_list = []

        for a in factor_list:
            d = math.gcd(a[0], new_factor)
            if d == 1:
                new_list.append(a)
            elif a[0] // d == 1:
                new_list.append((d, a[1]))
            else: 
                new_list.extend([(a[0] // d, a[1]), (d, a[1])])

        return self.refine(new_list)


    ####################
    ##### Factorer #####
    ####################

    def factor(self, number: int, order_finder: OrderFindingAlgorithm, bit_cutoff: int = 2, factoring_rounds: int = 40) -> List[Tuple[int, int]]:
        """
        Factors number with one call to an order finding algorithm. An implementation
        of the algorithm found in "On completely factoring any integer efficiently in 
        a single run of an order-finding algorithm" by Martin Ekera
        """
        #0. Initialize list of factors
        factor_list = [(number, 1)]

        #1. Randomly choose an invertible element of {0, ..., number - 1}
        g = self.random_invertible(number)

        #2. Call the order finding algorithm (in this case my very inefficient classical algorithm)
        r = order_finder.find_order(g, number)

        #3. Compute the cut-off for finding primes
        m = bit_cutoff * (number.bit_length())


        #4. Combine all possible factors
        prime_list = self.primes_below_cutoff(m)

        for q in prime_list:
            factor = q ** self.largest_exponent(q, m)

            r = r * factor
    
        #5. Extract the highest power of 2 dividing r and the remaining odd part
        even_exponent = 0
        while (r % 2) == 0:
            r = r // 2
            even_exponent += 1
    
        #6. Find the factors 

        for _ in range(1, factoring_rounds + 1):

            # compute potential source of factors
            x = self.random_invertible(number)

            # raise to maximal odd power
            x = pow(x, r, number)

            if x == 1:
                continue

            for i in range(even_exponent + 1):

                # potential factor
                d = math.gcd(x - 1, number)

                # add to list if non-trivial, return reduced list
                if d > 1:
                    factor_list = self.add_factor(factor_list, d)
            
                # reduce any powers
                factor_list = self.power_refine(factor_list)
            
                # halt if full factorization is complete
                if self.factorization_complete(factor_list):
                    return factor_list
            
                else:
                    x = pow(x, 2, number)
            
                if x == 1:
                    break

        #7. Return factor list
        return factor_list


################################################
################ ORCHESTRATION #################
################################################

class Number_Factorer:
    def __init__(self, factor_algo: FactorizationAlgorithm, order_algo: OrderFindingAlgorithm):
        self.factor_algo = factor_algo
        self.order_algo = order_algo

    def factor(self, number: int) -> List[Tuple[int, int]]:
        return self.factor_algo.factor(number, self.order_algo)

        





        
        


        