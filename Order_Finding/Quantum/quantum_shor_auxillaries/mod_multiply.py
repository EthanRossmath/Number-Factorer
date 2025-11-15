from qiskit import QuantumCircuit
from quantum_shor_auxillaries.QFT import QFT_gate, IQFT_gate
from quantum_shor_auxillaries.semi_classical_modular_adder import phiaddmod_gate

def cmult(multiplier, modulus, nbits):

    qc = QuantumCircuit(2 * nbits + 2)

    last_qubits = [i for i in range(nbits + 1, 2 * nbits + 1)]
    lastest_qubits = last_qubits + [2 * nbits + 1]

    # apply QFT

    qc.append(QFT_gate(nbits), last_qubits)

    # apply sequence of modular additions

    add_on = multiplier % modulus

    for i in range(nbits):

        power2_gate = phiaddmod_gate(
            summand= add_on, 
            modulus=modulus,
            nqbits=nbits + 3
        )
        qc.append(power2_gate, [0, nbits - i] + lastest_qubits)
        add_on = (2 * add_on) % modulus
    
    # one last qft

    qc.append(IQFT_gate(nbits), last_qubits)

    return qc

def cmult_gate(multiplier, modulus, nbits):

    return cmult(multiplier, modulus, nbits).to_gate(label=f'CMULT({multiplier}, {modulus})')

def Icmult_gate(multiplier, modulus, nbits):

    return cmult(multiplier, modulus, nbits).inverse().to_gate(label=f'ICMULT({multiplier}, {modulus})')


def shorU(multiplier, modulus, nbits):

    # Classical pre-processing.

    inv = pow(multiplier, -1, modulus)

    all_qubits = [i for i in range(2 * nbits + 2)]

    # Creating circuit

    qc = QuantumCircuit(2 * nbits + 2)

    # Apply multiplication

    qc.append(cmult_gate(multiplier, modulus, nbits), all_qubits)

    # Apply CSWAP

    for i in range(nbits):
        qc.cx(nbits + i + 1, i + 1)
        qc.ccx(0, i + 1, nbits + i + 1)
        qc.cx(nbits + i + 1, i + 1)
    
    # Apply inverse of multiplication by modular inverse

    qc.append(cmult_gate(inv, modulus, nbits).inverse(), all_qubits)

    return qc

def shorU_gate(multiplier, modulus, nbits):

    return shorU(multiplier, modulus, nbits).to_gate(label=f'U({multiplier}, {modulus})')