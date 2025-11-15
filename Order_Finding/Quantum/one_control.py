from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit_aer import AerSimulator

from quantum_shor_auxillaries.mod_multiply import shorU_gate
from quantum_shor_auxillaries.continued_fractions import get_denominator

def beauregard_circuit(multiplier, modulus, nbits):

    all_qubits = [i for i in range(2 * nbits + 2)]

    qc = QuantumCircuit(2 * nbits + 2, 2 * nbits)

    # initialize qubits
    qc.x(nbits)

    # initial round of quantum processing

    qc.h(0)
    qc.append(shorU_gate(pow(multiplier, 2 ** (2 * nbits - 1), modulus), modulus, nbits), all_qubits)
    qc.h(0)


    # first measurement
    qc.measure(0, 0)

    for i in range(1, 2 * nbits):
        
        # apply hadamard, shorU, and cumulative phase
        with qc.if_test((i - 1, 1)):
            qc.x(0)
        

        qc.h(0)
        qc.append(shorU_gate(pow(multiplier, 2 ** (2 * nbits - 1 - i), modulus), modulus, nbits), all_qubits)

        # do sequence of conditional phases
        for j in range(i):
            with qc.if_test((j, 1)):
                qc.p(-np.pi / (2 ** (i - j)), 0)

        qc.h(0)
        # measure result
        qc.measure(0, i)

    return qc

def quantum_order_finder_one_control(number, modulus):

    if np.gcd(number, modulus) != 1:
        print(f'{number} is not invertible modulo {modulus}')
        return 0

    nbits = modulus.bit_length() + 1

    qc = beauregard_circuit(number, modulus, nbits)

    # simulate runs number of times, taking the result each time.
    aer_simulator = AerSimulator()
    transpiled_circuit = transpile(qc, aer_simulator)

    order = 2
    while pow(number, order, modulus) != 1:
        result = list(aer_simulator.run(transpiled_circuit, shots=1).result().get_counts())[0]


            
        denom = get_denominator(result, modulus)

        guess = int(np.lcm(denom, guess))
        num_runs += 1
    
    return guess

