import numpy as np
from qiskit_aer import AerSimulator
from qiskit import transpile
from number_factorer.Order_Finding.Quantum.quantum_aux.continued_fractions import get_denominator

def quantum_order_finder(number, modulus, quantum_circuit, algo_name):

    if np.gcd(number, modulus) != 1:
        print(f'{number} is not invertible modulo {modulus}')
        return 0

    nbits = modulus.bit_length() 

    qc = quantum_circuit(number, modulus, nbits)

    # simulate runs number of times, taking the result each time.
    aer_simulator = AerSimulator()
    transpiled_circuit = transpile(qc, aer_simulator)

    order = 2
    while pow(number, order, modulus) != 1:
        result = list(aer_simulator.run(transpiled_circuit, shots=1).result().get_counts())[0]
            
        order = get_denominator(result, modulus, algo_name)
    
    return order