import numpy as np
from dataclasses import dataclass

from typing import Union
from numpy.typing import NDArray

ndfloat = Union[NDArray[np.float64], float]



@dataclass
class Material:
    """Attributes for material properties A, hc, k, V, p, Cp.

    These combine to form:
        pVC / hA            beta (time constant) [s]
        k / pC              alpha (diffusivity) [m2/s]
        h-Lc / k = h / U    Bi (Biot number) [-]
        alpha-t / L2        Fo (Fourier number) [-]

    Given dT[t] = T[t] - Te, we can express a lumped node dT[t] as:
        dT[t]/dT[0] = exp[Bi Fo(t)] = exp[t/beta]

    Args:
        area: float  # [m2] surface area
        vol: float   # [m3] volume
        hc: float    # [W/m2-K] convective coefficient
        k: float     # [W/m-K] thermal conductivity
        rho: float   # [kg/m3] density
        cp: float    # [J/kg-K] specific heat capacity at constant pressure

    """
    # Constants
    _EPS = 1e-10  # [-] zero tolerance epsilon

    # Geometry
    _area: float
    _vol: float   # [m3] volume

    # Surface heat transfer params
    _hc: float    # [W/m2-K] convective coefficient

    # Body heat transfer params
    _k: float     # [W/m-K] thermal conductivity
    _rho: float   # [kg/m3] density
    _cp: float    # [J/kg-K] specific heat capacity
                 # at constant pressure

    @property
    def area(self):
        """Surface area in [m2]"""
        return self._area

    @area.setter
    def area(self, area):
        assert area >= self._EPS, f"Area must be positive, got {area}."
        self._area = float(area)

    @property
    def vol(self):
        """Volume in [m3]"""
        return self._vol

    @vol.setter
    def vol(self, vol):
        assert vol >= self._EPS, f"Volume must be positive, got {vol}."
        self._vol = float(vol)

    @property
    def hc(self):
        """Surface convective coefficient in [W/m2-K]"""
        return self._hc

    @hc.setter
    def hc(self, hc):
        assert hc >= self._EPS, "Convectivity can't be adiabatic, got hc {hc}."
        self._hc = float(hc)

    @property
    def k(self):
        """Body conductive coefficient in [W/m-K]"""
        return self._k

    @k.setter
    def k(self, k):
        assert k >= self._EPS, f"Conductivity can't be adiabatic, got {k}."
        self._k = float(k)

    @property
    def rho(self):
        """Density in [kg/m3]."""
        return self._rho

    @rho.setter
    def rho(self, rho):
        assert rho >= self._EPS, f"Density must be positive, got {rho}."
        self._rho = float(rho)

    @property
    def cp(self):
        """Specific heat capacity at constant pressure in [J/kg-K]"""
        return self._cp

    @cp.setter
    def cp(self, cp):
        assert cp >= self._EPS, "Heat capacity must be positive, got {cp}."
        self._cp = float(cp)


def diffusivity_coef(k:float, rho:float, C_p:float) -> float:
    """Diffusivity coefficient alpha = k / rho-C [m2/s].

    Units k / rho-C
        = W/m-K / kg/m3-J/kg-K
        = m2/s

    Args:
        k: conductivity [W/m-K]
        rho: density [kg/m3]
        C_p: specific heat capacity at constant pressure [J/kg-K]

    Returns diffusivity coefficient [m2/s].
    """
    return k / (rho * C_p)


def time_constant(rho, vol, cp, hc, area):
    """Time constant (beta) for lumped node = pVC / hA [s].

    The reciprocal the time constant (beta) is the constant
    in the exponential function representing a lumped node
    system:
        dT[t]/dT[0] = exp[t/beta].

    Units rho-V-C / hc-A
        = kg-(J/kg-K) / [W/K]
        = J/K / J/K-s
        = 1/s

    Args:
        area: float  # [m2] surface area
        vol: float   # [m3] volume
        hc: float    # [W/m2-K] convective coefficient
        rho: float   # [kg/m3] density
        cp: float    # [J/kg-K] specific heat capacity at constant pressure

    Returns time constant.
    """
    return (rho * vol * cp) / (hc * area)



def fourier_num(alpha:ndfloat, char_len:ndfloat, nt:ndfloat) -> ndfloat:
    """Dimensionless fourier number (alpha-dt / L2) [-].

    Units dt-alpha / L2
        = s-alpha / m2
        = s-(m2/s) / L2,    alpha units is m2/s
        = - / -

    Args:
        alpha: diffusivity coefficient [m2/s]
        char_len: characteristic length [m]
        nt: elapsed time [s]

    Returns Fourier coefficient.
    """
    return (alpha * nt) / (char_len * char_len)


def biot_num(h_c:float, char_len:float, k:float) -> float:
    """Dimensionless Biot number (h-Lc / k) [-].

    Biot number represents ratio of convection at surface to
    conduction within body:
        hc / U

    In a lumped node system, the body must have a uniform distribution of
    temperature, which occurs when conductance is very high relative to
    convection. Thus a lumped node system is typically considered valid
    the Bi <= 0.1.


    Units h_c-Lc / k
        = m-(W/m2-K) / (W/m-K)
        = W/m-K / W/m-K
        = - / -

    Args:
        h_c: Convective coefficient [W/m2-K]
        char_len: Characteristic length [m]
        k: Conductivity [W/m-K]

    Returns Biot coefficient.
    """
    assert h_c >- 1e-10  # not adiabatic
    assert char_len >= 1e-10  # must have thickness
    assert k >= 1e-10  # must have Conductivity

    return (h_c * char_len) / k


def tau(delta_time, t):
    """Time scale tau, dimensionless time from Holford."""
    return t / delta_time


def time_scale_nu(tau, Fo):
    """Time scale 2-nu^2, ratio of mass diffusion to forcing time scale.

    nu = Lc / Sigma
    Sigma = sqrt(2-alpha / w)  # effective penetration depth where temp varies
    """

    nu_ = tau / Fo  # 2n^2
    return np.sqrt(nu_ / 2.0)  # nu


def time_scale_chi(tau, Fo, Bi):
    """Time scale chi - ratio of convection to forcing time scale.

    Indicates whether there is time for significant heat to be transferred
    to thermal mass before environmental temperature changes (forcing).
    """

    return tau / Fo-Bi


def time_scale_Rn(area_vent, beta, neutral_height, delta_temp):
    """Time scale Rn, ratio of forcing to ventilation flushing time."""

    G = 9.81  # gravity
    Rn = area_vent * np.sqrt(beta * G * neutral_height * delta_temp)
    return Rn

def time_scale_epsilon(vol_z, rho_z, c_pz, area_m, char_len_m, rho_m, c_m):
    """Time scale epsilon, Cp of interior air to Cp of thermal mass.

    rho = density [kg/m3]
    C_p = specific heat capacity at constant pressure [J/kg-K]
    V_z-rho_z-C_z / V_m-rho_m-C_m
    = kg_z-C_z / kg_m-C_m = K / K

    """
    return (vol_z, rho_z, c_pz) / (area_m * char_len_m * rho_m * c_m)


def main():

    # theta_z - theta_ext
    epl



