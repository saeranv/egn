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


def text_file(text_str:str, url:str) -> None:
    """Post image as base64 encoded string to server."""
    data = {'message':text_str}
    _ = requests.post(url, json=data)


def status(url:str) -> int:
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
        '-txt', '--text_file', type=FileType('r'))
    parser.add_argument(
        '--status', action='store_true', default=False,
        help=('# Exit with status code 0 (success) if server else1\n'
              '$ [[ $(python request.py -stat) == "200" ]] && echo "Run."'))
    parser.add_argument(
        '--url', action='store_true', default=False)
    args =  parser.parse_args()

    if args.image_file:
        url = URL + 'image_file'
        # args.img is file object io.BufferedReader
        # convert to base64 str to send through json
        byte_data = args.image_file.read()  # bytes
        byte_b64_str = base64.b64encode(byte_data).decode('utf-8') # base64 str
        image_file(byte_b64_str, url=url)
    elif args.text_file:
        url = URL + 'text_file'
        text_file(args.text_file.read(), url=url)
    elif args.url:
        print(URL, file=sys.stdout)
    elif args.status:
        url = URL + 'status'
        try:
            status_code = status(url=url)
        except requests.exceptions.ConnectionError:
           status_code = 400
        print(status_code, file=sys.stdout)
