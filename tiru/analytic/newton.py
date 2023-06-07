# Newton's law of cooling.
import numpy as np
import matplotlib.pyplot as plt


def newton(
    h_c, A, Cp, Vol, p,
    T_int_0, T_ext,
    dt, Nt
    ) -> np.ndarray:
    """Predict array of temperatures for node given parameters.

    1. Derivation of T(t) = (T0 - T_ext) exp(a t) + T_ext
    Newton's law states that temperature rate of lumped node decreases in
    proportion to difference of ambient temperature.
        dT/dt = K T - T_ext; where K is some constant of proportionality
        y(t) = T(t) - T_ext
        ; Simplify spatial diff as y
        dy  = dT = (T_1 - T_ext) - (T_0 - T_ext)
        dy/dt = K y.
        ; As exponential fn
        y(t) = C exp(a t)
        dy/dt = a C exp(a t); where C = y(0) = C exp(a 0)
        ; Substitute back original variables:
        T(t) - T_ext = C exp(a t), b/c y(t) = T(t) - T_ext
        T(t) = (T(0) - T_ext) exp(a t) + T_ext

    2. Derivation of a, diffusivity coefficient.


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
    T_int_0,  T_ext = T_int_0 + 273.15, T_ext + 273.15
    assert h_c >= eps
    assert A >= eps
    assert Cp >= eps
    assert Vol >= eps
    assert p >= eps
    assert dt >= eps
    assert Nt >= dt
    assert T_int_0 >= eps
    assert T_ext >= eps

    t_steps = int(Nt / dt)
    T_arr = np.zeros(t_steps, dtype=np.float64)


    return T_arr

