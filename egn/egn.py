#!/usr/bin/env python
# egn/egn.py
from __future__ import annotations
import sys
import typing as typ

from io import BytesIO, StringIO
from argparse import ArgumentParser
# import numpy as np
import pandas as pd

# Load dfut
dfutil_fpath = '/mnt/c/users/admin/master/thermal-mass'
sys.path.append(dfutil_fpath)
from thermal_mass import df_utils as dfut

ppd = dfut.ppdir
csrf, cspc = dfut.COL_SRF, dfut.COL_SPC


def write_binary(df: pd.DataFrame) -> None:
    """Write feather binary stream to stdout."""

    with sys.stdout as stdout:
        df.to_feather(stdout.buffer)
        stdout.buffer.flush()


def write_text(text_arr:Sequence) -> None:
    """Write text to stdout."""

    if isinstance(text_arr, str):
        text_arr = [text_arr]

    with sys.stdout as stdout:
        for text in text_arr:
            stdout.write(text)
        stdout.buffer.flush()


def read_text() -> str:
    """Create in-memory text buffer from stdin stream."""
    # read_stream_txt: read(pipe=sys.stdin)         # retursn StringIO
    # read_stream_bin: read(pipe=sys.stdin.buffer)  # returns BytesIO

    # Create in-memory text buffer to collect binary stream.
    text_file = StringIO()

    with sys.stdin as stdin:
        while True:
            chunk = stdin.readline()
            if chunk == '':
                break
            # Move "write" postion to end of stream
            # with seek, else write will overwrite
            text_file.write(chunk)

    text_str = text_file.getvalue()
    return text_str

def read_binary() -> pd.DataFrame:
    """Read feather binary stream from stdin."""

    # Create in-memory binary buffer to collect binary stream.
    byte_file = BytesIO()

    with sys.stdin as stdin:
        while True:
            chunk = stdin.buffer.read()
            if chunk == b'':
                break
            # Move "write" postion to end of stream
            # with seek, else write will overwrite
            byte_file.seek(0, 2)
            byte_file.write(chunk)

    # TODO move this to read_feather()
    df = pd.read_feather(byte_file)
    return df

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


if __name__ == '__main__':

    # Set args
    parser = ArgumentParser(
        prog='egn', description='parser')
    parser.add_argument('fns', type=str)
    parser.add_argument('-f', '--fn_str', nargs=1, type=str, default='')
    parser.add_argument('--osm', nargs=1, type=str, default='')
    parser.add_argument('--verbose', action='store_true')

    fn_lookup = {
        'e': print,
        'r': read_binary,
        'w': write_binary,
        'x': read_text,
        't': write_text,
        'f': None,
        'o': None
    }

    # Parse args
    args = parser.parse_args()
    fns = args.fns
    is_verbose = args.verbose

    if args.fn_str:
        fns = fns + 'f'
        fn_str = 'lambda ' + args.fn_str[0]
        fn_lookup['f'] = eval(fn_str)

    if args.osm:
        fns = 'o' + fns
        fn_lookup['o'] = (lambda: make_df(args.osm[0]))

    if is_verbose:
        print(f'fns: {fns}')
        if args.fn_str:
            print(f'fn_str: {args.fn_str[0]}')
        if args.osm:
            print(f'osm_fpath: {args.osm[0]}')

    # TODO: add a if args.fns == DEFAULT_ARGS
    fns = list(fns
               .replace('.', '')
               .replace('-', '')
               .replace('0', ''))

    # Recursively apply functions
    if len(fns) == 0:
        sys.exit(0)
    elif is_verbose:
        print(f'Looping through fns...\n\tfn: {fns[0]}')
    fn = fns.pop(0)
    x = fn_lookup[fn]()
    for fn in fns:
        if is_verbose:
            print(f'\tfn: {fn}')
        x = fn_lookup[fn](x)
