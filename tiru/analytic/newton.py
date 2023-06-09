# Newton's law of cooling.
import numpy as np
import matplotlib.pyplot as plt


def newton(
    h_c, A, Cp, Vol, p,
    T0, T_ext,
    dt, Nt
    ) -> np.ndarray:
    """Predict array of temperatures for lumped node given parameters.

    Assumes node is spatially isothermal (Bi < 0.1), and ambient temperature
    is a constant uniform temperature. Thus no meaningful temperature gradient
    within node, and entire node decays exponentially to ambient temp,
    according to,
        T(t) = (T0 - T_ext) exp(b t) + T_ext.

    Derivation follows from an energy balance for the lumped node,
        d(T-T_ext)/dt = (hA/VpC) (T-T_ext),
    then set T-T_ext) as DT, reveals DT(t) as exp function since dDT/dt ~ DT,
        dDT/dt = (hA/VpC) DT, thus
        DT(t) = DT(0) exp[(hA/VpC) t],
        dDT/dt = (hA/VpC) DT0 exp[(hA/VpC) t].
    To get original eqn we can simplify (hA/VpC) as b, and expand DT,
        b = hA/VpC; the time constant [s^-1] (Cengel, p.239)
        DT(t) = DT(0) exp(b t),
        (T(t) - T_ext) = (T(0) - T_ext) exp(b t),
    resulting in original eqn:
        T(t) = (T(0) - T_ext) exp(b t) + T_ext.

    Args:
        # Diffusivity (alpha) params: hA/pCV
        h_c: Node surface convective coefficient [W/m2-K]
        A: Node surface area [m2]
        p: Node density in [kg/m3]
        Cp: Node specific heat capacity [J/kg-K]
        Vol: Node volume [m3]

        # Initial temperatures
        T_int: Node temperature [C]
        T_ext: Ambient temperature [C]

        # Time params
        dt: time step [s]
        Nt: total time elapsed [s]

    Returns (Nt/dt) array of temperatures.
    """

    # TODO: clarify Cp against Cv
    # Rough check of physically possible
    eps = 1e-10
    T0,  T_ext = T0 + 273.15, T_ext + 273.15
    assert h_c >= eps
    assert A >= eps
    assert Cp >= eps
    assert Vol >= eps
    assert p >= eps
    assert dt >= eps
    assert Nt >= dt
    assert T0 >= eps
    assert T_ext >= eps

    t_steps = int(Nt / dt)
    T = np.zeros(t_steps, dtype=np.float64)

    # Simplify to dimensionless params: Fo/tau, Bi, theta so we can rewrite
    #    T(t)-T_ext = T0 exp(b t)
    #    dT/dt = b T(t),
    # as:
    #    theta(tau) = exp(Bi tau)
    #    d_theta/d_tau = Bi theta(tau).
    # Derivation:
    #     _Lc = V_mass / A_srf; characteristic length [m]
    #     _a = k/pC; thermal diffusivity
    #     Bi = h_Lc/k; since R = L/k can intuit Bi = hR
    #     tau = _at/L2 = kt/L2pC
    #     theta = (T - T_ext) / (T0 - T_ext)


    # Note tau Bi equals exponent coefficient:
    # Bi tau = hLc/k kt/L2pC = h/LpC t
    #        = (hA/VpC) t; since A/V = L

    k, L = 1, 1
    _a = k / p * Cp  # k/pC
    t_to_tau = lambda t: (_a * t) / (L*L)
    theta = lambda tau: (T[tau_to_t(tau)] - T_ext) / (T0 - T_ext)


    return T

