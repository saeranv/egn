# Unit test for analytical models

import pytest
import numpy as np
import material as mat
import heat as heat


# TODO
# obj: get infrastructure for optimization
# working w/ lumped node
# X- find Cengel example
# X- create test material
# X- material class
# - test time_vec
# - bd plot / vim.sh

def _thermocouple():
    """Test material from Cengel and Ghajar, pg.242.

    Represents thermocouple (temp sensor) junction as 0.5 mm radius there.

    Given:
        radius = 0.0005 # m
        k = 35 # W/m-K
        rho = 8500 # kg/m3
        cp = 230 # J/kg-K
        hc = 210 # W/m2-K
    """
    r = 0.0005 # m
    tc = mat.Material(
        _area = 4.0 * np.pi * (r * r), # m2
        _vol = (4.0 / 3.0) * np.pi * (r * r * r), # m3
        _hc = 210, # W/m2-K
        _k = 35, # W/m-K
        _rho = 8500, # kg/m3
        _cp = 320 # J/kg-K
    )
    return tc


def test_material():
    """Test material class."""

    # Test errors for bad inputs
    tc = _thermocouple()
    with pytest.raises(AssertionError):
        tc.area = 0.0
    with pytest.raises(AssertionError):
        tc.hc = 1e-11

    # Confirm vol, area of sphere is correct
    lc = tc.vol / tc.area
    lc_ = 1.67 * 1e-4 # m
    assert np.abs(lc - lc_) < 1e-4


def test_biot_num():
    """Test derivation of biot coefficient."""

    tc = _thermocouple()
    lc = tc.vol / tc.area
    biot_ = mat.biot_num(tc.hc, lc, tc.k)
    biot = 0.001  # Bi = (h_c * L^2) / k

    assert np.abs(biot - biot_) < 1e-3


def test_time_constant():
    """Test time constant."""

    # Test beta (time constant) pVC / hA
    # vol/area, (hc V)/(kA) already tested, so this tests rho-Cp
    tc = _thermocouple()
    lc = tc.vol / tc.area
    # Test reciprocal b = 1/beta
    b = tc.hc / (tc.rho * lc * tc.cp)   # [1/s]
    b_ = 0.462      # 1/s
    assert np.abs(b - b_) < 1e-2  # slightly less accurate than 1e-3



def test_thermocouple():
    """Solve q 4-1 from Cengel and Ghajar, pg.242.

    Given immersion of there in gas stream with temp Te, calculate time of
    thermocouple to reach 99% of initial temp diff.

    The time (t) equals:
        t = -log(0.99) * beta

    Derivation:
        dT[t] = dT[0] exp[-t/beta t], where dT[t] = Te - T[t]
        dT[t] / dT[0] = (100%-99%) / 100%, since dT[0] is initial temp diff
        log(0.01) = log(exp[-t / beta]) = -t / beta
        t = -log(0.99) / beta
    """
    tc = _thermocouple()

    # Check if Bi <= 0.1 to see if lumped node assumption valid.
    bi = (tc.hc * (tc.vol / tc.area)) / tc.k
    assert bi <= 0.1, bi

    # Test beta (time constant) pVC / hA
    beta = (tc.rho * tc.vol * tc.cp) / (tc.hc * tc.area)  # [s]

    # Test t (answer)
    t = -1 * np.log(0.01) * beta
    t_ = 10 # s
    assert np.abs(t - t_) < 1e-1


def test_diffusivity():
    """Test derivation of thermal diffusivity."""

    tc = _thermocouple()
    # alpha: k / p C
    alpha = mat.diffusivity_coef(tc.k, tc.cp, tc.rho)

    # Derive alpha from b_, Lc given in q 4-1
    b_ = 0.462 # hA/pVC
    lc_ = 1.67 * 1e-4 # ma
    alpha_ = (b_ * lc_ * tc.k) / tc.hc

    assert np.abs(alpha - alpha_) < 1e-3


def test_fourier_number():
    """Test Fourier number."""

    tc = _thermocouple()
    alpha = mat.diffusivity_coef(tc.k, tc.cp, tc.rho)
    t = 1.0 # s
    lc = tc.vol / tc.area
    fo = mat.fourier_num(alpha, lc, t)
    print(alpha, lc, t, alpha / (lc * lc))
    # Derive Fo from 1/beta value givein in q 4-1
    # Fourier: alpha t / L2 = kt/L2pC = t [hA/VpC] = t/beta
    b_ = 0.462 # 1/beta
    fo_ = t * b_
    assert np.abs(fo - fo_) < 1e-3


# def test_lumped_node():
#     """Test mat law of cooling."""

#     # Diffusivity (alpha) params: hA/pCV
#     h_c = 1 # W/m2-K
#     area = 1 # m2
#     rho = 1 # kg/m3
#     C_p = 1 # specific heat J/kg-K
#     vol = 1 # m3

#     # Initial temperatures
#     T0 = 100 # C
#     T_ext = 23 # C

#     # Time params
#     t = 30 # s

#     eps = 1e-10
#     assert T0 > -273.15; assert T_ext > -273.15
#     assert h_c >= eps; assert area >= eps
#     assert C_p >= eps; assert vol >= eps; assert rho >= eps
#     assert t >= eps

#     # Derive dimensionless params
#     char_len = vol / area  # [m]
#     bi = mat.biot_coef(h_c, char_len, k)
#     alpha = mat.diffusivity_coef(k, rho, C_p)
#     fo = mat.fourier_coef(alpha, char_len, dt)

#     # Convert to K, and then dimensionless theta
#     T0 += 273.15; T_ext += 273.15 # K
#     delta_T = np.abs(T0 - T_ext)

#     # theta(t) = T(t) / delta_T: dimensionless temp
#     # T = theta * delta_T
#     theta = heat.lumped_node(bi, fo)
#     T_int = theta * delta_T

#     assert isinstance(T_int, np.ndarray), type(T_int)
#     assert T_int.shape == t, T_int.shape
#     assert T0 > T_ext
#     assert T_int[0] == T0
#     assert T_int[1] < T0
#     assert abs(np.min(T_int) - T_int[-1]) <= 1e-10


# def test_chi_param():
#     """Test chi param."""

#     pass

