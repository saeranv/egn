from __future__ import annotations
import sys
import typing as typ
import requests
from argparse import ArgumentParser, FileType
import base64

URL = 'http://127.0.0.1:8100/'

# TODO: we want this to be used within python for visualization from .py
# file editing.
def post_byte_image(byte_str:str, url:str) -> None:
    """Post image as base64 encoded string to server."""
    data = {'message': byte_str}
    _ = requests.post(url, json=data)


if __name__ == "__main__":

    # TODO: replace with invoke
    parser = ArgumentParser(
        prog='tiru', description='??')
    parser.add_argument(
        '-img', '--img_file', type=FileType('rb'),
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
    if args.img_file:
        # args.img is file object io.BufferedReader, convert to base64 str
        # to send through json
        byte_data = args.img_file.read()  # bytes
        byte_b64_str = base64.b64encode(byte_data).decode('utf-8') # base64 str
        post_binary_image(bytes_b64_str, url=URL)
