# egn/server.py
"""Server for egn.
# Ref: https://stackoverflow.com/a/74382868/2185097
"""

import socket

# Load some slow modules
import matplotlib.pyplot as plt
import numpy as np
import openstudio
import time
import pandas as pd
import runpy
from . import stream_io
HOST = 'localhost'
PORT = 50007


if __name__ == "__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((HOST, PORT))
    except ConnectionRefusedError as err:
        print("error!", err.strerror)
        exit(1)

    # Start server with maximum 100 connections
    server_socket.listen(100)
    print("Starting server connection.")
    while True:
        connection, address = server_socket.accept()
        buf = connection.recv(64)
        # TODO: io.read_bin  # just get inner_loop?
        if len(buf) > 0:
            buf_str = str(buf.decode("utf-8"))
            now = time.time()
            #runpy.run_path(path_name=buf_str)
            print(buf_str, np.pi)
            after = time.time()
            duration = after - now
            print(f"I received {buf_str} script and it took "
                  f"{duration} seconds to execute it")
        if buf==b'':
            # TODO: receives raw data from server_socket
            # TODO: sends raw data to io.main and gets response
            # TODO: serializes raw data as json
            # TODO: sends json to client

