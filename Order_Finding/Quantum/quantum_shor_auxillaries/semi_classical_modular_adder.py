from qiskit import QuantumCircuit
from quantum_shor_auxillaries.QFT import QFT_gate, IQFT_gate
from quantum_shor_auxillaries.semi_classical_adder import Iphiadd_gate, cphiadd_gate, cIphiadd_gate

def phiaddmod(summand: int, modulus: int, nqbits: int):
    """
    If summand is an n-bit integer, choose nqbits = n + 4.
    nqbits > 3
    """

    if nqbits <= 3:
        return ValueError('Not enough qubits. nqbits must be at least 4')

    # Precomputing lists of qubits
    number_of_integer_qubits = nqbits - 3
    integer_qubits = list(range(2, nqbits - 1))
    ccqubits = [0, 1]
    ccqubits.extend(integer_qubits)

    cqubits = [nqbits - 1]
    cqubits.extend(integer_qubits)

    # Creating the computation
    qc = QuantumCircuit(nqbits)

    qc.append(cphiadd_gate(summand, number_of_integer_qubits, 2), ccqubits)


    qc.append(Iphiadd_gate(modulus, number_of_integer_qubits), integer_qubits)

    qc.append(IQFT_gate(number_of_integer_qubits), integer_qubits)

    qc.cx(2, nqbits - 1)

    qc.append(QFT_gate(number_of_integer_qubits), integer_qubits)

    qc.append(cphiadd_gate(modulus, number_of_integer_qubits, 1), cqubits)

    qc.append(cIphiadd_gate(summand, number_of_integer_qubits, 2), ccqubits)

    qc.append(IQFT_gate(number_of_integer_qubits), integer_qubits)

    qc.x(2)

    qc.cx(2, nqbits - 1)

    qc.x(2)

    qc.append(QFT_gate(number_of_integer_qubits), integer_qubits)

    qc.append(cphiadd_gate(summand, number_of_integer_qubits, 2), ccqubits)

    return qc

def phiaddmod_gate(summand, modulus, nqbits):

    phiaddmod(summand, modulus, nqbits).to_gate(label=f'phiaddmod({summand}, {modulus})')