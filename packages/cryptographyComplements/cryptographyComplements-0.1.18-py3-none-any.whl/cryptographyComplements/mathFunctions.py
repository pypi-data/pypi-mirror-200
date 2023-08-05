from cryptographyComplements.tools import Numbers # required class, because contains functions used by some of them below

def EulerTotientFunction(number: int):
    "Calculate, from a given number, the Euler Totient function."
    if not Numbers.isNumber(number):
        return None

    result = int(number)
    p = 2
    while p * p <= number:
        if number % p == 0:
            while number % p == 0:
                number //= p
            result -= result // p
        p += 1
    if number > 1:
        result -= result // number
    return result

def EuclideanAlgorithm(a: int, b: int):
    "Given two numbers, a and b, calculate their MCD."
    if not Numbers.isNumber(a, b):
        return None

    a, b = int(a), int(b)

    while True:
        r = a % b
        if r != 0:
            a, b, remainder = b, r, r # remainder = r needs to be kept, because if r = 0, then it will be stored back.
        else:
            return remainder

def ExtendedEuclideanAlgorithm(a: int, b: int):
    "Given two numbers, a and b, calculate their MCD. \nThe Extended Euclidean Algorithm is faster than Euclidean Algorithm. It uses the equation: au + bv = gcd(a,b)"

    if not Numbers.isNumber(a, b):
        return None
    a, b = int(a), int(b)

    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        r = a % b
        x = x0 - (a // b)*x1
        y = y0 - (a // b)*y1
        a, b, x0, x1, y0, y1 = b, r, x1, x, y1, y

    return a

def calculateOrder(g:int, p:int):
    "Given a number: g, and a prime number. Calculate the order of g in p."
    k = 1
    order = 0
    while order != 1:
        order = (g**k) % p
        k += 1
    
    return int(k-1) # -1 needs to be added because +1 will be added even if the order is 1, because the iteration when order becomes 1 is not completed yet.

def InverseModuloTrialError(number: int, mod:int):
    "Calculate by a given number and modulo the inverse modulo of them. It uses the trial and error method so for larger numbers is not recommended."
    from cryptographyComplements.mathFunctions import ExtendedEuclideanAlgorithm

    if ExtendedEuclideanAlgorithm(number, mod) != 1: # checks if exists an inverse modulo
        return None

    for i in range(mod):
        if (number*i % mod) == 1:
            return i
        
        i += 1

def WillansFormula(n: int):
    "From a given number in input calculate the Willans Formula. \nNote this formula can't be used for numbers > 7 because of Overflow Error."
    from math import floor, cos, pi, factorial
    return 1+ sum([
        floor(pow(
        n/sum([
            floor(pow(cos(pi * (float(factorial(j-1)) + 1)/j), 2))
            for j in range(1, i+1)
        ]), 1/n))
        for i in range(1, (2**n)+1)
    ])

def CollatzConjecture(n: int):
    "From a given number in input, calculate the Collatz Conjecture. \n\nIt will return True if the number entered in input it's in a cyclic group and False if it the number in input gets to 1."
    number = n
    while True:
        if n == 1:
            return False

        n = 3*n + 1     
        while n % 2 == 0:
            n //= 2

        if n == number:
            print(f"Cyclic number found: {n}")
            return True

class DiscreteLogarithm:
    "This class contains all the Discrete Logarithm algorithm to solve the Discrete Logarithm Problem: g^x = h (mod p)"

    def TrialErrorMethod(base: int, congruence: int, modulo: int):
        "Calculate, from given base, congruence and modulo, the discrete logarithm using the trial and error method. \nWarning: The function won't stop even if there isn't a number that can resolve the discrete logarithm."
        if not Numbers.isNumber(base, congruence, modulo):
            return None
        
        BASE, CONGRUENCE, MODULO = int(base), int(congruence), int(modulo)
        power = 0

        while True:
            number = base**power
            if number % MODULO == CONGRUENCE % MODULO:
                print(f"log{BASE} {power} \u2261 {CONGRUENCE} (mod {MODULO})")
                logarithm = [BASE, power, CONGRUENCE, MODULO]
                return logarithm
            
            power += 1

    def ShanksBabyStepGiantStepAlgorithm(g:int, h:int, p:int):
        "Using the Shanks Baby-Step Giant-Step algorithm, solve the Discrete Logarithm Problem: g^x = h (mod p) \n\nThe functions returns None if there isn't a solution to the algorithm"
        
        from math import floor, sqrt
        from cryptographyComplements.mathFunctions import calculateOrder
        n = floor(sqrt(calculateOrder(g, p))) + 1

        u = (g**(EulerTotientFunction(p)-n)) % p

        l1, l2 = [], []

        for i in range(0, n+1):
            l1.append((g**i) % p)

        for j in range(0, n):
            keep = (h*(u**j)) % p
            l2.append((h*(u**j)) % p)
            if keep in l1:
                break

        try:
            value = l1.index(keep)
        except ValueError:
            return None

        value2 = l2.index(keep)

        x = value + (n * value2)

        return x
    
def ChineseRemainderTheorem(congruences:list, modulo: list):
    "From a list of congruences and a list of modulos, tuples are accepted too, of the same lenght, calculate the Chinese Remainder Theorem. \n\nIf there is a solution it will be returned as a number, but if there isn't it will return None."
    try:
        for i in range(0, len(modulo)):
            if i == (len(modulo)-1):
                break

            try:
                # check if the numbers are relatively prime, if not there isn't a solution to the congruence
                if ExtendedEuclideanAlgorithm(int(modulo[i]), int(modulo[i+1])) != 1:
                    return None

            except ValueError:
                return None

    except TypeError:
        return None
          
    M = Numbers.listMultiplication(modulo)
    totalM = []

    for i in modulo:
        moduloI = M/i
        totalM.append(moduloI)

    moduloInverses = []
    for i in range(0, len(congruences)):
        moduloI = InverseModuloTrialError(totalM[i], modulo[i])

        if moduloI == None: # If there is no inverse modulo, then there isn't a solution for that congruence
            return None


        moduloInverses.append(moduloI)

    y = 0
    for i in range(0, len(congruences)):
        y += (moduloInverses[i]* totalM[i] * congruences[i])

    return int((y % M))