# For ezplt
from sys import stdout
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt


def stream_plt(fig) -> None:
    """Stream bytes from fig to stdout."""
    buffer = BytesIO()
    fig.savefig(buffer, format='jpg', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    stdout.buffer.write(buffer.getvalue())
    stdout.flush()


def subplots(row=1, col=1, dimx=10, dimy=7):
    fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
    ax = np.array([ax]) if not isinstance(ax, np.ndarray) else ax
    return fig, ax
