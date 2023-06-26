# Unit test for analytical models

import pytest
import numpy as np
import material as mat
import heat as heat


# TODO
# obj: get infrastructure for optimization
# working w/ lumped node
# X- find Cengel example
# - create test material
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
        _cp = 230 # J/kg-K
    )
    return tc


def test_thermocouple():
    """Solve q 4-1 from Cengel and Ghajar, pg.242.

    Given immersion of there in gas stream with temp Te, calculate time of
    thermocouple to reach 99% of initial temp diff.

    The time (t) equals:
        t = -log(0.99) / beta

    Derivation:
        dT[t] = dT[0] exp[-beta t], dT[t] = Te - T[t]
        dT[t] / dT[0] = (100%-99%) / 100%, since dT[0] is initial temp diff
        log(0.01) = log(exp[-beta t]) = -beta t
        t = -log(0.99) / beta
    """
    # Should check if Bi <= 0.1 to see if lumped node assumption valid.

    # Calculate beta (time constant) pVC / hA
    tc = _thermocouple()
    beta = mat.time_constant(
        tc.area, tc.vol, tc.hc, tc.rho, tc.cp)

    t = -np.log(0.01) / beta
    t_ = 10.0 # s
    print(t)
    assert np.abs(t - t_) < 1e-5


def test_material():
    """Test material class."""

    # Test tolerance error
    mat_ = mat.Material(1, 1, 1, 1, 1, 1)
    with pytest.raises(AssertionError):
        mat_.area = 0.0
    with pytest.raises(AssertionError):
        mat_.hc = 1e-11


def test_diffusivity():
    """Test derivation of thermal diffusivity."""

    rho = 1 # kg/m3
    Cp = 1 # specific heat J/kg-K
    k = 0.1 # W/m-K
    # alpha: k / p C
    alpha = mat.diffusivity_coef(k, Cp, rho)
    alpha_ = k / (rho * Cp)
    assert np.abs(alpha - alpha_) < 1e-10


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
    fo_ = (alpha * dt) / (char_len * char_len)
    assert np.abs(fo - fo_) < 1e-10


def test_lumped_node():
    """Test mat law of cooling."""

    # Diffusivity (alpha) params: hA/pCV
    h_c = 1 # W/m2-K
    area = 1 # m2
    rho = 1 # kg/m3
    C_p = 1 # specific heat J/kg-K
    vol = 1 # m3

    # Initial temperatures
    T0 = 100 # C
    T_ext = 23 # C

    # Time params
    t = 30 # s

    eps = 1e-10
    assert T0 > -273.15; assert T_ext > -273.15
    assert h_c >= eps; assert area >= eps
    assert C_p >= eps; assert vol >= eps; assert rho >= eps
    assert t >= eps

    # Derive dimensionless params
    char_len = vol / area  # [m]
    bi = mat.biot_coef(h_c, char_len, k)
    alpha = mat.diffusivity_coef(k, rho, C_p)
    fo = mat.fourier_coef(alpha, char_len, dt)

    # Convert to K, and then dimensionless theta
    T0 += 273.15; T_ext += 273.15 # K
    delta_T = np.abs(T0 - T_ext)

    # theta(t) = T(t) / delta_T: dimensionless temp
    # T = theta * delta_T
    theta = heat.lumped_node(bi, fo)
    T_int = theta * delta_T

    assert isinstance(T_int, np.ndarray), type(T_int)
    assert T_int.shape == t, T_int.shape
    assert T0 > T_ext
    assert T_int[0] == T0
    assert T_int[1] < T0
    assert abs(np.min(T_int) - T_int[-1]) <= 1e-10


    def test_chi_param():
        """Test chi param."""

        pass

