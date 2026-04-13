import math
import random

class QuantumAttacker:
    def __init__(self):
        pass

    def quantum_period(self, a, N):
        r = 1
        while True:
            if pow(a, r, N) == 1:
                return r
            r += 1

    def shors_algorithm(self, N):
        print(f"Running Shor's Algorithm for N = {N}")
        a = random.randint(2, N-1)
        print(f"Randomly chosen a: {a}")
        if math.gcd(a, N) != 1:
            print(f"Found a non-trivial factor: {math.gcd(a, N)}")
            return math.gcd(a, N), N // math.gcd(a, N)
        
        r = self.quantum_period(a, N)
        print(f"Found period r: {r}")
        if r % 2 != 0:
            print("Period is odd, retrying...")
            return self.shors_algorithm(N)
        
        half_r = r // 2
        guess1 = math.gcd(pow(a, half_r, N) - 1, N)
        guess2 = math.gcd(pow(a, half_r, N) + 1, N)

        factors = []
        if 1 < guess1 < N:
            factors.append(guess1)
        if 1 < guess2 < N:
            factors.append(guess2)

        if len(factors) == 0:
            print("No non-trivial factors found, retrying...")
            return self.shors_algorithm(N)
        else:
            p = factors[0]
            q = N // p
            print(f"Found factors: {p}, {q}")
            return p, q