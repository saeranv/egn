"""notebook on lumped node optimization."""

import numpy as np
import matplotlib.pyplot as plt

# tiru libs
import material as mat
import heat
import vlt.plot as vlt

"""
# GTD-DEFINE
# obj: define problem, independant params to opt
- prob = p(Z | V,A)
- Define Lc, A ranges
- make, V=LcA, make meshgrid [V, A]
    - subplot(1,3) = Lc, V,A

# GTD-JOINT-MATRIX
# obj: check useful hidden vars
- Define mat=from EP_ref/Holford?
- Plot/propogate: Bi, 1/beta, make images (save images)
    - subplots(2,3) = Bi>0.01, 1/Beta>0.01, nan

# GTD-COST
# obj: define cost fn, determines params
- Create T function (1 hour)
 - plt.T vs t
- Z(v,a) = |T(v,a) <= Tcomf|
    - subplots(2,3) nan=Z
- plt.T vs t for argmax_(v,a)(Z(v,a))
"""


def main():





if __name__ == "__main__":
    main()
