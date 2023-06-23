import numpy as np


def fact(n1,n0):
    return np.prod(np.arange(n0,n1+1, dtype=np.float64))


print(fact(100,5))
