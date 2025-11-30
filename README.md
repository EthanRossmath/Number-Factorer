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

## Further Documentation

- See [USER_GUIDE.md](/docs/USER_GUIDE.md) for tutorials on using number factorer and its various functionalities.

- See [TECHNICAL.md](/docs/TECHNICAL.md) for technical discussions on each of the algorithms and their implementations.

- See [REFERENCES.md](/docs/REFERENCES.md) for references to the technical literature relied upon for this library.

    




