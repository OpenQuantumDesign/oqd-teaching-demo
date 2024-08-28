from pydantic import BaseModel
import RPi.GPIO as GPIO
import time
import numpy as np

class Lasers(BaseModel):
    channels: list[int] = [29, 31, 33, 35, 37]
    intensities: list[float] = 5 * [0.001,]
    frequency: float = 100.0

    def model_post_init(self, _context=None):
        GPIO.setmode(GPIO.BOARD)
        self._pwms = {channel: None for channel in self.channels}
        for channel in self.channels:
            GPIO.setup(channel, GPIO.OUT)

        
    def initialize(self):
        for channel, intensity in zip(self.channels, self.intensities):
            # GPIO.output(channel, True)
            p = GPIO.PWM(channel, self.frequency)  # channel 10, frequency in Hz
            p.start(0.10)   # where dc is the duty cycle (0.0 <= dc <= 100.0)
            # p.start(intensity * 100.0)   # where dc is the duty cycle (0.0 <= dc <= 100.0)
            self._pwms[channel] = p

    def waveform(self, intensities: np.array, dt: float):
        for intensity in intensities: 
            for channel in self.channels:
                self._pwms[channel].ChangeDutyCycle(intensity * 100.0)
            time.sleep(dt)

    def off(self):
        for channel in self.channels:
            self._pwms[channel].stop()
            GPIO.output(channel, False)

    def close(self):
        self.off()
        GPIO.cleanup()


    
if __name__ == "__main__":

    intensities = np.linspace(0.0, 0.1, 100)
    dt = 0.05
        
    lasers = Lasers()
    lasers.initialize()
    lasers.waveform(intensities=intensities, dt=dt)
    input('Press return to stop:')
    lasers.close()