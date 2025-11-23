import gmpy2

def baby_giant_order(invertible: int, modulus: int) -> int:
        """
        Finds the order of an invertible element in (Z/modulus)^* using Baby Steps, Giant Steps
        algorithm due to Shanks.
        """

        # compute bound for first round of exponentiation
        baby_bound = int(gmpy2.ceil(gmpy2.sqrt(modulus - 1)))

        # initialize a dictionary of modular powers
        power_dict = {1:invertible}

        # begin at the first power
        baby_power = invertible

        # BABY STEPS: compute invertible ** i for i between 2 and baby_bound
        for i in range(2, baby_bound + 1):
            baby_power = (invertible * baby_power) % modulus

            # if we hit 1 at any point, we've already found the bound
            if baby_power == 1:
                return i
        
            # add power to the dictionary of powers
            else:
                power_dict[i] = baby_power
    
        # GIANT STEPS: now compute powers of the form invertible ** (i * baby_bound) until a 
        # collision is detected with an already computed power

        exponent = 2 * baby_bound
        big_power = pow(baby_power, 2, modulus)

        while big_power not in power_dict.values():
            power_dict[exponent] = big_power

            big_power = (big_power * baby_power) % modulus
            exponent = exponent + baby_bound

        # Compute the collision
        other_exponent = min((j for j in power_dict if power_dict[j] == big_power))

        return exponent - other_exponent