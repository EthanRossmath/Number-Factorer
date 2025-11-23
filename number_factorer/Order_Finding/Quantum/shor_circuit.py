from qiskit import QuantumCircuit
from number_factorer.Order_Finding.Quantum.quantum_aux.mod_multiply import shorU_gate
from number_factorer.Order_Finding.Quantum.quantum_aux.QFT import IQFT_gate

def shor_circuit(multiplier, modulus, nbits):

    active_qubits = list(range(2 * nbits, 4 * nbits + 1))

    qc = QuantumCircuit(4 * nbits + 1, 2 * nbits)

    # initialize qubits
    qc.x(3 * nbits - 1)

    for i in range(2 * nbits):
        qc.h(i)
    
    # apply sequence of modular multiplication operators

    for i in range(2 * nbits):

        qc.append(shorU_gate(pow(multiplier, 2 ** i, modulus), modulus, nbits), [2 * nbits - i - 1] + active_qubits)
    
    # apply inverse QFT to first register

    qc.append(IQFT_gate(2 * nbits), list(range(2 * nbits)))

    # apply sequence of measurements

    for i in range(2 * nbits):
        qc.measure(i, i)

    return qc



