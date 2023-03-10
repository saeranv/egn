# pSDF tests

import numpy as np
from thiru import psdf


def _tocol(pt):
    return np.array(pt)[:, np.newaxis]

def test_point_sdf():
    """Test SDF of point.

    Given point (0, 0), SDF should evaluate to 1 at (0, 0), and
    0 elsewhere.
    """
    pt = np.array([[0], [0]])
    pt_sdf = psdf.point_sdf(pt)

    eval_pt = _tocol([0, 0])
    sdf = pt_sdf(eval_pt)
    assert np.abs(sdf - 1.0) < 1e-6, sdf
    eval_pt = _tocol([0.5, 0])
    sdf = pt_sdf(eval_pt)
    assert np.abs(sdf - 0.0) < 1e-6, sdf


