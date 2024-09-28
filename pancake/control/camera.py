from pydantic import BaseModel
from pydantic.types import NonNegativeInt, Literal
from picamera2 import Picamera2, Preview

# https://stackoverflow.com/questions/78604504/displaying-raspberry-pi-camera-3-using-pyqt5-on-pi5-results-in-odd-images
# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5
# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
# https://forums.raspberrypi.com/viewtopic.php?t=354644

class Camera(BaseModel):
    transform: Literal["none", "horizontal", "vertical", "both"] = "none"
    exposure_time: NonNegativeInt = 10000
    analog_gain: float = 1.0

    def model_post_init(self, _context=None):
        self._camera = Picamera2()
        config = self._camera.create_preview_configuration()
        self._camera.configure(config)
        self._camera.set_controls({"ExposureTime": self.exposure_time, "AnalogueGain": self.analog_gain})

    def capture(self):
        image = self._camera.capture_image()
        image = image.convert("RGBA")
        return image


if __name__ == "__main__":
    camera = Camera()