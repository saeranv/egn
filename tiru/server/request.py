from __future__ import annotations
import sys
import typing as typ
import requests
# from io import BytesIO, StringIO
from argparse import ArgumentParser
from select import select

URL = 'http://127.0.0.1:8100/'

# def read_binary() -> bytes:
    # """Read binary stream from stdin."""
#
    # # Create in-memory binary buffer to collect binary stream.
    # byte_file = BytesIO()
#
    # with sys.stdin as stdin:
        # while True:
            # chunk = stdin.buffer.read()
            # if chunk == b'':
                # break
            # # Move "write" postion to stream end w/ seek
            # # or else overwrite
            # byte_file.seek(0, 2)
            # byte_file.write(chunk)
#
    # return byte_file

def read_timed_stdin() -> str|list[typ.Any]:
    """Read stdin """
    # Check if piped data exists
    rlist, wlist, xlist = [sys.stdin], [], []
    timeout = 0.5
    rlist = select(rlist, wlist, xlist, timeout)[0]
    return sys.stdin.read() if rlist else []
    # return read_binary() if rlist else []


def post_binary_image(byte_file:bytes, url:str) -> None:
    img_uri = byte_file
    data = {'message': img_uri}
    response = requests.post(url, json=data)
    print(response.text)


if __name__ == "__main__":

    # TODO: replace with invoke
    parser = ArgumentParser(
        prog='tiru', description='??')
    parser.add_argument('-img', type=str)
    parser.add_argument('-str', type=str)

    args, stdin_arr = parser.parse_known_args()
    if not stdin_arr:
        stdin_arr = read_timed_stdin()

    print(args.img)

    if args.img and len(stdin_arr) > 0:
        # byte_file = read_binary()
        byte_file = stdin_arr[0]
        post_binary_image(byte_file, url=URL)

