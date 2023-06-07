# Unit test for analytical models

import pytest
import numpy as np
import newton


def test_newton():
    """Test newton law of cooling.
    :! /bin/bash ./vim.sh
    """

    # Diffusivity (alpha) params: hA/pCV
    h_c = 1 # W/m2-K
    A = 1 # m2
    p = 1 # kg/m3
    Cp = 1 # specific heat J/kg-K
    Vol = 1 # m3

    # Initial temperatures
    T_int = 100 # C
    T_ext = 23 # C

    # Time params
    dt = 0.1 # s
    t_final = 3600 # s

    # Solve
    T_arr = newton.newton(
        h_c, A, p, Cp, Vol,
        T_int, T_ext,
        dt, t_final
    )

    assert isinstance(T_arr, np.ndarray), type(T_arr)
    assert T_arr.shape == (t_final/dt,), T_arr.shape
    assert T_arr[0] == T_int, T_arr[0]
    assert T_arr[1] < T_int, T_arr[0]
    assert abs(np.min(T_arr) - T_arr[-1]) <= 1e-10





