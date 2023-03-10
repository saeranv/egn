import sys
from argparse import ArgumentParser

ENC = 'utf-8'

if __name__ == "__main__":


    parser = ArgumentParser()
    parser.add_argument('a', nargs=1)
    args = parser.parse_args()
    #print('args:', args.a)
    #print('istty?', sys.stdin.isatty())
    #tamil = "ஒரு"
    #tamil_bytes = str.encode(tamil, ENC)
    #print('encode:', str.encode(tamil, encoding=ENC))
    #print('decode:', bytes.decode(tamil_bytes, encoding=ENC))
    data = b''
    with sys.stdin.buffer as stdin:
        while True:
            chunk = stdin.readline()
            if chunk == b'': break
            data += chunk
            print('chunk:', chunk, sys.getsizeof(chunk))
    print(bytes.decode(data, ENC))


