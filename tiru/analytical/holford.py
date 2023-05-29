# Holford 2007

import numpy as np
import matplotlib.pyplot as plt

"""
Models naturally ventilated space with internal thermal mass in response to
harmonic variation in T_ext. T_int is function of heat balance between
thermal mass (C m = kg J/kgK), and environment via natvent (vol_nv/s = m3/s).

Dynamic:
- When T_ext >= T_int, Cm inversely correlates to T_int (<< Cm leads to >> T_int).
- When << q_int, >> diurnal swing b/c T_int varies from T_ext widely.
- When >> q_int, << diurnal swings b/c loosely follows T_ext. B/c << q_int drives << vol_nv/s. While
  T_int is higher, expect more rapid flushing due to higher temperature delta.





Assumes:
- internal gains small
- internal walls are adiabatic
- no solar gains

Thermally massive buildings

"""

