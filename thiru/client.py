# egn/client.py
"""Client for egn."""

import sys
import socket
from argparse import ArgumentParser
import json
HOST = 'localhost'
PORT = 50007

from . import io

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


if __name__ == '__main__':

    # Set args
    parser = ArgumentParser(
        prog='egn', description='parser')
    parser.add_argument('-o'        , '--osm')
    #parser.add_argument('-r'       , '--read_text')
    #parser.add_argument('-rb'      , '--read_binary')
    #parser.add_argument('-w'       , '--write_text')
    #parser.add_argument('-wb'      , '--write_binary')
    parser.add_argument('-fn'       , '--fn_str', nargs=1, type=str, default='')
    # Modal options
    parser.add_argument('--osm'     , nargs=1, type=str, default='')
    parser.add_argument('--verbose' , action='store_true')

    # Write text or binary to server.
    args = parser.parse_args()
    args_dict = vars(args).items()

    args_bytes = json.dump(args_dict).encode('utf-8')
    client_socket.send(args_bytes)
    data_bytes = egn_io.read_binary(sys.stdin.buffer, 'utf-8')
    client_socket.send(data_bytes)


