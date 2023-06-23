import numpy as np


def fact(n1,n0):
    return np.prod(np.arange(n0, n1+1, dtype=np.float64))


p = fact(365, 365-23) / (365.0 ** 23.0)

print(p)
