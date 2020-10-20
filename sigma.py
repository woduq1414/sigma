from fractions import Fraction
import time
import sys
import copy




class Polynomial():


    def __init__(self, **kwargs):
        if "size" in kwargs:
            self.coef = [Fraction(0)] * kwargs["size"]
        elif "coef" in kwargs:
            self.coef = kwargs["coef"]

        if "char" in kwargs:
            self.char = kwargs["char"]
        else:
            self.char = "x"

    def set(self, _coef):
        self.coef = _coef

    def get_degree(self):
        for i in range(len(self.coef) - 1, -1, -1):
            if self.coef[i] != 0:
                break
        return i

    def add(self, other):

        if len(self.coef) - 1 < other.get_degree():
            self.coef += [Fraction(0)] * (other.get_degree() - len(self.coef) + 1)
        if len(other.coef) - 1 < self.get_degree():
            other.coef += [Fraction(0)] * (self.get_degree() - len(other.coef) + 1)

        for i in range(max(self.get_degree(), other.get_degree()) + 1):
            self.coef[i] += other.coef[i]

    def subtract(self, other):

        if len(self.coef) - 1 < other.get_degree():
            self.coef += [Fraction(0)] * (other.get_degree() - len(self.coef) + 1)
        if len(other.coef) - 1 < self.get_degree():
            other.coef += [Fraction(0)] * (self.get_degree() - len(other.coef) + 1)

        for i in range(max(self.get_degree(), other.get_degree()) + 1):
            self.coef[i] -= other.coef[i]

    def multiple(self, n):
        for i in range(self.get_degree() + 1):
            self.coef[i] *= n

    def divide(self, n):

        for i in range(self.get_degree() + 1):
            self.coef[i] /= n

    def __str__(self):
        result = []
        for i in range(self.get_degree(), -1, -1):
            if self.coef[i] == 0:
                continue
            if i != 0:
                result.append(f"{self.coef[i]}{self.char}^{i}")
            else:
                result.append(f"{self.coef[i]}")
        return " + ".join(result)


def in_cache(func):
    cache = {}

    def wrapper(n):

        if n in cache:

            return cache[n]
        else:
            cache[n] = func(n)
            return cache[n]

    return wrapper


@in_cache
def factorial(n):
    return n * factorial(n - 1) if n > 1 else 1


def combination(n, r):
    return factorial(n) // factorial(n - r) // factorial(r)


@in_cache
def sigma(x):
    if x == 0:
        return Polynomial(coef=[Fraction(0), Fraction(1)], char="n")
    else:
        temp = [0] * (x + 2)
        for i in range(x + 1, 0, -1):
            temp[i] = combination(x + 1, x + 1 - i)
        p1 = Polynomial(coef=temp, char="n")

        p2 = Polynomial(size=x + 1, char="n")
        for i in range(x - 1, -1, -1):
            temp_p = sigma(i)
            temp_p2 = copy.deepcopy(temp_p)
            temp_p2.multiple(combination(x + 1, x + 1 - i))
            p2.add(temp_p2)

        p1.subtract(p2)

        p1.divide(x + 1)

        return p1


st = time.time()
sys.setrecursionlimit(10 ** 4)
for i in range(1, 101):
    print(f"k^{i}: ", sigma(i))

print(time.time() - st, "초")




