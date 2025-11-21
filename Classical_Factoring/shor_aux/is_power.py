import gmpy2

def kroot(number: int) -> list[int]:
        """
        Takes a number and determines if it is a perfect power. If so, returns
        list [base, exponent] where number = base ** exponent and exponent is
        maximal.
        """
        if not gmpy2.is_power(number):
            return False


        k = number.bit_length()
        exp = 1
        base = number

        for i in range(k, 1, -1):
            val, bool = gmpy2.iroot(number, i)

            if bool:

                exp = i
                base = int(val)

        return [base, exp]