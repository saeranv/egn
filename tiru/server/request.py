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

def read_timed_stdin(mode:str) -> str|bytes|list[bytes]|list[str]:
    """Read stdin

    Args:
        mode: 'b' for binary, 't' for text
    """
    # Check if piped data exists
    # [r|w|x]list: wait until ready for [reading|writing|exception-condition]
    read_arr = [sys.stdin] if mode == 't' else [sys.stdin.buffer]
    timeout = 0.5
    readable = select(read_arr, [], [], timeout)[0]
    is_read = len(readable) > 0
    return read_arr[0].readline() if is_read else []


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
        if args.img:
            stdin_arr = read_timed_stdin('b')
        else:
            stdin_arr = read_timed_stdin('t')

    print(args.img)
    if args.img and len(stdin_arr) > 0:
        byte_file = stdin_arr[0]
        post_binary_image(byte_file, url=URL)

