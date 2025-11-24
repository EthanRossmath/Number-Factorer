# NUMBER-FACTORER

#### Table of Contents

1. [Introduction](#1-introduction)
2. [How to use this repository](#2-how-to-use-this-repository)
3. [Description of algorithms](#3-description-of-algorithms)
4. [Sources](#4-sources)

## 1. Introduction

This is a Python library implemented by Ethan Ross for factoring integers using using variants of the number factoring algorithm presented by Shor in his seminal 1997 paper *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer.* The essential idea is that factoring an integer N will involve two algorithms
1. An order finding algorithm $\mathrm{Ord}$ that takes as input two integers $N,a\in \mathbb{Z}$ such that

    a) $N\geq 3$

    b) $2\leq a\leq N-1$ and $\mathrm{gcd}(a,N)=1$

    and outputs the multiplicative power $|a|\in \mathbb{Z}_{>0}$ of $a$. That is, the smallest positive integer $n$ satisfying $$a^n\equiv 1\text{ mod }N.$$

2. A classical processing algorithm $\mathrm{Factor}$ which takes as input a positive integer $N\geq 3$ an order finding algorithm $\mathrm{Ord}$ and produces the full prime factorization $N=p_1^{k_1}\cdots p_n ^{k_n}$ of $N$.

Provided that an order finding algorithm $\mathrm{Ord}$ has been provided, the classical processing algorithm $\mathrm{Factor}$ can be implemented extremely quickly. The original algorithm $\mathrm{Factor}$ provided by Shor goes as follows for an integer $N$ which is neither even nor a power of a prime.

1. Randomly choose an integer $2\leq a\leq N-1$ with $\mathrm{gcd}(a, N)=1$.
2. Compute $r=\mathrm{Ord}(a, N)$
3. If $r$ is odd, return to Step 1. Otherwise $0=(a^{r/2}-1)(a^{r/2}+1)\text{ mod }N$,
which implies $a^{r/2}-1\text{ mod }N$ divides $N$. Let $d=\mathrm{gcd}(a^{r/2}-1,N)$
4. Return $d$ and $N/d$

There are two features worth noting about the above algorithm. First, it is not a full factorization algorithm, but rather a crucial inductive step in a full factorization. See [shor_factorizer.py](/number_factorer/Classical_Factoring/shor_factorizer.py) for a full implementation. Checking if an integer is even, a power of a prime, and the other processing (like computing modular powers and greatest common divisors) can be implemented in polynomial time on a classical computer. Thus, this leads us to the second thing of note in this algorithm: the usage of an order finding algorithm $\mathrm{Ord}$ in step 2. As far as classical computing goes, the best order finding algorithms (e.g. prime sieves) run in subexponential time and seemingly cannot be improved to polynomial time (provided $P\neq NP$). Thus, factorization is inherently inefficient on a classical computer.

Of course, the point of this repository is that Shor showed order finding can be done efficiently, *provided you have access to a sufficiently large quantum computer.* In particular, order finding can be implemented in $\mathcal{O}(n^3)$ time on a quantum computer where $n$ is the bit length of the integer $N$ we are factoring. This is a remarkable speed up and shows the promise of quantum computers (to destroy our public key cryptography, for instance).


In the future, I would like to implement some version of Shor's algorithm on actual hardware, but that would require implementing Quantum Error Correction (QEC) in some capacity and would require an in depth study of the actual hardware used by, say, IBM.

As of November 2025, these are the following options available.

### Order Finding
#### Classical

[bad_order_finder.py](/number_factorer/Order_Finding/Classical/bad_order_finder.py)

Incrementally computes order of $a$ modulo $N$ in $\mathcal{O}(n^2 2^n)$ computations, where $n$ is the bit length of $N$.

[babygiantsteps.py](/number_factorer/Order_Finding/Classical/babygiantsteps.py)

Shanks' 1969 order finding algorithm. Computes the order of $a$ modulo $N$ with $\mathcal{O}(n2^{n/2})$ computations.

#### Quantum
[shor_circuit.py](/number_factorer/Order_Finding/Quantum/shor_circuit.py)

A simulation of the original order finding quantum circuit as presented by Shor in 1997. Implemented using Qiskit and the AerSimulator package. Computes the order of $a$ modulo $N$ using $4n+2$ qubits and $\mathcal{O}(n^3)$ simulated quantum operations.

[beauregard.py](/number_factorer/Order_Finding/Quantum/beauregard_circuit.py)

A simulation of Beauregard's 2003 variant of Shor's circuit that uses only one control qubit. Implemented using Qiskit and the AerSimulator package. Computes the order of $a$ modulo $N$ using $4n+2$ qubits and $\mathcal{O}(n^3)$ simulated quantum operations.


### Classical Factoring
[shor_factorizer.py](/number_factorer/Classical_Factoring/shor_factorizer.py)

A full implementation of Shor's original 1997 classical factoring algorithm. Produces the full prime factorization of $N$ in $\mathcal{O}(n^3)$ computations modulo the order finding algorithm.


[ekera_factorizer.py](/number_factorer/Classical_Factoring/ekera_factorizer.py)

Ekera's 2021 variant of Shor's classical processing that only calls on the order finding algorithm once. Also computes the full prime factorization in $\mathcal{O}(n^3)$ operations modulo the order finding algorithm.


## 2. How to Use This Repository

### Downloading the library
In the root directory, run the following in your terminal
```
pip install -e .

```
After that, number_factorer should be downloaded to your machine. 

### Using the library

In a python file, run
```
from number_factorer import (
    Number_Factorer,
    IncrementOrder,
    BabyGiantOrder,
    ShorFactorization,
    EkeraFactorization,
    ShorOrder,
    BeauregardOrder
)
```
To get all options. To factor a number, say 91, you need to do the following:
1. choose an order finding algorithm: IncrementOrder, BabyGiantOrder, ShorOrder, or BeauregardOrder
2. choose a classical processing algorithm: ShorFactorization or EkeraFactorization
3. Instantiate a full factorization algorithm by running
```
nf = Number_Factorer(Factor(), Order())
```
for example,
```
nf = Number_Factorer(ShorFactorization(), BabyGiantOrder())
```
4. Factor your number using the .factor() method
```
nf.factor(91)
```
will return 
```
[(7, 1), (13, 1)]
```
indicating (correctly) that $91=7\times 13$.



## 3. Description of algorithms.

### Order Finding
#### Classical

[bad_order_finder.py](/number_factorer/Order_Finding/Classical/bad_order_finder.py)

 The most inefficient algorithm possible. Given a positive integers $N\geq 3$ and $2\leq a\leq N-1$ with $\mathrm{gcd}(a,N)=1$, this algorithm compute the multiplicative order of $a$ modulo $N$ as follows.
1. Compute $x=a^2\text{ mod }N$ and set $i=2$.
2. If $x=1$, return $i$. Otherwise, increment $i=i+1$.
3. Compute $x=x\cdot a\text{ mod }N$. Return to Step 2.

Computes the order in $\mathcal{O}(n^2 2^n)$ computations where $n$ is the bit length of $N$.

Naive improvements like randomly sampling exponents and using fast modular exponentation are not quite the improvement because if a random exponent $i$ with $2\leq i\leq N-1$ satisfies $a^i=1\text{ mod }N$, then this only guarantees $i$ is a multiple of the order and thus much more processing is required.


[babygiantsteps.py](/number_factorer/Order_Finding/Classical/babygiantsteps.py)

Shanks' 1969 order finding algorithm. A significant improvement over the previous algorithm. Given a positive integers $N\geq 3$ and $2\leq a\leq N-1$ with $\mathrm{gcd}(a,N)=1$, this algorithm computes the multiplicative order of $a$ modulo $N$ as follows.
1. Set $b=\lceil \sqrt{N-1}\rceil$.
2. (Baby Steps) Compute list $\{a,\dots,a^b\}$, all modulo $N$. If $a^i=1\text{ mod }N$ for some $1\leq i\leq b$, return the minimal such $i$.
3. (Giant Steps) Compute $a^{ib}\text{ mod }N$, starting at $i=2$. Continue to increment until there exists $1\leq j\leq b$ so that $a^{ib}=a^j$. Return $ib-j$.

Computes the order in $\mathcal{O}(n^2 2^{n/2})$ operations where $n$ is the bit length of $N$.

#### Quantum
[shor_circuit.py](/number_factorer/Order_Finding/Quantum/shor_circuit.py)

A simulation of the original order finding quantum circuit as presented by Shor in 1997. Implemented using Qiskit and the AerSimulator package.

PICTURE

Given positive integers $N\geq 3$ and $2\leq a\leq N-1$, computes the order of $a$ modulo $N$ using $4n+4$ qubits and $\mathcal{O}(n^3)$ quantum computations, where $n$ is the bit length of $N$. 



[beauregard.py](/number_factorer/Order_Finding/Quantum/beauregard_circuit.py)

A simulation of Beauregard's 2003 variant of Shor's circuit that uses only one control qubit. Implemented using Qiskit and the AerSimulator package.

PICTURE

Given positive integers $N\geq 3$ and $2\leq a\leq N-2$, computes the order of $a$ modulo $N$ using $2n+3$ qubits and $\mathcal{O}(n^3)$ quantum operations.

### Classical Factoring
[shor_factorizer.py](/number_factorer/Classical_Factoring/shor_factorizer.py)

A full implementation of Shor's original 1997 classical factoring algorithm. Given a positive integer $N\geq 3$ and an order finding algorithm $\mathrm{Ord}$, produces the full prime factorization $N=p_1^{n_1}\cdots p_k^{n_k}$, where $p_1,\dots,p_k$ are all distinct primes and $k_1,\dots,k_n\geq 1$ are the multiplicites. 

1. Initialize two empty lists $\mathrm{factors}=\{\}$ and $\mathrm{primes}=\{\}$. 
2. If $N$ is even, factor $N=2^k m$ where $\mathrm{gcd}(2,m)=1$. Update $\mathrm{factors}=\{(m, 1)\}$ and $\mathrm{primes}=\{(2,1)\}$. Otherwise, update $\mathrm{factors}=\{(N, 1)\}$
3. While $|\mathrm{factors}|>0$, do the following. 

    3.1. Let $(A, k)\in \mathrm{factors}$.

    3.2. Classically check if $A$ is prime (using say Miller-Rabin). If so, remove $(A,k)$ from $\mathrm{factors}$, add it to $\mathrm{primes}$, and return to 3.1. If not, continue.

    3.3. Classically check if $A=r^\ell$ for some $r\geq 2$ and $\ell\geq 2$ (using say Bernstein's 1998 algorithm). If so, update $(A,k)$ to $(r, \ell k)$ and return to 3.1. If not, continue.

    3.4. Run the following algorithm.

    3.4.1. Randomly choose $2\leq a\leq A-1$  with $\mathrm{gcd}(a,A)=1$.

    3.4.2. Use the ordering finding algorithm $\mathrm{Ord}$ to compute the order $r=|a|$ of $a$ modulo $A$. If $r$ is odd, return to 3.4.1.

    3.4.3. Compute $d=\mathrm{gcd}(a^{r/2}+1,A)$. 

    3.4.4. Remove $(A,k)$ from $\mathrm{factors}$ and replace it with $(d,k)$ and $(A/d,k)$. 

    3.5. Consolidate any repeated factors in $\mathrm{factors}$. Return to 3.1.

4. Return $\mathrm{primes}$

This algorithm wittles down the factors of $N$ until they are prime then adds them to the list of prime factors. Modulo the order finding algorithm, this will compute the full factorization in $\mathcal{O}(n^3)$ where $n$ is the bit length of $N$.

[ekera_factorizer.py](/number_factorer/Classical_Factoring/ekera_factorizer.py)

Ekera's 2021 variant of Shor's classical processing that only calls on the order finding algorithm once. Given an integer $N\geq 3$ and an order finding algorithm $\mathrm{Ord}$, and constant integers $c\geq 1$, $R\geq 1$, compute the prime factorization $N=p_1^{n_1}\cdots p_k^{n_k}$ as follows.

1. Initialize a list of factors $\mathrm{factor}=\{(N,1)\}$.
2. Randomly choose integer $2\leq a\leq N-2$ with $\mathrm{gcd}(a,N)=1$.
3. Compute $r=\mathrm{Ord}(a,N)$
4. Let $m=cn$, where $n$ is the bit length of $N$.
5. Compute a list $P$ of primes $p$ with bit length less than $m$ (using say Miller-Rabin).
6. Let $q = r\prod_{p \in P}p^{\eta_p}$, where $\eta_p\geq 0$ is the largest integer so that $p^{\eta_p}<m$
7. Write $r=2^ks$, where $s$ is odd. 
8. Run the following algorithm $R$ times.

    8.1. Randomly choose $2\leq x\leq N-2$ with $\mathrm{gcd}(x,N)=1$.

    8.2. Compute $y=x^s\text{ mod }N$ and set $i=0$. If $y=1$, return to 8.1. 

    8.3. Compute $d=\mathrm{gcd}(y-1,N)$. If $d>1$, add $(d,1)$ to the list $\mathrm{factors}$. Reduce the list so that all factors are co-prime. Otherwise, continue.

    8.4. Set $y=y^2\text{ mod }N$ and increment $i=i+1$. 

    8.5. If $i=k$, halt. Otherwise, return to $8.3$. 

9. Return $\mathrm{factors}$.

## 4. Sources

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

    




