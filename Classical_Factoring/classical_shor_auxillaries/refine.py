import math

def refine(factors: list):
    L = []
    for m in factors:
        L.append((m, 1))

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

def consolidate_pairs(factor_list: list):
    combine_dict = {}
    for a in factor_list:
        if a[0] in combine_dict:
            combine_dict[a[0]] += a[1]
        else:
            combine_dict[a[0]] = a[1]
    combine_list = []
    for a in combine_dict:
        combine_list.append((a, combine_dict[a]))
    
    combine_list.sort(key=lambda x: x[0])
    return combine_list