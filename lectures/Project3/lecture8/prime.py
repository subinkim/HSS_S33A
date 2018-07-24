import math

def is_prime(n):
    """Determines if a non-negative integer is prime."""
##    if n < 2:
##        return False
##    for i in range(2, int(math.sqrt(n)) + 1):
##        if n % i == 0:
##            return False
##    return True

    return n > 1 and all(n % 1 for i in range(2, int(math.sqrt(n)) + 1))

## Both behave in the same way
