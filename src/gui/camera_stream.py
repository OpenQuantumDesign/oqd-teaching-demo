# Copyright 2024-2025 Open Quantum Design

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import controls
import cv2

# Initialize the camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(camera_config)
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 11.0})


# Flask app
app = Flask(__name__)


def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        frame = cv2.flip(frame, -1)
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        # Yield frame as part of HTTP response
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/stream")
def stream():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
