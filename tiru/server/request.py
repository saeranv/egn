from __future__ import annotations
import sys
import typing as typ
import requests
from argparse import ArgumentParser, FileType
import base64

URL = 'http://127.0.0.1:8100/'

# TODO: we want this to be used within python for visualization from .py
# file editing.
def image_file(byte_str:str, url:str) -> None:
    """Post image as base64 encoded string to server."""
    data = {'message': byte_str}
    _ = requests.post(url, json=data)

def server_status(url:str) -> int:
    """Check if server is running."""
    r = requests.get(url)
    return r.status_code


if __name__ == "__main__":

    # TODO: replace with invoke
    parser = ArgumentParser(
        prog='tiru', description='??')
    parser.add_argument(
        '-img', '--image_file', type=FileType('rb'),
        help=('# Accepts img filepath: \n'
              '$ request.py -img ./img.jpg'
              '# To stream file as <stdin> use "-" as arg:\n'
              '$ cat img.jpg | request.py -img -\n'))
    parser.add_argument(
        '-stat', '--server_status', action='store_true',
        default='False',
        help=('# Exit with status code 0 (success) if server else1\n'
              '$ request.pu -stat && echo "Success" || echo "Fail"'))
    args =  parser.parse_args()

    if args.image_file:
        # args.img is file object io.BufferedReader
        # convert to base64 str to send through json
        byte_data = args.image_file.read()  # bytes
        byte_b64_str = base64.b64encode(byte_data).decode('utf-8') # base64 str
        image_file(byte_b64_str, url=URL)
    elif args.server_status:
        status_url = URL + 'status'
        try:
            status_code = server_status(url=status_url)
        except requests.exceptions.ConnectionError:
           status_code = 400
        print(status_code)
