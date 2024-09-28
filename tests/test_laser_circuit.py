
from pydantic import BaseModel
from gpiozero import PWMLED
import time
import numpy as np

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.lasers import GreenLaser


if __name__ == "__main__":

    ts = np.linspace(0, 4 * np.pi, 1000)
    # intensities =  0.5 * (np.sin(ts) + 1)
    dt = 0.01
        
    lasers = GreenLaser(channels=[2, 13])
    # lasers = GreenLaser()

    intensities = np.stack([
        1.0 * 0.5 * (np.sin(ts + 0) + 1),
        0.5 * 0.5 * (np.sin(ts + 0.2 * np.pi) + 1)
        ], axis=1)
    
    print(intensities.shape)
    lasers.waveform(intensities=intensities, dt=dt)