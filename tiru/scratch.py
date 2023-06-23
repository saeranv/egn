import numpy as np
import matplotlib.pyplot as plt
import viz.plt as vlt


f, ax = vlt.subplots()
ax[0].scatter(np.random.rand(100), np.random.rand(100))
vlt.stream_plt(f)
print('a')
