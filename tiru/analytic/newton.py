# Newton's law of cooling.
import numpy as np
import matplotlib.pyplot as plt


def newton(
    h_c, A, Cp, Vol, p,
    T_int_0, T_ext,
    dt, Nt
    ) -> np.ndarray:
    """Predict array of temperatures for node given parameters.

    Args:
        # Diffusivity (alpha) params: hA/pCV
        h_c: Node surface convective coefficient [W/m2-K]
        A: Node surface area [m2]
        p: Node density in [kg/m3]
        Cp: Node specific heat capacity [J/kg-K]
        Vol: Node volume [m3]

        # Initial temperatures
        T_int: Node temperature [C]
        T_ext: Ambient temperature [C]

        # Time params
        dt: time step [s]
        Nt: total time elapsed [s]

    Returns (Nt/dt) array of temperatures.
    """

    # TODO: clarify Cp against Cv
    # Rough check of physically possible
    eps = 1e-10
    assert h_c >= eps
    assert A >= eps
    assert Cp >= eps
    assert Vol >= eps
    assert p >= eps
    assert dt >= eps
    assert Nt >= dt

    # Convert to K
    T_int_0,  T_ext = T_int_0 - 273.15, T_ext - 273.15
    assert T_int_0 >= 273.15 + eps
    assert T_ext >= 273.15 + eps



