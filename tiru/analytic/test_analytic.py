# Unit test for analytical models

import pytest
import numpy as np
import material as mat


def test_biot_coef():
    """Test derivation of biot coefficient."""

    h_c = 1 # W/m2-K
    area = 1 # m2
    vol = 1 # m3
    L = vol / area  # m
    k = 0.1 # W/m-K

    # Bi = (h_c * L^2) / k
    biot = mat.biot_coef(h_c, L, k)
    biot_ = (h_c * L**2) / k
    assert np.abs(biot - biot_) < 1e-10


def test_diffusivity():
    """Test derivation of thermal diffusivity."""

    rho = 1 # kg/m3
    Cp = 1 # specific heat J/kg-K
    k = 0.1 # W/m-K
    # alpha: k / p C
    alpha = mat.diffusivity_coef(k, Cp, rho)
    alpha_ = k / (rho * Cp)
    assert np.abs(alpha - alpha_) < 1e-10


def test_fourier_coef():
    """Test Fourier (time constant) coefficient."""

    rho = 1 # kg/m3
    Cp = 1 # specific heat J/kg-K
    k = 0.1 # W/m-K
    char_len = 0.1  # m
    alpha = mat.diffusivity_coef(k, Cp, rho)
    dt = 0.1 # s
    # Fourier: alpha t / L2 = kt/L2pC
    fo = mat.fourier_coef(alpha, char_len, dt)
    fo_ = (alpha * dt) / (L * L)
    assert np.abs(fo - fo_) < 1e-10



# def test_mat():
    # """Test mat law of cooling."""
#
    # # Diffusivity (alpha) params: hA/pCV
    # h_c = 1 # W/m2-K
    # A = 1 # m2
    # p = 1 # kg/m3
    # Cp = 1 # specific heat J/kg-K
    # Vol = 1 # m3
#
    # # Initial temperatures
    # T_int_0 = 100 # C
    # T_ext = 23 # C
#
    # # Time params
    # dt = 0.1 # s
    # Nt = 3600 # s
#
    # # Solve
    # T_int = mat.mat(
        # h_c, A, p, Cp, Vol,
        # T_int_0, T_ext,
        # dt, Nt
    # )
#
    # assert isinstance(T_int, np.ndarray), type(T_int)
    # assert T_int.shape == (Nt/dt,), T_int.shape
    # assert T_int_0 > T_ext
    # assert T_int[0] == T_int_0
    # assert T_int[1] < T_int_0
    # assert abs(np.min(T_int) - T_int[-1]) <= 1e-10
#
#
