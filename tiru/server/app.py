import base64
import os
import cv2
import numpy as np
import numpy.typing as npt
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="eventlet")
STATE = session


@socketio.on("connect")
def test_connect():
    """Send message to client from server to confirm client-server connection.

    It sends a message to the client letting it know that it has successfully
        connected.

    Returns A 'connected' string
    """
    print("Connected")
    emit("my response", {"data": "Connected"})


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
    base64_data = base64_str.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
    STATE['debug'] += [image_arr.shape, image_arr.dtype, image.shape, image.dtype]
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
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("processed_image", processed_img_data)

@app.route("/stream")
def stream(methods=['GET', 'POST']):
    if request.method == 'POST':
        data = request.get_json()
        url = data['message']
        emit('process_img', url)


@socketio.on('process_image')
def handle_img(url):
    emit('stream_image', url)


@app.route('/')
def index():
    """Renders the index.html template."""

    if 'debug' not in STATE:
        STATE['debug'] = ["first"]
    debug = STATE['debug']
    state = 'state-check-2'

    return render_template("index.html", debug=debug, state=state)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8100, host='0.0.0.0')

