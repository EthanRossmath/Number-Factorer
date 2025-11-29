# USER GUIDE

## 1. Basic Usage

### Factoring
The Number-Factorer library enables you to construct a prime factorization algorithm given two primitives: an order finding algorithm and a classical processing algorithm. 

The general outline for creating a number factoring algorithm is as follows:

1. Choose an order finding algorithm. The choices are
    - ShorOrder
    - BeauregardOrder
    - IncrementOrder
    - BabyGiantOrder

2. Choose a classical processing algorithm. The choices are
    - ShorFactorizer
    - EkeraFactorizer

3. Put them together using the Number_Factorizer orchestration function. 

The code below gives an example using ShorOrder and ShorFactorizer.

```python
from number_factorer import (
    Number_Factorer, # main orchestration function
    ShorOrder, # an order finding algorithm
    ShorFactorizer # a classical processing algorithm
)

# instantiate the algorithm
nf = Number_Factorer(factor_algo=ShorFactorizer(), order_algo=ShorOrder()) 

# factor an integer using the .factor() method
print(nf.factor(15)) # returns [(3, 1), (5, 1)]
```

Factoring will produce a list of tuples consisting of each distinct prime dividing the number in the first entry together with the multiplicity of the prime in the second factor. For instance, ```nf.factor(15)``` produces ```[(3, 1), (5, 1)]``` which corresponds to the fact that
$$
15 = 3^1 \cdot 5^1
$$

### Acessing the underlying Qiskit circuits

Two of the order finding algorithms are based on simulated quantum circuits via Qiskit. These are ShorOrder and BeauregardOrder. Each of these runs a variant of the phase estimation circuit for order finding. To gain access to the underlying quantum circuit, use the ```.get_circuit()``` method.

```python
from number_factorer import ShorOrder, BeauregardOrder

# two distinct circuits that compute the order of 3 modulo 7
qc1 = ShorOrder().get_circuit(invertible=3, modulus=7)
qc2 = BeauregardOrder().get_circuit(invertible=3, modulus=7)
```

In the above code, ```qc1``` and ```qc2``` are two Qiskit circuits that compute the multiplicative order of $3$ modulo $7$. Once you've obtained your Qiskit circuit, you can now apply Qiskit QuantumCircuit methods. Some useful ones for elementary analysis are the following

- ```.draw()``` method: creates a rendering of the quantum circuit in diagram form.
- ```.num_qubits``` aspect: computes the number of qubits used in the circuit.
- ```.depth()``` method: computes the number of quantum gates in the circuit.

```python
from number_factorer import ShorOrder

qc = ShorOrder().get_circuit(invertible=2, modulus=3)

qc.draw('mpl')
```

![Alt text](/images/smallshor.png)

```python
from number_factorer import BeauregardOrder

qc = BeauregardOrder().get_circuit(invertible=11, modulus=25)

print(qc.num_qubits, qc.depth())

# returns 12, 94
```

You can also gain access to the quantum circuit using number factorer. When you instantiate a number factoring algorithm with an order finding algorithm, use the ```.order_algo``` aspect to gain access to the raw order finding algorithm. If the algorithm is quantum in nature, the ```.get_circuit()``` method will work exactly the same way as above.

```python
from number_factorer import (
    Number_Factorer, 
    ShorOrder, 
    ShorFactorization 
)

nf = NumberFactorer(ShorFactorization(), ShorOrder())

order_finder = nf.order_algo #== ShorOrder()

order_finder.get_circuit(2, 5).draw('mpl')
```

![Alt text](/images/shor25.png)

## 2. Comparing Factorization Methods

Let's now embark on a elementary comparison of the efficacy of each number factorization algorithm and their components. 

### Comparing the quantum algorithms

Given an $n$-bit integer $N$,

- ShorOrder will use $4n+1$ qubits, and
- BeauregardOrder will use $2n+2$ qubits. 

This is crucial because Qiskit's AerSimulator can only accept a maximum of 30 qubits meaning if you choose ShorOrder you can only reliably factor $7$-bit integers (i.e. less than $2^8=128$), whereas BeauregardOrder can be used to reliably factor $14$-bit integers (i.e. less than $2^{15}=32768$)

Another consideration is circuit depth. For a comparatively large number of qubits, ShorOrder uses vastly less gates than BeauregardOrder. The diagram below depicts the average number of gates required to find the order of each integer.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from number_factorer import ShorOrder, BeauregardOrder

shor_gates = []
beau_gates = []

for n in range(2, 8):
    integer = 2 ** n
    shor_gates.append(ShorOrder().get_circuit(integer - 1, integer).depth())
    beau_gates.append(BeauregardOrder().get_circuit(integer - 1, integer).depth())

