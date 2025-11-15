from qiskit import QuantumCircuit
import numpy as np

def phiadd(summand: int, nqbits: int):
    """
    Uses Draper's addition circuit (2002).
    Input: Qubit string |b> where b is an nqbits integer
    Output: Qubit string |(b + summand)  % 2 ** nqbits>
    """

    # First create a binary representation of summand.
    bit_rep = []

    bit_string = format(summand, f'0{nqbits}b')

    for bit in bit_string:
        bit_rep.append(int(bit))

    # generate a list of angles
    angle_list = []
    angle = np.pi 

    for i in range(nqbits):
        angle_list.append(angle)

        angle /= 2
    
    # Creating gates 
    qc = QuantumCircuit(nqbits)

    # Using the bit representation of summand to generate a collection
    # of 1 qubit gates
    for i in range(nqbits):
        angle_i = 0
        for j in range(nqbits - i):
            if bit_rep[j + i] == 1:
                angle_i += angle_list[j]
        qc.p(angle_i, i)
    
    return qc


def phiadd_gate(summand: int, nqbits: int):

    return phiadd(summand, nqbits).to_gate(label=f'phiadd({summand})')

def Iphiadd_gate(summand: int, nqbits: int):

    return phiadd(summand, nqbits).inverse().to_gate(label=f'Iphiadd({summand})')

def cphiadd_gate(summand: int, nqbits: int):

    return phiadd(summand, nqbits).control(1).to_gate(label=f'phiadd({summand})')

def cIphiadd_gate(summand: int, nqbits: int):

    return phiadd(summand, nqbits).control(1).inverse().to_gate(label=f'Iphiadd({summand})')