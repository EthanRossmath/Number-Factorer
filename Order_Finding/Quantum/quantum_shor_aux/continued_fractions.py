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

def get_denominator(binary_string, modulus):
    n = len(binary_string)
    dec = 0

    power_of_two = 2
    for i in range(n):
        dec += int(binary_string[i]) / power_of_two
        power_of_two *= 2
    
    ratio = unbound_convergents(dec, modulus)

    
    return ratio[1]
