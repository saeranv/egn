import base64
import os
import cv2
import numpy as np
import numpy.typing as npt
from flask import Flask, session, request, url_for, redirect
from flask_socketio import SocketIO, emit
from jinja2 import Environment, PackageLoader, select_autoescape


# For ezplt
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
pp = print

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="eventlet")
PORT = 8100
HOST = '127.0.0.1'
ENV = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape(),
    trim_blocks=True,           # remove newline from block end
    lstrip_blocks=True,         # remove leading space/tabs from block start
    keep_trailing_newline=True  # keep newline at end of template
)


@socketio.on("connect")
def test_connect():
    """Send message to client from server to confirm client-server connection.

    It sends a message to the client letting it know that it has successfully
        connected.

    Returns A 'connected' string
    """
    print("Connected")
    # emit("connect_response", {"data": "Connected"})
    emit(event="connect_response", data={"data": "Connected"}, callback=None)


def base64_to_image(base64_str:str)->npt.NDArray:
    """Decodes base64 encoded string to an array of unit8 (3,M,N).

    The base64_to_image function accepts a base64 encoded string and returns
    an image. The function extracts the base64 binary data from the input
    string, decodes it, converts the bytes to numpy array, and then decodes
    the numpy array as an image using OpenCV.

    Args:
        base64_str: base64 encoded image string to the
                function

    Returns image as (3,M,N) array.
    """
    base64_data = base64_str.split(",")[1]  # separate header
    image_bytes = base64.b64decode(base64_data)
    image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
    return image


@socketio.on("image")
def receive_image(image:str):
    """Receive base64 string image, convert to string and sends to client.

    Args:
        image: Pass the image data to the receive_image function

    Returns the image that was received from the client
    """
    # Decode the base64-encoded image data
    image = base64_to_image(image)

    # Image processing (convert RGB to color)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame_resized = cv2.resize(gray, (640, 360))
    # Encode image to string
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    image_uri_ = base64.b64encode(frame_encoded).decode()
    image_uri = "data:image/jpg;base64," + image_uri_
    emit("processed_image", image_uri)


@app.route("/status", methods=['GET'])
def status():
    """Check if server is running."""
    return { 'statusCode': 200 }


@app.route("/image_file", methods=['POST'])
def image_file():
    """Post image to tiru url."""
    BLANK_BYTE_STR = base64.b64encode(b'\n').decode("utf-8")  # blank byte as utf-8 str
    image_b64_str = request.get_json()['message']
    image_data = "data:image/jpg;base64," + image_b64_str
    image_stats = ""

    if not BLANK_BYTE_STR == image_b64_str:
        image = base64_to_image(image_data)
        image_stats = f"matrix: {image.shape[:2]}"

    # Use socketio.emit(), not emit() else sends to orig socketio.on event.
    socketio.emit('stream_image', {'data':image_data, 'stats':image_stats})
    return redirect(url_for('index'))


@app.route("/ezplt_file", methods=['POST'])
def ezplt_file():
    """ezplt experiment."""

    def subplots(row=1, col=1, dimx=10, dimy=7):
        fig, ax = plt.subplots(row, col, figsize=(dimx, dimy))
        ax = ax if isinstance(ax, np.ndarray) else [ax]
        return ax

    RAND = np.random.RandomState(101)
    X = RAND.uniform(0, 1, 1000)
    plt_str = request.get_json()['message']
    plt_str_list = plt_str.strip().replace('\n', ';').split(';')
    print(plt_str_list)
    for i, p in enumerate(plt_str_list):
        if len(p) == 0:
          continue
        print(p.strip())
        exec(p.strip())
        print(X.shape)
    print('check shape', X.shape)
    # # process evaluated data
    # buffer = BytesIO()
    # plt.savefig(buffer, format='jpg', bbox_inches='tight', dpi=150)
    # buffer.seek(0)
    # image_b64_str = buffer.getvalue().decode("utf-8")
    # #sys.stdout.buffer.write(buffer.getvalue())
    # image_data = "data:image/jpg;base64," + image_b64_str
    # socketio.emit('stream_image', {'data':image_data, 'stats':"ezplt"})
    return redirect(url_for('index'))


@app.route("/text_file", methods=['POST'])
def text_file():
    """Post text to tiru url."""
    if 'text' not in session:
        session['text'] = []
    raw_text = request.get_json()['message']
    session['text'] += [raw_text]
    parsed_text = raw_text.replace('\n', '<br>')
    # Use socketio.emit(), not emit() else sends to orig socketio.on event.
    socketio.emit('stream_text', parsed_text)
    #return { 'statusCode': 200 }
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index.html template."""
    if not {'text', 'image'}.issubset(session.keys()):
        session['text'], session['image'] = [], []
    # Use redis.. don't want to deal w/ cookies
    debug = [f'image-state:{len(session["image"])}', f'text-state: {len(session["text"])}']
    return ENV.get_template("index.html").render(url_for=url_for, debug=debug)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=PORT, host=HOST)
