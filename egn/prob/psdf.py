# Probability SDF

from typing import Callable
import numpy as np
import numpy.typing as npt

"""
x_org | xdir: [[x1, x2, x3], [y1, y2, y3]]
x_vec: x_org + x_dir
"""


def point_sdf(a_vec:npt.NDArray[float]) -> Callable:
    """Returns SDF for shape vector A given input vector B."""

    def _point_fn(b_vec:npt.NDArray[float]) -> np.float64:
        return np.linalg.norm(b_vec - a_vec)

    return _point_fn


def circle_sdf(a_vec:npt.NDArray[float], radius:float) -> Callable:
    """Circle SDF."""

    def _circle_fn(b_vec:npt.NDArray[float]) -> np.float64:
        c_vec = b_vec - a_vec  # vector pointing from A to B
        return radius - np.linalg.norm(c_vec)

    return _circle_fn


