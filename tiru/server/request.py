from __future__ import annotations
import sys
import typing as typ
import requests
from io import BytesIO, StringIO
from argparse import ArgumentParser


def read_binary() -> bytes:
    """Read binary stream from stdin."""

    # Create in-memory binary buffer to collect binary stream.
    byte_file = BytesIO()

    with sys.stdin as stdin:
        while True:
            chunk = stdin.buffer.read()
            if chunk == b'':
                break
            # Move "write" postion to stream end w/ seek
            # or else overwrite
            byte_file.seek(0, 2)
            byte_file.write(chunk)

    return byte_file


def post_binary_image(byte_file:bytes) -> None:
    url = 'http://127.0.0.1:8100/'
    img_uri = byte_file
    data = {'message': img_uri}
    response = requests.post(url, json=data)
    #print(response.text)



if __name__ == "__main__":

    parser = ArgumentParser(
        prog='tiru', description='??')
    parser.add_argument('-img', type=str)
    parser.add_argument('-str', type=str)

    args = parser.parse_args()
    print(args.img)
    if args.img:
        byte_file = read_binary()
        post_binary_image(byte_file)

