# Unit test for analytical models

import pytest
import numpy as np
import newton


def test_newton():
    """Test newton law of cooling."""

    # Diffusivity (alpha) params: hA/pCV
    h_c = 1 # W/m2-K
    A = 1 # m2
    p = 1 # kg/m3
    Cp = 1 # specific heat J/kg-K
    Vol = 1 # m3

    # Initial temperatures
    T_int_0 = 100 # C
    T_ext = 23 # C

    # Time params
    dt = 0.1 # s
    Nt = 3600 # s

    # Solve
    T_int = newton.newton(
        h_c, A, p, Cp, Vol,
        T_int_0, T_ext,
        dt, Nt
    )

    assert isinstance(T_int, np.ndarray), type(T_int)
    assert T_int.shape == (Nt/dt,), T_int.shape
    assert T_int_0 > T_ext
    assert T_int[0] == T_int_0
    assert T_int[1] < T_int_0
    assert abs(np.min(T_int) - T_int[-1]) <= 1e-10


