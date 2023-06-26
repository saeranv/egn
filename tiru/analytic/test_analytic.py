# Unit test for analytical models

import pytest
import numpy as np
import material as mat
import heat as heat


# TODO
# obj: get infrastructure for optimization working w/ lumped node
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

    # Derive Fo from 1/beta value givein in q 4-1
    # t/beta = Fo Bi
    # Fo = t/(beta Bi)
    beta_ = 1.0/0.462 # given beta
    bi_ = 0.001       # given biot
    fo_ = t / (beta_ * bi_)

    # lose lots of precision w/ Cengel's vals
    assert np.abs(fo - fo_) < 1.5


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
    lc = tc.vol / tc.area
    # Check if Bi <= 0.1 to see if lumped node assumption valid.
    bi = (tc.hc * (tc.vol / tc.area)) / tc.k
    assert bi <= 0.1, bi

    # Test beta (time constant) pVC / hA
    beta = (tc.rho * tc.vol * tc.cp) / (tc.hc * tc.area)  # [s]

    # Test t (answer)
    t = -1 * np.log(0.01) * beta
    t_ = 10 # s
    assert np.abs(t - t_) < 1e-1


    # Test same problem w/ heat class

    # Initial temperatures
    _temp_0 = 100.0
    _temp_ext = 0.0
    temp_0 = _temp_0 + 273.15 # K
    temp_ext = _temp_ext + 273.15 # K
    t = np.arange(0, 11) # 0-10 seconds in 11 steps (time at T[t])
    alpha = mat.diffusivity_coef(tc.k, tc.rho, tc.cp)
    fo = mat.fourier_num(alpha, lc, t)
    # so at 99%, T_int ~ 1C

    # Convert temps to dimensionless theta
    # TODO: confirm if theta should input
    # Fo=alpha-t / Lc2, then alphaT/Lc2
    # theta(fo) = (T[t]-Te) / (T[0]-Te) (alpha / Lc2)
    #           = (T[t]-Te)-alpha / (T[0]-Te)-Lc2
    # T[t] = [(theta * (T[0]-Te) * Lc2) / alpha] + Te
    sc = ((temp_0 - temp_ext) * (lc * lc)) / alpha

    theta = heat.lumped_node(bi, fo)
    print(theta.round(2))
    assert theta.shape == t.shape
    assert abs(theta[0] - 1.0) < 1e-10
    assert abs(theta[-1] - 0.0) < 1e-2

    temp = ((theta * sc) - temp_ext) - 273.15

    print(temp.round(7))
    assert temp[0] > _temp_ext
    assert np.abs(temp[0] - _temp_0) < 1e-3
    # assert temp[1] < temp_0
    # assert abs(np.min(temp) - temp[-1]) <= 1e-10



