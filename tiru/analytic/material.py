import numpy as np
from dataclasses import dataclass

@dataclass
class Material:
    """Attributes for material properties.

    Args:
        area: float  # [m2] surface area
        vol: float   # [m3] volume

        # Surface heat transfer params
        hc: float    # [W/m2-K] convective coefficient

        # Body heat transfer params
        k: float     # [W/m-K] thermal conductivity
        rho: float   # [kg/m3] density
        cp: float    # [J/kg-K] specific heat capacity
                     # at constant pressure

    These combine to form:
        pVC / hA            [s] beta (time constant)
        k / pC              [m2/s] alpha (diffusivity)
        h-Lc / k = h / U    [-] Bi (Biot number)
        alpha-t / L2        [-] Fo (fourier number)

    (T[t] - Te) = (T[0] - Te) exp[Bi Fo(t)] = beta t

    Biot number represents ratio of convection at surface to
    conduction within body
    """

    # Geometry
    area: float  # [m2] surface area
    vol: float   # [m3] volume

    # Surface heat transfer params
    hc: float    # [W/m2-K] convective coefficient

    # Body heat transfer params
    k: float     # [W/m-K] thermal conductivity
    rho: float   # [kg/m3] density
    cp: float    # [J/kg-K] specific heat capacity
                 # at constant pressure



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
    assert k >= 1e-10    # not adiabatic
    assert rho >= 1e-10  # must have density
    assert C_p >= 1e-10  # must have heat capacity

    return k / (rho * C_p)


def fourier_coef(alpha:float, char_len:float, dt:float) -> float:
    """Dimensionless fourier coefficient (alpha-dt / L2) [-].

    Units dt-alpha / L2
        = s-alpha / m2
        = s-(m2/s) / L2,    alpha units is m2/s
        = - / -

    Args:
        alpha: diffusivity coefficient [m2/s]
        char_len: characteristic length [m]
        dt: time step [s]

    Returns Fourier coefficient.
    """
    assert alpha >= 1e-10  # k > 0 so (k / rho-C) > 0
    assert char_len >= 1e-10  # must have thickness
    assert dt >= 1e-10  # must have timestep

    return (alpha * dt) / (char_len * char_len)


def biot_coef(h_c:float, char_len:float, k:float) -> float:
    """Dimensionless Biot coefficient (h-Lc / k) [-].

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
    """Time scale tau, dimensionless time from Holford.
    """
    return t / delta_time


def time_scale_nu(tau, Fo):
    """Time scale 2-nu^2, ratio of mass diffusion to forcing time scale.

    nu = Lc / Sigma
    Sigma = sqrt(2-alpha / w)  # effective penetration depth where temp varies
    """

    two_nu_sq = tau / Fo  # 2n^2
    return np.sqrt(two_nu_sq / 2.0)

two_nu_sq
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



