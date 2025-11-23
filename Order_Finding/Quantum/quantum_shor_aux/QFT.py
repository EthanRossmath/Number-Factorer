from qiskit import QuantumCircuit
import numpy as np

def QFT(nqbits):
    """
    Computes the Quantum Fourier Transform on nqbits number of 
    qubits making use of using Draper's decomposition from (2002)
    """

    angle = np.pi

    rotation_angles = []
    
    for j in range(nqbits - 1):
        angle /= 2
        rotation_angles.append(angle)

    qc = QuantumCircuit(nqbits)

    j = 0

    while j < nqbits - 1:
        qc.h(j)

        for i in range(nqbits - j - 1):
            qc.cp(rotation_angles[i], i + j + 1, j)
        j += 1
    
    qc.h(nqbits -1)

    return qc

def QFT_gate(nqbits):
    """
    QFT on nqbits turned into a gate.
    """

    return QFT(nqbits).to_gate(label=f'QFT({nqbits})')

def IQFT_gate(nqbits):
    """
    Inverse QFT on nqbits turned into a gate.
    """
    return QFT(nqbits).inverse().to_gate(label=f'IQFT({nqbits})')
