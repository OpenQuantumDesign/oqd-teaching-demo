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
from gpiozero import PWMLED
import time
import numpy as np


class LaserArray(BaseModel):
    """ Base class for laser control using PWM (pulse width modulation) on the Raspberry Pi. """
    channels: list[int] = []

    def model_post_init(self, _context=None):
        self._lasers = {channel: PWMLED(channel) for channel in self.channels}

    def set_intensities(self, intensities: list):
        for j, channel in enumerate(self.channels):
            self.set_intensity(idx=j, intensity=intensities[j])

    def set_intensity(self, idx: int, intensity: float):
        self._lasers[self.channels[idx]].value = intensity


    def waveform(self, intensities: np.array, dt: float):
        for i in range(intensities.shape[0]):
            for j, channel in enumerate(self.channels):
                self._lasers[channel].value = intensities[i,j]
            time.sleep(dt)

    def on(self):
        """
        Turn all lasers on (maximum intensity).

        Returns:

        """
        for channel in self.channels:
            self._lasers[channel].value = 1.0

    def off(self):
        """
        Turns all lasers off.
        Returns:

        """
        for channel in self.channels:
            self._lasers[channel].value = 0.001


class RedLasers(LaserArray):
    channels: list[int] = [5, 6, 19, 26]


class GreenLaser(LaserArray):
    channels: list[int] = [2]  # 


class BlueLaser(LaserArray):
    channels: list[int] = [3]


if __name__ == "__main__":
    ts = np.arange(100)
    dt = 0.15
    lasers = RedLasers()

    intensities = np.stack(
        [
            0.2 * (np.sin(0.3 * ts + i) + 1) for i, channel in enumerate(lasers.channels)
        ], axis=1
    )
    print(intensities)
    print(intensities.shape)

    lasers.waveform(intensities=intensities, dt=dt)