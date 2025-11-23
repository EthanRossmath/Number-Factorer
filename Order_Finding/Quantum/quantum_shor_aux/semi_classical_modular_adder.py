from qiskit import QuantumCircuit
from .QFT import QFT_gate, IQFT_gate
from .semi_classical_adder import Iphiadd_gate, cphiadd_gate, cIphiadd_gate

def phiaddmod(summand: int, modulus: int, nqbits: int):
    """
    Implements Beauregard's modular adder (2003). 

    Input: qubit |a>, 0 <= a <= 2 ** (nqbits - 3) - 1
    Output: qubit |(a + summand) % modulus >
    
    If summand is an n-bit integer, choose nqbits = n + 4.
    nqbits > 3
    """

    if nqbits <= 3:
        return ValueError('Not enough qubits. nqbits must be at least 4')

    # Precomputing lists of qubits

    number_of_integer_qubits = nqbits - 3

    # all the qubits used to store the integers
    integer_qubits = list(range(2, nqbits - 1))

    # two control qubits for addition
    ccqubits = [0, 1]
    ccqubits.extend(integer_qubits)

    # overflow control qubit (used for checking if modulus - (a + b) < 0)
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

    return phiaddmod(summand, modulus, nqbits).to_gate(label=f'phiaddmod({summand}, {modulus})')