def largest_exponent(prime, upperbound):
    """
    Returns the largest positive integer a so that prime ** a <= upperbound
    """

    a = 0
    x = 1

    while x < upperbound:
        x = x * prime
        a += 1
    
    return a - 1