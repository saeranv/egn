from sys import stdout
from os import fdopen
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
pp = print

RAND = np.random.RandomState(101)

X = np.arange(1000)
Y = np.arange(1000)

def subplots(row=1, col=1, dimx=7, dimy=10):
    fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
    ax = ax if isinstance(ax, np.ndarray) else [ax]
    return fig, ax


def ezplt(X, Y, *args, **kwargs):
    """Write binary data to stdout."""

    ax = kwargs['ax'] if 'ax' in kwargs else subplots(1, 2)[1]
    print(ax, len(ax))
    print(subplots(1,1)[1])

    # buffer = BytesIO()
    # ax.savefig(buffer, format='jpg')
    # buffer.seek(0)
    # stdout.buffer.write(buffer.getvalue())

if __name__ == '__main__':



    ezplt()

