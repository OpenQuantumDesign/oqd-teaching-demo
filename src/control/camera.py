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


from pydantic import BaseModel
from pydantic.types import NonNegativeInt, Literal
from picamera2 import Picamera2, Preview


"""
Relevant resources for setting up a RPi camera:
# https://stackoverflow.com/questions/78604504/displaying-raspberry-pi-camera-3-using-pyqt5-on-pi5-results-in-odd-images
# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5
# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
# https://forums.raspberrypi.com/viewtopic.php?t=354644
"""

class Camera(BaseModel):
    transform: Literal["none", "horizontal", "vertical", "both"] = "none"
    exposure_time: NonNegativeInt = 30000
    analog_gain: float = 1.0

    def model_post_init(self, _context=None):
        self._camera = Picamera2()
        config = self._camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)})
        self._camera.configure(config)

    def capture(self, file: str = "image"):
        self._camera.start()
        self._camera.capture_file(f"{file}.png")


if __name__ == "__main__":
    camera = Camera()
    camera.capture(file="test_capture")
