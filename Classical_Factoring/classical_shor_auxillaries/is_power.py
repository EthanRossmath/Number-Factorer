import gmpy2

def kroot(n):
    if not gmpy2.is_power(n):
        return ValueError(f'{n} is not a power')


    k = n.bit_length()
    exp = 1
    base = n

    for i in range(k, 1, -1):
        val, bool = gmpy2.iroot(n, i)
        if bool:
            exp = i
            base = int(val)
    return [base, exp]