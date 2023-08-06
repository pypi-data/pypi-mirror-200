from cryptographyComplements.tools import Numbers
def EulerTotientPrimalityTest(n: int):
    "Using the equation: p - 1 = phi(p), you can verify if a number is prime. \nThis primality test is deterministic but numbers greater than 2^60 requires to much time, and computational power, to be calculated using this primality test."

    from cryptographyComplements.mathFunctions import EulerTotientFunction

    if not Numbers.isNumber(n): # verifying if the input is a number 
        return False

    elif int(n) < 0: # verifying if the input belongs to N
        return False

    n = int(n)
    if n == 5 or n==2: # needs to be put because in the if condition below it would be set to false
        return True
    
    elif Numbers.isEven(n) or str(n).endswith("5"): # skip the nums that are not prime
        return False

    phi = EulerTotientFunction(n)

    if (n - 1) == phi:
        return True
    
    return False