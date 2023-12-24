# Unit test for analytical models
import numpy as np
import material as mat
import heat as heat

# utility fns to wrap scalars as arrays
# TODO: might be good to find this from Rust
# typedef uint8_t   u8;
# typedef int32_t   b32;
# typedef int32_t   i32;
# typedef uint32_t  u32;
# typedef uint64_t  u64;
i8 = (lambda x: np.int8([x]))
i32 = (lambda x: np.int32([x]))
f64 = (lambda x: np.float64([x]))


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
        area = f64(4.0 * np.pi * (r * r)), # m2
        vol = f64((4.0 / 3.0) * np.pi * (r * r * r)), # m3
        hc = f64(210) , # W/m2-K
        k = f64(35) , # W/m-K
        rho = f64(8500), # kg/m3
        cp = f64(320) # J/kg-K
    )
    return tc


def test_material():
    """Test material class."""

    # Test errors for bad inputs
    tc = _thermocouple()

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
    nt = 1.0 # s
    lc = tc.vol / tc.area
    fo = mat.fourier_num(alpha, lc, nt)

    # Derive Fo from 1/beta value givein in q 4-1
    # t/beta = Fo Bi
    # Fo = t/(beta Bi)
    beta_ = 1.0/0.462 # given beta
    bi_ = 0.001       # given biot
    fo_ = nt / (beta_ * bi_)

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

    # Test time to get to 1C manually
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
    temp_0 = f64(100.0)
    temp_ext = f64(0.0)
    nt = np.arange(0, 11) # 0-10 seconds in 11 steps (time at T[t])
    alpha = mat.diffusivity_coef(tc.k, tc.rho, tc.cp)
    fo = mat.fourier_num(alpha, lc, nt)
    # so at 99%, T_int ~ 1C

    # Get theta, dimensionless temp
    theta = heat.lumped_node(bi, fo)
    assert theta.shape == nt.shape
    assert np.abs(theta[0] - 1.0) < 1e-10
    assert np.abs(theta[-1] - 0.0) < 1e-2
    # theta(fo) = (T[t]-Te) / (T[0]-Te)
    # theta * (T[0]-Te) = T[t] - Te
    # T[t] = [theta * (T[0]-Te)] + Te
    dT = (temp_0 - temp_ext)
    temps = (theta * dT) + temp_ext
    assert abs(temps[0] -  temp_0) < 1e-3
    # after 10s = 99% of temp diff achieved = T[10]=1C
    assert abs(temps[10] - 1.0) < 1e-1


def test_numeric():
    """Numeric lumped node.

    dtheta = (theta_eps - theta_i)
    eps d(theta)/d(phi) = \
        1/chi (theta|x1 - theta|xi) + eps Rn dtheta |dtheta|^0.5
    """

    nt = np.arange(11)
    dnt = nt[-1] - nt[0]
    tau = mat.tau(dnt, nt)
    Te = np.sin(np.pi * 2) * 30.0
    T = 23.0

    # Materials
    mass = _thermocouple()
    iair = _thermocouple()

    #
    mass_lc = mass.vol / mass.area
    mass_alpha = mat.diffusivity_coef(mass.k, mass.rho, mass.cp)
    mass_fo = mat.fourier_num(mass_alpha, mass_lc, nt)
    mass_bi = mat.biot_num(mass.hc, mass_lc, mass.k)
    mass_beta = (mass.rho * mass.vol * mass.cp) / (mass.hc * mass.area)  # [s]

    # Time-scale factors
    # 1. chi ξ - ratio of convection to forcing time scale.
    # indicates whether there is time for significant heat to be transferred
    # to thermal mass before environmental temperature changes (forcing).
    chi = mat.time_scale_chi(tau, mass_fo, mass_bi)

    # 2. epsilon ε, Cp of interior air to Cp of thermal mass.
    eps = mat.time_scale_epsilon(
        iair.vol, iair.rho, iair.rho,
        mass.area, mass_lc, mass.rho, mass.cp)

    # 3. Rn, ratio of forcing to ventilation flushing time.
    area_vent = 1 # m^2
    neutral_height = 1.5
    dTi = Te[0] - T # ??
    # TODO: check beta
    Rn = mat.time_scale_Rn(area_vent, mass_beta, neutral_height, dTi)

    # 4. 2η^2, ratio of mass diffusion to forcing time scale.
    dnusq = mat.time_scale_nu(tau, mass_fo)

    dT = np.abs(T[0] - Te)
    theta = T / (dT - Te)
    # theta(t) = T(t) / delta_T: dimensionless temp
    # dtheta = (theta_eps - theta_i)
    # eps d(theta)/d(phi) = \
    #     1/chi (theta_m|x1 - theta_z|xi) + eps Rn dtheta_? |dtheta_?|^0.5

    # eps d(theta)/d(phi) = \
    #     1/chi (theta_m|x1 - theta_z|xi) + eps Rn dtheta_? |dtheta_?|^0.5



