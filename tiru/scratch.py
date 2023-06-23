import numpy as np
import matplotlib.pyplot as plt
import viz.plt as vlt


# f, ax = vlt.subplots()
# ax[0].scatter(np.random.rand(100), np.random.rand(100),c='b')
# vlt.stream_plt(f)

fact = lambda v: np.prod(np.arange(1,v+1))
v = fact(23) / (23*23)
print(v)
