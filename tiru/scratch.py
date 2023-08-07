import numpy as np
import viz.plt as vlt

def fact(n1,n0):
    vals = np.arange(n0, n1).astype(np.float64)
    # print(vals, vals.size)
    return np.prod(vals)

p = fact(365, 365-23) / (365.0 ** 23)

print(p)
