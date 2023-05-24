from sys import stdout
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
pp = print

RAND = np.random.RandomState(101)

X = RAND.uniform(0, 1, 1000)


def sp(row=1, col=1, dimx=10, dimy=7):
    fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
    ax = ax if isinstance(ax, np.ndarray) else [ax]
    return fig, ax


def ezplt(xvec:np.ndarray, yvec:np.ndarray, plt_fn:str='scatter', *args, **kwargs) -> None:
    """Write binary data to stdout."""

    axs = kwargs.pop('ax') if 'ax' in kwargs else sp()[1]

    buffer = BytesIO()
    for ax in axs:
        ax = getattr(ax, plt_fn)(xvec, yvec, *args, **kwargs)


    plt.savefig(buffer, format='jpg', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    stdout.buffer.write(buffer.getvalue())
    stdout.flush()

# Add random value here for print from stdin to work.
1

