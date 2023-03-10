# egn/stream_io.py
"""IO operations for in-memory streams of binary or text formats."""
import sys
from io import BytesIO, StringIO

# TODO: remove
from pandas import read_feather as pd_read_feather


def read_text(fp=None, enc='utf-8') -> str:
    """Create in-memory text buffer from file-like obj.

    Args:
        fp: file-like object like stdin.

    Returns str.
    """
    # text_file = StringIO()
    # with sys.stdin as stdin:
    #     while True:
    #         chunk = stdin.readline()
    #         if chunk == '':
    #             break
    #         # Move "write" postion to end of stream
    #         # with seek, else write will overwrite
    #         text_file.write(chunk)
    # text_str = text_file.getvalue()
    # return text_str
    fp = sys.stdin if fp is None else fp
    data = read_binary(fp)
    txt = bytes.decode(data, enc)

    return txt


def read_binary(fp=None) -> pd.DataFrame:
    """Create in-memory binary buffer to collect binary stream."""

    fp = sys.stdin.buffer if fp is None else fp
    byte_arr = b''
    buf_size = 64
    with fp as buf:
        while True:
            chunk = buf.read(buf_size)
            if chunk == b'':
                break
            # Move "write" postion to end of stream
            # with seek, else write will overwrite
            # byte_file.seek(0, 2)
            byte_arr += chunk
    return byte_arr


def write_text(data:Any, fp=None) -> None:
    """Write text or binary to file-like objects like
    stdout, StringIO etc.

    Input df is written to the stdout buffer via
        the to_feather method.
    """

    # Stdout is a FileIO object, and stdout.buffer is a
    # BytesIO object?
    # Don't use writelines, applies to every char.
    #writer = lambda _buf, _data: \
    #    [_buf.write(text) for text in _data]
    data = bytes.encode(data, 'utf-8')
    fp = sys.stdin.buffer if fp is None else fp
    write_binary(data, fp)


def write_binary(data:bytes, fp=None) -> None:

    # Assume all binary data is a dataframe.
    # For in-memory binary streams we use
    # stdout.buffer.write(data) via df.to_feather
    # will uses a provided buf object to write binary to.
    # TODO: remove this to client(?)
    fp = sys.stdout.buffer if fp is None else fp
    with fp as buf:
        _ = [buf.write(d) for d in data]
        buf.flush()
    return fp


def deserial_fns(args_dict):
    fn_arr = (lambda d: eval(f'egn.{k}')(d, v)
              for k, v in args_dict.items())
    return fn_arr


# TODO: move this to eigen?
def deserial_df(byte_arr:bytes) -> pd.DataFrame:
    """Convert binary data to df."""
    byte_fp = BytesIO(byte_arr)
    df = pd_read_feather(byte_fp)
    return df


def serial_df(df:pd.DataFrame) -> bytes:
    byte_fp = BytesIO()
    df.to_feather(byte_fp)
    byte_fp.seek(0)  # reset position
    return byte_fp.read()



def pipe_fns(fn_arr, data):
    """Return function composition."""

    for fn in fn_arr:
        data = fn(data)

    return data


def main(args_dict:dict, data:bytes):

    header = BytesIO(data).read(64)
    if header == 'type:df':
        data = deserialize_df(data)
    elif header == 'type:osm':
        data = deserialize_osm(data)
    elif header == 'type:str'
        data = str.encode(data, 'utf-8')
    elif header == 'type:bytes':
        data = data
    else:
        raise Exception('unrecognized header')

    # Read
    fn_arr = serial_fns(args_dict)
    data = pipe_fns(fn_arr, data)
    return data



