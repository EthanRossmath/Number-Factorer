# TECHNICAL

This document contains technical descriptions of all the algorithms contained in this repository.

- [Main Idea](#main-idea)
- [Order Finding](#order-finding)
    - [Classical](#classical)
    - [Quantum](#quantum)
- [Classical Factoring](#classical-factoring)

## Main Idea

The essential idea is that factoring an integer N will involve two algorithms
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

## Order Finding
### Classical

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

### Quantum
[shor_circuit.py](/number_factorer/Order_Finding/Quantum/shor_circuit.py)

A simulation of the original order finding quantum circuit as presented by Shor in 1997. Implemented using Qiskit and the AerSimulator package. Given positive integers $N\geq 3$ and $2\leq a\leq N-1$, computes the order of $a$ modulo $N$ using $4n+4$ qubits and $\mathcal{O}(n^3)$ quantum computations, where $n$ is the bit length of $N$. 

The full circuit is below.

![The full circuit for Shor's algorithm](/images/shor.png)

Two gates need to be implemented to carry out the circuit above, namely the Quantum Fourier Transform $\mathrm{QFT}$ and the modular multiplication gate $U(a)$. The Quantum Fourier Transform, which can be found in [QFT.py](/number_factorer/Order_Finding/Quantum/quantum_aux/QFT.py), is the version given by Draper (2001) with the following circuit.

![Draper's version of the QFT](/images/QFT.png)

The gates $P(\pi/2^{i})$ are controlled phase gates, where for any angle $\theta$
$$
P(\theta)=
\begin{pmatrix}
1 & 0\\
0 & e^{i\theta}
\end{pmatrix}
$$

Given a collection of $n$ qubits $|x\rangle =|x_0\cdots x_{n-1}\rangle$, the Quantum Fourier Transform is defined by
$$
QFT(|x\rangle)=\frac{1}{2^{n/2}}\sum_{j=0}^{2^n-1}e^{2\pi i xj}|j\rangle.
$$
The above circuit comes from the decomposition
$$
\sum_{j=0}^{2^n-1}e^{2\pi i xj}|j\rangle=\bigotimes_{k=0}^{n-1}(|0\rangle+e^{2\pi i kx2^{-k-1}}|1\rangle),
$$
where we're viewing $x=\displaystyle\sum_{k=0}^{n-1}x_k 2^k$.

 The controlled modular multiplication gate, which can be found in [mod_multiply.py](number_factorer/Order_Finding/Quantum/quantum_aux/mod_multiply.py), is the version given by Beauregard (2003)

 ![Beauregard's implementation of modular multiplication](/images/U.png)


This is a variant of Beauregard's 2003  implementation. In detail, this gate takes the following inputs

- a control qubit $|c\rangle$,
- a collection of qubits $|b\rangle=|b_0\cdots b_{n-1}\rangle$, where $\displaystyle b=\sum_{j=0}^{n-1}b_j2^j$,
- and $n+1$ workspace qubits $|0^{n+1}\rangle=|0\cdots 0\rangle$

and returns the control and workspace qubits $|c\rangle$ and $|0^{n+1}\rangle$ in the first and third registers untouched and in the second register returns $|a\cdot b\text{ mod }N\rangle$ if the control is $1$ and $|b\rangle$ otherwise. The implementation can be found in the folder [quantum_aux](/number_factorer/Order_Finding/Quantum/quantum_aux).

The general idea is for how this algorithm works is as follows. Let $N\geq 3$ and $2\leq a\leq N-1$ be coprime integers and let $n$ be the bit length of $N$. For any integer $0\leq x\leq 2^{n}-1$, write $\displaystyle x= \sum_{k=0}^{n-1}x_k 2^k$ for its bit representation and define
$$
|x\rangle:=|x_0\rangle\otimes\cdots \otimes |x_{n-1}\rangle=|x_0\cdots x_{n-1}\rangle
$$

Suppose we've implemented modular multiplication $U(b)$ for an arbitrary $0\leq b\leq N-1$, i.e.
$$
U(b)|x\rangle=|b\cdot x\text{ mod }N\rangle
$$

Recall that we are trying to compute the multiplicative order of $a$. Let us write $r=|a|$ for this order. It's easy to see that 
$$
|\psi_0\rangle=\frac{1}{\sqrt{r}}\sum_{k=0}^{r-1}|a^k\rangle
$$
satisfies $U(a)|\psi_a\rangle=|\psi_a\rangle$. Indeed, more generally,
$$
|\psi_j\rangle=\frac{1}{\sqrt{r}}\sum_{k=0}^{r-1}e^{2\pi ik/r}|a^k\rangle
$$
satisfies $U(a)|\psi_j\rangle=e^{2\pi i j/r}|\psi_j\rangle$. The circuit given by Shor (modulo the input bits) is the circuit for a family of quantum algorithms called "Phase Estimation" which in this case if we ran the following circuit

![Applying the phase estimation circuit to an eignvector of U(a)](/images/shoreigen.png)

Then the measured bits $c_0,\dots,c_{m-1}$ satisfy
$$
\sum_{k=0}^{m-1}c_k 2^{m-k}\approx \frac{j}{r}
$$
where we were trying to find $r$ all along! Of course that means we would need to be able to prepare one of these eigenvectors, which is infeasible. However, it turns out that
$$
|1\rangle=|10\cdots0\rangle=\frac{1}{\sqrt{r}}\sum_{j=0}^{r-1}|\psi_j\rangle
$$
This is why in the diagram for Shor's algorithm given above, I initialized the second register to be $|1\rangle\otimes |0^{n-1}\rangle$. The result of running this circuit is that we will uniformly at random obtain an approximation for some $\displaystyle\frac{j}{r}$ for some $0\leq j\leq r-1$. With good probability, $j$ will be co-prime with $r$ allowing us to easily find $r$.


[beauregard.py](/number_factorer/Order_Finding/Quantum/beauregard_circuit.py)

A simulation of Beauregard's 2003 variant of Shor's circuit that uses only one control qubit. Implemented using Qiskit and the AerSimulator package.

![Alt text](images/beauregard.png)

Given positive integers $N\geq 3$ and $2\leq a\leq N-2$, computes the order of $a$ modulo $N$ using $2n+3$ qubits and $\mathcal{O}(n^3)$ quantum operations. This works almost identically to Shor's original algorithm, except there is only one control qubit which is reset back to $0$ after every run of $U(a^{2^j})$. The inverse QFT is also applied by means of phase gates $P(\phi_j)$, where for each $j$,
$$
\phi_j=-2\pi \sum_{k=0}^{j-1} m_k 2^{k-j+2}.
$$


## Classical Factoring
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