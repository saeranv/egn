import numpy as np

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

