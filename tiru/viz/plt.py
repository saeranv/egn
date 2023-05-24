"""ezplt(X, np.sin(X), 'scatter', c='red', s=10, ax=suplots(1, 2,
10, 7)[0])"""
from sys import stdout
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
pp = print

RAND = np.random.RandomState(101)
X = RAND.uniform(0, 1, 1000)


def subplots(row=1, col=1, dimx=10, dimy=7):
    fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
    ax = ax if isinstance(ax, np.ndarray) else [ax]
    return fig, ax


def ezplt(x:np.ndarray, y:np.ndarray, plt_fn:str='scatter', *args, **kwargs) -> None:
    """Write binary data to stdout."""

    axs = kwargs.pop('ax') if 'ax' in kwargs else subplots()[1]

    buffer = BytesIO()
    axs = [getattr(ax, plt_fn)(x, y, *args, **kwargs)
           for ax in axs]

    plt.savefig(buffer, format='jpg', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    stdout.buffer.write(buffer.getvalue())
    stdout.flush()

