# NUMBER-FACTORER

## INTRODUCTION

This is a Python library implemented by Ethan Ross for factoring integers using using variants of the number factoring algorithm presented by Shor in his paper [CITE] in [YEAR]. The essential idea is that factoring an integer N will involve two algorithms
1. An order finding algorithm $\mathrm{Ord}$ that takes as input two integers $N,a\in \mathbb{Z}$ such that

        a) $N\geq 3$

        b) $2\leq a\leq N-1$ and $\mathrm{gcd}(a,N)=1$

    and outputs the multiplicative power $|a|\in \mathbb{Z}_{>0}$ of $a$. That is, the smallest positive integer $n$ satisfying $$a^n\equiv 1\text{ mod }N.$$

2. A classical processing algorithm $\mathrm{Factor}$ which takes as input a positive integer $N\geq 3$ an order finding algorithm $\mathrm{Ord}$ and produces the full prime factorization $N=p_1^{k_1}\cdots p_n ^{k_n}$ of $N$.

The key here is that the first algorithm $\mathrm{Ord}$ if implemented classically can be at best subexponential in complexity, whereas Shor in 1997 showed that a Quantum Computer can compute the order in polynomial time. So this project is broken up into two main folders: Order_Finding and Classical_Factoring. The first folder, Order_Finding, implements various order finding algorithms, both classical and (simulated) quantum. The second contains all the current classical factoring algorithms implemented that make use of order finding as a blackbox. 

In the future, I would like to implement some version of Shor's algorithm on actual hardware, but that would require implementing Quantum Error Correction (QEC) in some capacity and would require an in depth study of the actual hardware used by, say, IBM.

## SOURCES

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


## OVERVIEW OF CONTENTS

This project consists of two folders, Order_Finding and Classical_Factoring. An in depth description will be given in the next section. Here, I will briefly describe each folder and its contents. Both are completely independent of one another to keep in the spirit of this project.

```
NUMBER-FACTORER
├── Classical_Factoring
│   ├── classical_shor_auxillaries
│   │   ├── is_power.py
│   │   ├── power_of_two.py
│   │   ├── refine.py
│   │   └── splitter.py
│   ├── one_shot_auxillaries
│   │   ├── adding_factors.py
│   │   ├── is_complete_factor.py
│   │   ├── largest_exponent.py
│   │   ├── power_refine.py
│   │   ├── prime_below_cutoff.py
│   │   └── random_invertible.py
│   ├── oneshot_full_factorizer.py
│   └── shor_full_factorizer.py
├── Order_Finding
│   ├── Classical
│   │   ├── babygiantsteps.py
│   │   ├── bad_order_finder.py
│   │   └── random_order_finder.py
│   └── Quantum
│       ├── one_control.py
│       └── quantum_shor_auxillaries
│           ├── continued_fractions.py
│           ├── mod_multiply.py
│           ├── QFT.py
│           ├── semi_classical_adder.py
│           └── semi_classical_modular_adder.py

```
Classical_Factoring contains all algorithms and helper functions which implement a $\mathrm{Factor}$ algorithm that completely factors an integer using an order finding method as a primitive.  Order_Finding contains all classical and (simulated) quantum algorithms that implement an order finding method. 

## DESCRIPTION OF EACH FOLDER

### 1. Order_Finding
This implements various Classical and Quantum order finding methods organized into the Classical and Quantum subfolders.

#### 1.1 Classical

This contains all the current implementations of classical order finding methods which compute the multiplicative order of an integer $a\in \mathbb{Z}$ modulo $N$ for some $N\geq 3$ provided $\mathrm{gcd}(a,N)=1$.

    bad_order_finder.py

This is the most inefficient algorithm one could implement. It goes as follows.
        
(A) Set $i=2$ and $x = a^2 \text{ mod }N$
         
(B) Check if $x=1$. If so, let $\mathrm{Ord}(a,N)=i$. 
          
(C) If not, set $x = x\cdot a \text{ mod }N$ and increment $i$ by $1$. Return to step (B)

This almost guaranteed to take an exponential number of calculuations and hence is extremely inefficient for large $N$.

    babygiantsteps.py


This is a version of the Baby Steps, Giant Steps ordering finding algorithm due to Shanks in 1967.  This algorithm has two parts. 

1. Baby Steps.

Set $b = \lceil \sqrt{N-1} \rceil$ and compute $\{a, a^2, \dots, a^b \}$ all modulo $N$. If $a^i \equiv 1\text{ mod }N$ at any step along the way, set $\mathrm{Ord}(a, N)=i$ (this so far looks like the previous algorithm).

2. Giant Steps.

Compute the list $\{a^{2b}, a^{3b}, a^{4b}, \cdots\}$. If for any $i$ it ever occurs that $a^{ib}\equiv a^j\text{ mod }N$ for some $1\leq j\leq b$, then set $\mathrm{Ord}(a,N) = ib-j$.

#### 1.2 Quantum

Contains all simulated Quantum circuits in qiskit that implement some version of Shor's original order finding algorithm.

    original_shor.py



Description

    one_control

[SCREEN SHOT]

Description

##### 1.2.1 quantum_shor_auxillaries

Here I will briefly describe each of the helper functions and routines found in this folder.

    QFT.py

[SCREEN SHOT]

Description

    semi_classical_adder.py

[SCREEN SHOT]

Description


    semi_classical_modular_adder.py

[SCREEN SHOT]

Description


    mod_multiply.py

[SCREEN SHOT]

Description


    continued_fractions.py

[SCREEN SHOT]

Description

### 2. Classical_Factoring

This directory contains all algorithms $\mathrm{Factor}$ which take as input an integer $N\geq 3$ and an order finding algorithm $\mathrm{Ord}$ and outputs the full  prime factorization of $N$. All algorithms make use of the ```gmpy``` Python library for highly optimized computing. In the future, I would like to hop in the C++ coding and implement this myself.

    shor_full_factorizer

[SCREEN SHOT]

Descrption

    one_shot_factorizer

[SCREEN SHOT]

Descrption

#### 2.1 classical_shor_auxillaries

    is_power.py

[SCREEN SHOT]

Descrption

    power_of_two.py

[SCREEN SHOT]

Descrption

    refine.py

[SCREEN SHOT]

Descrption

    splitter.py

[SCREEN SHOT]

Descrption

#### 2.2 one_shot_auxillaries

    adding_factors.py

[SCREEN SHOT]

Descrption

    is_complete_factor.py

[SCREEN SHOT]

Descrption

    largest_exponent.py

[SCREEN SHOT]

Descrption

    power_refine.py

[SCREEN SHOT]

Descrption

    prime_below_cutoff.py

[SCREEN SHOT]

Descrption

    random_invertible.py

[SCREEN SHOT]

Descrption




    




