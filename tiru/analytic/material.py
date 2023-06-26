from dataclasses import dataclass
from typing import Union
import numpy as np
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
    # Surface heat transfer params
    hc: ndfloat
    area: ndfloat
    # Body heat transfer params
    vol: ndfloat
    k: ndfloat
    rho: ndfloat
    cp: ndfloat
    # Temp
    theta: ndfloat
    temp: ndfloat


def diffusivity_coef(k:ndfloat, rho:ndfloat, c_p:ndfloat) -> ndfloat:
    """diffusivity coefficient alpha = k / rho-c [m2/s].

    units k / rho-c
        = w/m-k / kg/m3-j/kg-k
        = m2/s

    args:
        k: conductivity [w/m-k]
        rho: density [kg/m3]
        c_p: specific heat capacity at constant pressure [j/kg-k]

    returns diffusivity coefficient [m2/s].
    """
    return k / (rho * c_p)


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


def biot_num(h_c:ndfloat, char_len:ndfloat, k:ndfloat) -> ndfloat:
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


def tau(delta_time:ndfloat, t:ndfloat)->ndfloat:
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


