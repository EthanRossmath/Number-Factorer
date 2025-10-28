def power_of_two(n):
    if (n % 2) != 0:
        return [(n, 1)]
    
    k = 0
    m = n 

    while (m % 2) == 0:
        k += 1
        m //= 2
    
    return [(2, k), (m, 1)]