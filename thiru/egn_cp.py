#!/usr/bin/env python
# egn/egn.py
from __future__ import annotations
import sys
import typing as typ


# Load dfut
dfutil_fpath = '/mnt/c/users/admin/master/thermal-mass'
sys.path.append(dfutil_fpath)
from thermal_mass import df_utils as dfut


ppd = dfut.ppdir
csrf, cspc = dfut.COL_SRF, dfut.COL_SPC


def proto(*args, **kwargs) -> None:
    """For prototyping code."""
    return dfut._proto(*args, **kwargs)


# TODO: Delete
def make_eval_fn(fn_str: str | None) -> typ.Callable:
    """Make function from string."""
    return eval('lambda ' + fn_str) if fn_str else (lambda x: x)


def make_df(osm_fpath: str) -> pd.DataFrame:
    """Make srf df from osm text stream."""

    _b = dfut.b_make(osm_fpath)
    srf = dfut.b_make_df(_b, csrf + cspc)

    return srf

