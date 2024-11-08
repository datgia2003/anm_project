import math
import sympy
import custom_library
import json

class RSA_Key_Generator:
    def __init__(self, key_size=1024):
        self.p = sympy.randprime(2**int((key_size/2 - 1)), 2**int((key_size/2)))
        self.q = sympy.randprime(2**int((key_size/2 - 1)), 2**int((key_size/2)))
        self.n = self.p * self.q
        self.phi_n = (self.p - 1) * (self.q - 1)
        
        self.e = 65537
        while math.gcd(self.e, self.phi_n) != 1:
            self.e += 2

        self.d = custom_library.extended_euclidean(self.e, self.phi_n)[0]
        if self.d < 0:
            self.d += self.phi_n

        self.public_key = {
            "n": self.n,
            "e": self.e
        }

        self.private_key = {
            "n": self.n,
            "d": self.d
        }

    def save_keys(self, public_key_path, private_key_path):
        with open(public_key_path, 'w') as f:
            f.write(json.dumps(self.public_key))
        
        with open(private_key_path, 'w') as f:
            f.write(json.dumps(self.private_key))

        return public_key_path, private_key_path
