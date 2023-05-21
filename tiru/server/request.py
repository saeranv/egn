from __future__ import annotations
import sys
import typing as typ
import requests
from io import BytesIO, StringIO
from argparse import ArgumentParser, FileType
from select import select
import base64

URL = 'http://127.0.0.1:8100/'


def read_binary() -> bytes:
    """Read binary stream from stdin."""
    # # Create in-memory binary buffer to collect binary stream.

    #byte_file = BytesIO()
    byte_file = bytearray()
    with sys.stdin as stdin:
        while True:
            chunk = stdin.buffer.read()
            if chunk == b'':
                break
            # Move "write" postion to stream end w/ seek
            # or else overwrite
            # byte_file.seek(0, 2)
            # byte_file.write(chunk)
            byte_file.extend(chunk)
    return byte_file


def read_timed_stdin(mode:str) -> str|bytes|list[bytes]|list[str]:
    """Read stdin
    Args:
        mode: 'b' for binary, 't' for text
    """
    # Check if piped data exists
    # [r|w|x]list: wait until ready for [reading|writing|exception-condition]
    read_arr = [sys.stdin]
    timeout = 0.5
    readable = select(read_arr, [], [], timeout)[0]
    is_read = len(readable) > 0
    if mode == 'b':
        return read_binary() if is_read else []
    else:
        print('implement t mode.')


# TODO: we want this to be used within python for visualization from .py
# file editing.
def post_binary_image(byte_file:bytes, url:str) -> None:
    # If byte_file is io.BytesIO, use byte_file.read()
    img_uri = byte_file
    data = {'message': img_uri}
    response = requests.post(url, json=data)
    # print(response.text)


if __name__ == "__main__":

    # TODO: replace with invoke
    parser = ArgumentParser(
        prog='tiru', description='??')
    parser.add_argument(
        '-img', type=FileType('rb'),
        help=('# to stream file as <stdin> use "-" as arg:\n'
              'cat img.jpg | request.py -img -\n'
              '# to add filename: \n'
              'request.py -img ./img.jpg')
    )
    # args, stdin_arr = parser.parse_known_args()
    args =  parser.parse_args()

    # if stdin_arr:
        # # TODO: fix. Doesn't work because input is text which can't cast
        # # TODO: just make optional narg in -img arg and specify bytes?
        # assert False, "Only piped stdin works."
        # # _stdin_arr = bytearray()
        # # [_stdin_arr.append(bytes(x, 'utf-8')) for x in stdin_arr]
        # # stdin_arr = _stdin_arr
    # # else:
        # stdin_arr = read_timed_stdin('b')
        # stdin_arr = [base64.b64encode(stdin_arr).decode()]

    # print('img: ', args.img, 'txt: ', args.txt)
    if args.img:
        # args.img: io.BufferedReader
        bytes_data = args.img.read()  # bytes
        print(type(bytes_data.decode()))
        # post_binary_image(byte_file, url=URL)