results = []

for N in range(2, 8):
    results.append(('Shor', N, shor_gates[N - 2]))
    results.append(('Beau', N, beau_gates[N - 2]))

df = pd.DataFrame(results, columns = ["Algorithm", "num_bits", "num_gates"])

for algo in df["Algorithm"].unique():
    subset = df[df["Algorithm"] == algo]
    plt.scatter(subset["num_bits"], subset["num_gates"], label = algo, alpha = 0.7)

plt.xlabel("Number of Bits")
plt.ylabel("Number of Quantum Gates")
plt.legend()
plt.show()
```

![PICTURE](/images/gate_compare.png)

#### Run time of quantum algorithms and classical processing

Despire the fact that ShorOrder uses way less gates than Beauregard, it turns out as far as classical simulation of quantum circuits is concerned, the number of qubits is a much more pressing issue. Indeed, randomly selects an integer within each bit range and times how long each factorization algorithm runs before terminating.

```python
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from number_factorer import (
    Number_Factorer,
    ShorFactorization,
    ShorOrder,
    BeauregardOrder
)

nf_shor = Number_Factorer(ShorFactorization(), ShorOrder())
nf_beau = Number_Factorer(ShorFactorization(), BeauregardOrder())

shor_time = []
beau_time = []

for n in range(1, 8):
    integer = random.randint(2 ** n, (2 ** (n + 1)) - 1)

    start_shor = time.perf_counter()
    nf_shor.factor(integer)
    end_shor = time.perf_counter()
    nf_beau.factor(integer)
    end_beau = time.perf_counter()

    shor_time.append(end_shor - start_shor)
    beau_time.append(end_beau - end_shor)

results = []

for N in range(1, 8):
    results.append(('Shor', N + 1, float(np.log10(shor_time[N - 1]))))
    results.append(('Beau', N + 1, float(np.log10(beau_time[N - 1]))))

df = pd.DataFrame(results, columns = ["Algorithm", "num_bits", "log_comp_time"])

for algo in df["Algorithm"].unique():
    subset = df[df["Algorithm"] == algo]
    plt.scatter(subset["num_bits"], subset["log_comp_time"], label = algo, alpha = 0.7)

plt.xlabel("Number of Bits")
plt.ylabel("log(Run Time (seconds) )")
plt.legend(loc='upper left')
plt.show()
```

![PICTURE](/images/runtime_quantum.png)

You can see in the above that Shor in general does much worse that Beauregard. They may seem somewhat close, but note that the vertical axis is the logarithm of run time! Indeed, for the 7 bit integer, the factoring algorithm using ShorOrder took around 2000 seconds which is approximately 30 minutes, wheras BeauregardOrder took only about a second. 

One way to improve this run time issue is to use the other classical processing algorithm EkeraFactorization. This only calls on the quantum algorithm once and relegates the rest of the calculation to classical processing. Running the same code with EkeraFactorization

### Comparing Quantum and Classical Order Finding

As one might expect, the simulated quantum circuits are vastly slower than the classical order finding algorithms. However, we crucially would like to get an estimate on how well our circuits would run on a sufficiently powerful and fault-tolerant quantum computer. To that end, I have implemented the ```.quantum_time_estimate()``` method for each of the factorization algorithms. To run this, pick one of the classical processing algorithms ShorFactorizer() or EkeraFactorizer() and choose one of the quantum order finding algorithms ShorOrder() or BeauregardOrder(). To estimate (in seconds) how long it would take to factor an integer $N$ run the code below.

```python
from number_factorer import ShorFactorization, EkeraFactorization

N = 115 # number to factor

# estimate time to factor N using ShorOrder() and ShorFactorization()
ShorFactorization().quantum_time_estimate(115, 'shor') 
# returns approx 0.00026224982889000437


# estimate time to factor N using BeauregardOrder() and ShorFactorization()
ShorFactorization().quantum_time_estimate(115, 'beau') 
# returns approx 6.3318293541669846e-06


# estimate time to factor N using ShorOrder() and EkeraFactorization()
EkeraFactorization().quantum_time_estimate(115, 'shor') 
# returns approx 0.00027508298830687997


# estimate time to factor N using BeauregardOrder() and EkeraFactorization()
EkeraFactorization().quantum_time_estimate(115, 'beau') 
# returns approx 0.0013107499431073664
```

For an anecdotal reference, using ShorOrder() with ShorFactorization() to factor $115$ took 2 hours on my machine. And so, the benefit is now we can compare the hypothetical performance of our quantum algorithms on numbers much larger than what would be feasible to simulate. 

The code below compares the performance of the quantum factorization algorithms and their classical counterparts for large numbers.



[PICTURE]




