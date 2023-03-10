# Probability SDF

from typing import Callable
import numpy as np
import numpy.typing as npt


def point_sdf(pt:npt.NDArray) -> Callable:
    """Point SDF."""

    def _sdf(x:npt.NDArray) -> np.float64:
        return np.linalg.norm(pt - x)

    return _sdf
