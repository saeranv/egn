"""Heat transfer equations."""

import numpy as np
import material as mat


def ref_lumped_node():
    """Lumped node derivation."""

    return """

    ## LUMPED NODE ASSUMPTIONS
    Assumes node is spatially isothermal (Bi < 0.1), and ambient temperature
    is a constant uniform temperature. Thus no meaningful temperature gradient
    within node, and entire node decays exponentially to ambient temp. The
    energy balance for the lumped node is:
        d(T-T_ext)/dt = (hA/VpC) (T-T_ext) (eqn 0)

    From this temperature can be solved as:
        T(t) = (T(0) - T_ext) exp[(ha/VpC t]  (eqn 1)

    Or in dimensionless form:
        theta(Fo) = exp[Bi Fo] = exp[(hA/VpC) t]

    ## VARIABLES
    ### Diffusivity (alpha) params: hA/pCV
    h_c: Node surface convective coefficient [W/m2-K]
    A: Node surface area [m2]
    p: Node density in [kg/m3]
    Cp: Node specific heat capacity [J/kg-K]
    Vol: Node volume [m3]

    # Initial temperatures
    T_int: Node temperature [C]
    T_ext: Ambient temperature [C]

    # Time params
    t: time at n, or array of times [s]

    ## DERIVATION OF EQN 1
    ## T(t) = (T(0) - T_ext) exp[(ha/VpC t]
    Derivation follows from an energy balance for the lumped node,
    Eqn 1.
        d(T-T_ext)/dt = (hA/VpC) (T-T_ext),
    ;then set T-T_ext) as DT, reveals DT(t) as exp function since dDT/dt ~ DT,
        dDT/dt = (hA/VpC) DT, thus
        DT(t) = DT(0) exp[(hA/VpC) t],
        dDT/dt = (hA/VpC) DT0 exp[(hA/VpC) t].
    ;To get original eqn we can simplify (hA/VpC) as b, and expand DT,
        b = hA/VpC; the time constant [s^-1] (Cengel, p.239)
        DT(t) = DT(0) exp(b t),
        (T(t) - T_ext) = (T(0) - T_ext) exp(b t),
    ;resulting in original eqn:
        T(t) = (T(0) - T_ext) exp(b t) + T_ext.

    ## DERIVATION OF EQN 2
    ## theta(tau) = exp(Bi Fo) = exp(t hA/VpC)
    Simplify to 4 dimensionless params:
    theta, tau, Bi, so we can rewrite
       T(t)-T_ext = T0 exp(b t)
       dT/dt = b T(t),
    as:
       theta(tau) = exp(Bi tau)
       d_theta/d_tau = Bi theta(tau).

    Eqn 2.
    Convert to dimensionless form by defining:
        theta = (T - T_ext) / (T0 - T_ext)
        Lc = V_mass / A_srf; characteristic length [m]
        a = k/pC; thermal diffusivity
        Bi = h-Lc/k; since R = L/k can intuit Bi = hR
        Fo = a-t/L2 = kt/L2pC
    Note how Bi Fo can be rewritten as beta t:
        Bi Fo = hLc/k kt/L2pC = h/LpC t
              = hA/VpC t; since A/V = L
    Thus:
    theta(t) = exp(Bi Fo) = exp(hA/VpC t)
    """

def lumped_node(bi:float, fo:float):
    """Dimensionless transient lumped node eqn.

    Solves for theta given Bi and tau,
        theta(tau) = exp(Bi tau)

    Args:
        Bi: Biot number = h-Lc / k [-]
        tau: dimensionless time = a t / Lc2 [-]

    Returns dimensionless temp, theta = (T - T_ext) / (T0 - T_ext) [-]
    """
    # T =  (theta * (T0 - T_ext)) + T_ext)
    return np.exp(bi * fo)


def main(
    h_c, area,      # surface params
    k, rho, C_p, vol,  # mass params
    T0, T_ext,   # initial and external temps
    t # time
    ):
    """Predict array of temperatures for lumped node given parameters."""

    eps = 1e-10
    assert T0 > -273.15; assert T_ext > -273.15
    assert h_c >= eps; assert area >= eps
    assert C_p >= eps; assert vol >= eps; assert p >= eps
    assert isinstance(tn, int);  assert tn >= eps; assert dt > eps

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
    theta = lumped_node(bi, fo)
    return theta * delta_T





