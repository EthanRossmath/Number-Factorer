from qiskit import QuantumCircuit
import numpy as np

from .quantum_aux.mod_multiply import shorU_gate

def beauregard_circuit(multiplier, modulus, nbits):

    all_qubits = list(range(2 * nbits + 2))

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

