from abc import ABC, abstractmethod
from typing import List, Tuple

#Classical processing for factorization
from number_factorer.Classical_Factoring.ekera_factorizer import ekera_factorizer
from number_factorer.Classical_Factoring.shor_factorizer import shor_factorizer

# Classical and quantum ordering finding methods
from number_factorer.Order_Finding.Classical.babygiantsteps import baby_giant_order
from number_factorer.Order_Finding.Classical.bad_order_finder import bad_order_finder
from number_factorer.Order_Finding.Quantum.beauregard_circuit import beauregard_circuit
from number_factorer.Order_Finding.Quantum.shor_circuit import shor_circuit
from number_factorer.Order_Finding.Quantum.quantum_order_finder import quantum_order_finder

# Benchmarking methods
from number_factorer.Bench_Marking.shor_factor_estimate import shor_estimate_time
from number_factorer.Bench_Marking.ekera_factor_estimate import ekera_estimate



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

    def is_quantum(self) -> bool:
        """
        Returns True if order finding method is based on a quantum circuit,
        returns False otherwise.
        """
        return False
    
    def get_circuit(self, invertible, modulus):
        """
        For order finding methods that use quantum methods,
        returns a Qiskit quantum circuit of the order finding algorithm
        for invertible modulo modulus if quantum. Returns None otherwise
        """
        return None

#############
# Classical #
#############

class IncrementOrder(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        """
        The most inefficient method possible for computing the order of an invertible
        in the integers modulo the given modulus. Compute invertible ** i mod modulus
        incrementally in i until 1 is achieved.
        """
        
        return bad_order_finder(invertible, modulus)
    
class BabyGiantOrder(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        """
        Finds the order of an invertible element in (Z/modulus * Z)^* using Baby Steps, Giant Steps
        algorithm due to Shanks.
        """
        
        return baby_giant_order(invertible, modulus)

#############
## Quantum ##
#############

class ShorOrder(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        
        return quantum_order_finder(invertible, modulus, shor_circuit, 'shor')
    
    def is_quantum(self):
        return True
    
    def get_circuit(self, invertible, modulus):
        nbits = modulus.bit_length()

        return shor_circuit(invertible, modulus, nbits)

class BeauregardOrder(OrderFindingAlgorithm):
    def find_order(self, invertible: int, modulus: int) -> int:
        
        return quantum_order_finder(invertible, modulus, beauregard_circuit, 'beau')
    
    def is_quantum(self):
        return True
    
    def get_circuit(self, invertible, modulus):
        nbits = modulus.bit_length()

        return beauregard_circuit(invertible, modulus, nbits)


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

    def factor(self, number: int, order_finder: OrderFindingAlgorithm) -> List[Tuple[int, int]]:
        """
        The full factorization algorithm hinted at by Shor in REFERENCE. Takes an integer number
        and provides its full prime factorization in  the form 
        [(p_1, n_1), ..., (p_k, n_k)] where p_i are distinct primes and
        (p_1 ** n_1) * ... * (p_k ** n_k) = number
        """
        return shor_factorizer(number, order_finder)
    
    def quantum_time_estimate(self, number: int, quantum_order_name):
        """
        Estimates the length of time required by a quantum computer to run quantum circuit
        (provided circuit had proper quantum error correction.) quantum_order_name can be either
        'shor' or 'beau'
        """

        return shor_estimate_time(number, quantum_order_name)

    

#############
### Ekera ###
#############
    
class EkeraFactorization(FactorizationAlgorithm):
    def __init__(self):
        self.smallprimeslist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


    def factor(self, number: int, order_finder: OrderFindingAlgorithm, bit_cutoff: int = 2, factoring_rounds: int = 40) -> List[Tuple[int, int]]:
        """
        Factors number with one call to an order finding algorithm. An implementation
        of the algorithm found in "On completely factoring any integer efficiently in 
        a single run of an order-finding algorithm" by Martin Ekera
        """
        
        return ekera_factorizer(number, order_finder, bit_cutoff, factoring_rounds)
    
    def quantum_time_estimate(self, number: int, quantum_order_name):
        """
        Estimates the length of time required by a quantum computer to run quantum circuit
        (provided circuit had proper quantum error correction.) quantum_order_name can be either
        'shor' or 'beau'
        """

        return ekera_estimate(number, quantum_order_name)


################################################
################ ORCHESTRATION #################
################################################

class Number_Factorer:
    def __init__(self, factor_algo: FactorizationAlgorithm, order_algo: OrderFindingAlgorithm):
        self.factor_algo = factor_algo
        self.order_algo = order_algo

    def factor(self, number: int) -> List[Tuple[int, int]]:
        return self.factor_algo.factor(number, self.order_algo)

        





        
        


        