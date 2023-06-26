"""notebook on lumped node optimization."""

import numpy as np
import matplotlib.pyplot as plt

# tiru libs
import material as mat
import heat
import vlt.plot as vlt

"""
# GTD-SEARCH
# obj: viz biot, 1/beta
- Define Lc, A ranges
- make, V=LcA, make meshgrid [V, A]
    - subplot(1,3) = Lc, V,A
- Define mat=from EP_ref/Holford?
- Plot/propogate: Bi, 1/beta, make images (save images)
    - subplots(2,3) = Bi>0.01, 1/Beta>0.01, nan

# GTD-COST
# obj: define cost fn
- Create T function (1 hour)
 - plt.T vs t
- Z = |T <= Tcomf|
    - subplots(2,3) nan=Z
"""


def main():





if __name__ == "__main__":
    main()
