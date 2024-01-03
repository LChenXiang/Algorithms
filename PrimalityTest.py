import random
from ModExpo import modularExponentiation

"""
Miller-Rabin's primality test
True : Prime
False: Composite
"""
def miller_rabin(n, k):
    
    # 2 and 3 are primes
    if n == 2 or n == 3:
        return True

    # all even numbers are not primes
    if not (n & 1):
        return False

    # factor n-1 as (2ˆs)*t, where t is odd
    s = 0
    t = n - 1

    while t % 2 == 0: # if even
        s += 1
        t /= 2

    # run k random tests
    for _ in range(k):
        # random witness
        a = random.randrange(2, n-1)

        # fermat's test on this witness
        if fermat_test(a, s) != 1:
            return False
        
        # sequence test
        for j in range(2, s):
            x_j = fermat_test(a, j)
            x_j1 = fermat_test(a, j-1)

            if x_j == 1 and (x_j1 != 1 and x_j1 != n-1):
                return False

    return True  # ...probably.
        
        
# formula of fermat's little theorem
def fermat_test(a, n):
    return modularExponentiation(a, n-1, n) # a^n-1 mod n

def is_prime(n):
    for k in range(2, n):
        if n % k == 0:
            return False

    return True


if __name__ == '__main__':
    s = 27
    # print(s.bit_length())
    k = s.bit_length() 
    print(k)
    print(miller_rabin(s, k))
    result = is_prime(s)
    print(result)

    for _ in range(100):
        test = miller_rabin(s, k)
        if test != result:
            print(test)
            break
    print("DOne")