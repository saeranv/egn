# For ezplt
from sys import stdout
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
pp = print


RAND = np.random.RandomState(101)
X = RAND.uniform(0, 1, 1000)


def plt_buffer(plt):
    """Raw bytes from plt to stdout."""
    buffer = BytesIO()
    plt.savefig(buffer, format='jpg', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    stdout.buffer.write(buffer.getvalue())
    stdout.flush()


def subplots(row=1, col=1, dimx=10, dimy=7):
    fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
    ax = ax if isinstance(ax, np.ndarray) else [ax]
    return ax


