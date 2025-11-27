# Number-Factorer

## Overview
Number-Factorer is a Python library implemented by Ethan Ross for factoring integers using using variants of the number factoring algorithm presented by Shor in his seminal 1997 paper *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer.* It has implemented various quantum and classical order finding algorithms, together with two classical processing algorithms to provide full prime factorizations of arbitrary integers.

- **Classical Order Finding:** Baby-step Giant-step (Shanks 1969), Incremental order finding. 
- **Quantum Order Finding:** Shor 1997, Beauregard 2003
- **Classical Processing:** Show 1997, Ekera 2021

## Installation
In the root directory, run the following in your terminal
```bash
pip install -e .
```
After that, number_factorer should be downloaded to your machine.

## Example Usage
```python
from number_factorer import Number_Factorer, BabyGiantOrder, ShorFactorization

nf = Number_Factorer(ShorFactorization(), BabyGiantOrder())
nf.factor(92) # Returns [(7, 1), (13, 1)]
```

## Algorithms

See [TECHNICAL.md](TECHNICAL.md) for in-depth discussions of each of the algorithms listed below.

### Classical Order Finding
- **IncrementOrder**: $\mathcal{O}(n^2\cdot 2^n)$
- **BabyGiantOrder**: $\mathcal{O}(n\cdot 2^{n/2})$

### (Simulated) Quantum Order Finding
- **ShorOrder**: $4n+1$ qubits, $\mathcal{O}(n^3)$ quantum computations
- **BeauregardOrder**: $2n+2$ qubits, $\mathcal{O}(n^3)$ quantum computations

### Classical Factoring
- **ShorFactorization**: Full prime factorization using order finding, repeatedly splits subfactors until full prime factorization is obtained.
- **EkeraFactorization**: Single order-finding call variant.

## References

See [REFERENCES.md](REFERENCES.md) for citations to the technical sources for this project.
    




