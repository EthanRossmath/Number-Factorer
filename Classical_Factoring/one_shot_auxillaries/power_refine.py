import gmpy2
from classical_shor_auxillaries.is_power import kroot

def power_refine(factor_list):
    new_list = []

    for a in factor_list:
        if gmpy2.is_power(a[0]):
            base, exponent = kroot(a[0])
            new_list.append((base, exponent * a[1]))
        
        else: 
            new_list.append(a)
    
    return new_list