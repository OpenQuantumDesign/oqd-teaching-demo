from pydantic import BaseModel
from gpiozero import PWMLED
import time
import numpy as np

class Lasers(BaseModel):
    channels: list[int] = [5, 6, 13, 19, 26]

    def model_post_init(self, _context=None):
        self._lasers = {channel: PWMLED(channel) for channel in self.channels}

    def waveform(self, intensities: np.array, dt: float):
        for i in range(intensities.shape[0]):
            for j, channel in enumerate(self.channels):
                self._lasers[channel].value = intensities[i,j]
            time.sleep(dt)
    
    def on(self):
        for channel in self.channels:
            self._lasers[channel].value = 1.0


    def off(self):
        for channel in self.channels:
            self._lasers[channel].value = 0.0


    
if __name__ == "__main__":

    ts = np.arange(1000)
    # intensities =  0.5 * (np.sin(ts) + 1)
    dt = 0.05
        
    lasers = Lasers()

    intensities = np.stack(
        [
            0.5 * (np.sin(0.3 * ts + i) + 1) for i, channel in enumerate(lasers.channels)
        ], axis=1
    )
    lasers.waveform(intensities=intensities, dt=dt)