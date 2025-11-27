In putting this library together, a variety of technical sources were consulted. Here are the main ones.

### Quantum Order Finding

1. Shor. *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer.* SIAM Journal on Computing. vol 26, pp 1484-1509, 1997.

The paper where Shor first proposed his polynomial time Quantum factoring algorithm.

2. Draper. *Addition on a Quantum Computer* 	arXiv:quant-ph/0008033, 2000.

An efficient implementation of addition on a quantum circuit that uses the Quantum Fourier transform.

3. Parker and Plenio. *Efficient Factorization with a Single Pure Qubit and $\mathrm{log}\mathit{N}$ Mixed Qubits.* Physical Review Letters. vol 85, pp 3049-3052, 2000.

An variant of Shor's algorithm that uses a single control qubit.

3. Beauregard. *Circuit for Shor’s algorithm using 2n+3 qubits.* Quantum Info. Comput. vol 3, pp 175-185, 2003.

A single control qubit variant of Shor's algorithm (vis-a-vis Parker-Plenio) that uses Draper's QFT-based adder to create the reversible modular multiplication operator key to Shor's algorithm.

5. Sachs, *Ten Little Algorithms, Part 7: Continued Fraction Approximation.* 2023. https://www.embeddedrelated.com/showarticle/1620.php

My main source for implementing the continued fractions algorithm which is essential for finding the order of an element from the output of Shor's quantum circuit.

### Classical Order Finding

1. Sutherland. *Order Computations in Generic Groups.* Dissertation, MIT. 2007.

Main source for Shank's Baby-Steps, Giant-Steps algorithm.

### Classical Processing

1. Shor. *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer.* SIAM Journal on Computing. vol 26, pp 1484-1509, 1997.

Shor gives the key inductive procedure for translating order finding to finding two non-trivial factors.

2. Ekerå. *On completely factoring any integer efficiently in a single run of an order-finding algorithm.* Quantum Information Processing. vol 20, pp 205, 2021.

A variant of the classical processing proposed by Shor that only calls upon the quantum algorithm once.

3. Bach, Driscoll, and Shallit. *Factor Refinement.* Journal of Algorithms. vol 15, pp 199-222, 1993.

The main way to translate Shor's "splitting algorithm" into a full prime factorization.

4. Bernstein. *Detecting Perfect Powers in Essentially Linear Time.* Mathematics of Computation, vol 67, pp 1253-1283, 1998.

The most efficient way to compute if a number is a perfect power. In this implementation, I use the gmpy2 library, but in the future I want to create a C++ implementation of Bernstein's algorithms.

### Quantum Circuit Typesetting

1. Kay. *Tutorial on the Quantikz Package.* arXiv:10809.03842v7, 2023.

I used the Quantikz latex package to make all the circuit diagrams in this README.