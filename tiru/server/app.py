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
PORT = 8100
HOST = '127.0.0.1'


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


def init_state(state):
    state['debug'] = [] if 'debug' not in state else state['debug']
    return state


@app.route("/status", methods=['GET'])
def status():
    """Check if server is running."""
    return { 'statusCode': 200 }


@app.route("/image_file", methods=['POST'])
def image_file():
    """Post image to tiru url."""
    image_b64_str = request.get_json()['message']
    image_data = "data:image/jpg;base64," + image_b64_str
    image = base64_to_image(image_data)
    image_stats = f"Image dim: {image.shape}, Image type: {image.dtype}"
    # Use socketio.emit(), not emit() since emit() will send back to
    # original socketio.on event.
    socketio.emit('stream_image', {'data':image_data, 'stats':image_stats})
    return { 'statusCode': 200 }


@app.route("/text", methods=['POST'])
def text_file():
    """Post text to tiru url."""
    text = request.get_json()['message']
    # Use socketio.emit(), not emit() since emit() will send back to
    # original socketio.on event.
    socketio.emit('stream_text', text)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index.html template."""
    debug = []
    return render_template("index.html", debug=debug)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=PORT, host=HOST)

