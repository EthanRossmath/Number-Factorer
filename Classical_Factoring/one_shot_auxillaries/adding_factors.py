import math

def refine(factors: list):
    L = factors

    while True:
        pair = None 
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                if math.gcd(L[i][0], L[j][0]) != 1:
                    pair = (i, j)
                    break
            if pair:
                break
        if not pair:
            break 

        i, j = pair

        d = math.gcd(L[i][0], L[j][0])
        new1 = (L[i][0] // d, L[i][1])
        new2 = (d, L[i][1]+L[j][1])
        new3 = (L[j][0] // d, L[j][1])
        new_guys = [new1, new2, new3]

        for idx in sorted([i, j], reverse=True):
            del L[idx]
        
        for newer in new_guys:
            if newer[0] != 1:
                L.append(newer)
    
    L.sort(key=lambda x: x[0])
    return L

def add_factor(factor_list: list, new_factor: int):
    """
    factor_list = [(a_1, n_1), ..., (a_k, n_k)] is a factorization of a number N, i.e.
    N = (a_1 ** n_1) * ... * (a_k ** n_k)
    and new_factor is a divisor of N. Outputs a new refined list
    """

    new_list = []

    for a in factor_list:
        d = math.gcd(a[0], new_factor)
        if d == 1:
            new_list.append(a)
        elif a[0] // d == 1:
            new_list.append((d, a[1]))
        else: 
            new_list.extend([(a[0] // d, a[1]), (d, a[1])])

    return refine(new_list)