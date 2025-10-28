import gmpy2

def factorization_complete(factor_list: list):
    for a in factor_list:
        if not gmpy2.is_prime(a[0]):
            return False
    
    return True