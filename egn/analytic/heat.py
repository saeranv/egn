"""Heat transfer equations."""

# from typing import Union
from numpy.typing import NDArray
import numpy as np

# ndfloat = Union[NDArray[np.float64], float]
ndfloat = NDArray[np.float64]


def lumped_node(bi: ndfloat, fo: ndfloat) -> ndfloat:
    """Dimensionless transient lumped node eqn.

    Solves for theta given Bi and tau,
        theta(tau) = exp(Bi tau)

    Usage:
    .. code-block:: python

        # Define dimensionless params
        char_len = vol / area  # [m]
        bi = mat.biot_coef(h_c, char_len, k)
        alpha = mat.diffusivity_coef(k, rho, C_p)
        fo = mat.fourier_coef(alpha, char_len, dt)

        # Convert to K, and then dimensionless theta
        T0 += 273.15; T_ext += 273.15 # K
        delta_T = np.abs(T0 - T_ext)

        # theta(t) = T(t) / delta_T: dimensionless temp
        # T = theta * delta_T
        theta = lumped_node(bi, fo)

        temps = theta * delta_T

    Args:
        Bi: Biot number = h-Lc / k [-]
        tau: dimensionless time = a t / Lc2 [-]

    Returns dimensionless temp, theta = (T - T_ext) / (T0 - T_ext) [-]
    """
    # T =  (theta * (T0 - T_ext)) + T_ext)
    if bi >= 0.1:
        print("Warning: Biot must be <= 0.1 for lumped node assumption, "
              f"but got Biot of `{bi}`")

    return np.exp(-1 * bi * fo)
