import gmpy2

def find_order(invertible: int, modulus: int) -> int:
        """
        Finds the order of an invertible element in (Z/modulus)^* using Baby Steps, Giant Steps
        algorithm due to Shanks.
        """
        b = gmpy2.ceil(gmpy2.sqrt(modulus - 1))

        look_up_dict = {1:invertible}
        baby_power = invertible

        for i in range(2, b + 1):
            baby_power = (invertible * baby_power) % modulus

            if baby_power == 1:
                return i
        
            else:
                look_up_dict[i] = baby_power
    

        exponent = 2 * b
        big_power = pow(baby_power, 2, modulus)

        while big_power not in look_up_dict.values():
            look_up_dict[exponent] = big_power

            big_power = (big_power * baby_power) % modulus
            exponent = exponent + b
    
        other_exponent = min((j for j in look_up_dict if look_up_dict[j] == big_power))

        return exponent - other_exponent