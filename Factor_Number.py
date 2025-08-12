class Factor_Number:
    def __init__(self, isprime_power, prime_power, order, randomness, powermod, gcd):
        self.isprime_power = isprime_power
        self.prime_power = prime_power
        self.order = order
        self.randomness = randomness
        self.powermod = powermod
        self.gcd = gcd

    def isprime_power(self, integer):
        return self._isprime_power(integer)

    def prime_power(self, integer):
        return self._prime_power(integer)

    def order(self, element, modulus):
        return self._order(element, modulus)
    
    def randomness(self, lower_bound, upper_bound):
        return self._randomness(lower_bound, upper_bound)
    
    def powermod(self, base, exponent, modulus):
        return self._powermod(base, exponent, modulus)
    
    def gcd(self, number1, number2):
        return self._gcd(number1,number2)
    
    def splitter(self, N):
        
        a = self.randomness(2, N)
        d = self.gcd(a, N)

        if d > 1:
            return (d, N // d)
        
        r = self.order(a, N)

        if (r % 2 == 1):
            return (1, N)
        
        x = (self.powermod(a, r // 2, N) - 1) % N

        d = self.gcd(x, N)

        return (d, N // d)


        





        
        


        