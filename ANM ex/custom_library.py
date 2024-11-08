def extended_euclidean(a, b):
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, b
    while v3 != 0:
        q = u3 // v3
        t1, t2, t3 = u1 - q * v1, u2 - q * v2, u3 - q * v3
        u1, u2, u3 = v1, v2, v3
        v1, v2, v3 = t1, t2, t3
    return u1, u2, u3

def modular_exponentiation(a, b, m):
    x = []
    while b:
        x.append(b & 1)
        b = b >> 1

    size = len(x)
    myPow = [a % m]

    for i in range(1, size):
        p = myPow[i-1]**2 % m
        myPow.append(p)

    res = 1
    for i in range(size):
        if x[i] != 0:
            res *= myPow[i]
            res %= m

    return res

def get_segment_size(number):
    temp = 1
    result = 0
    while temp < number:
        result += 1
        temp *= 2
    result -= 1
    from math import floor
    result = floor(result/8)
    return result
