import gmpy2

def unbound_convergents(number, modulus):
    floaty = number
    num_prev, num = 0, 1
    denom_prev, denom = 1, 0

    bound = 1 / (2 * (modulus ** 2))

    convergents = []
    while True:
        int_part = gmpy2.floor(floaty)

        old_num = num 
        old_denom = denom

        num = int_part * num + num_prev
        denom = int_part * denom + denom_prev


        convergents.append((num, denom))

        ratio = num / denom

        num_prev = old_num
        denom_prev = old_denom

        remainder = floaty - int_part 

        if remainder < bound:
            break

        floaty = 1 / remainder

        difference = abs(number - ratio)

        if (difference < bound) and (num < modulus) and (denom < modulus):
            break

        if denom > modulus:
            num = num_prev
            denom = denom_prev
            break
            
    
    return int(num), int(denom)

def get_denominator(binary_string, modulus, algo_name: str):
    n = len(binary_string)
    dec = 0

    if algo_name == 'shor':
        power_of_two = 2
    
    if algo_name == 'beau':
        power_of_two = 4
        
    for i in range(n):
        dec += int(binary_string[i]) / power_of_two
        power_of_two *= 2
    
    ratio = unbound_convergents(dec, modulus)

    
    return ratio[1]

def cont_frac(number: float, error: float, bound: float) -> list[int]:
    """
    Given a floating point number, computes pair of integers [num, denom]
    where |number - num / denom| < bound.
    """

    num_prev = int(gmpy2.floor(number))

    if (number - num_prev) < max(bound, error):
        return [num_prev, 1]
    
    denom_prev = 1

    conv = int(gmpy2.floor(1 / (number - num_prev)))

    num = 1 + num_prev * conv
    denom = conv

    distance = abs(number - num / denom)

    if distance < bound:
        return [num, denom]
    
    diff = (1 / (number - num_prev)) - conv 

    if diff < error:
        return [num, denom]
    
    while (distance >= bound) and (diff >= error):
        recip = 1 / diff
        conv = int(gmpy2.floor(recip))

        diff = recip - conv 

        numpp = num
        denompp = denom 

        num = conv * num + num_prev 
        denom = conv * denom + denom_prev

        num_prev = numpp
        denom_prev = denompp

        distance = abs(number - num / denom)
    
    return [num, denom]
