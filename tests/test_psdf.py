# pSDF tests

import numpy as np
from thiru import psdf


def _vec(*args):
    return np.array(args)[:, np.newaxis]

def test_point_sdf():
    """Test SDF of point.

    Given point (0, 0), SDF should evaluate to 1 at (0, 0), and
    0 elsewhere.
    """
    # Base case at origin
    pt_sdf = psdf.point_sdf(_vec(0, 0))

    eval_pt = _vec(0, 0)
    sdf = pt_sdf(eval_pt)
    assert np.abs(sdf - 0.0) < 1e-6, sdf
    eval_pt = _vec(1, 0)
    sdf = pt_sdf(eval_pt)
    assert np.abs(sdf - 1.0) < 1e-6, sdf

    # Off origin
    pt_sdf = psdf.point_sdf(_vec(-1.0, -1.0))

    eval_pt = _vec(0, 0)
    sdf = pt_sdf(eval_pt)
    _hypot = np.sqrt(2)
    assert np.abs(sdf - _hypot) < 1e-6, sdf
    eval_pt = _vec(-1, 0)
    sdf = pt_sdf(eval_pt)
    assert np.abs(sdf - 1.0) < 1e-6, sdf


