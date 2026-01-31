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

"""
Mock implementations of hardware control classes for testing without physical hardware.

These classes provide the same interface as the real hardware classes but print
actions instead of controlling GPIO pins, lasers, or cameras.
"""

from pydantic import BaseModel, Field
from pydantic.types import NonNegativeInt
from typing import Literal
import time
import threading
import numpy as np


class MockTrap(BaseModel):
    """Mock implementation of the acoustic trap controller."""

    pin_left: int = 20
    pin_right: int = 16
    pin_reset: int = 21
    frequency: float = 1
    duty: float = 50

    def model_post_init(self, _context=None):
        self._current_mode = "stop"
        print(f"[MockTrap] Initialized with pins: left={self.pin_left}, right={self.pin_right}, reset={self.pin_reset}")

    def left(self):
        self._current_mode = "left"
        print("[MockTrap] Moving trap LEFT")

    def right(self):
        self._current_mode = "right"
        print("[MockTrap] Moving trap RIGHT")

    def stop(self):
        self._current_mode = "stop"
        print("[MockTrap] Trap STOPPED")

    def shake(self):
        self._current_mode = "shake"
        print(f"[MockTrap] Trap SHAKING at frequency={self.frequency}Hz, duty={self.duty}%")

    def mode(self, mode: Literal["left", "right", "shake", "stop"]):
        if mode == "left":
            self.left()
        elif mode == "right":
            self.right()
        elif mode == "shake":
            self.shake()
        elif mode == "stop":
            self.stop()
        else:
            print(f"[MockTrap] Unknown mode: {mode}")

    def close(self):
        print("[MockTrap] Closing trap controller")
        self._current_mode = "stop"


class MockLaserArray(BaseModel):
    """Mock implementation of the laser array controller."""

    channels: list[int] = []

    def model_post_init(self, _context=None):
        self._intensities = {channel: 0.0 for channel in self.channels}
        print(f"[MockLaserArray] Initialized with channels: {self.channels}")

    def set_intensities(self, intensities: list):
        for j, channel in enumerate(self.channels):
            self.set_intensity(idx=j, intensity=intensities[j])

    def set_intensity(self, idx: int, intensity: float):
        channel = self.channels[idx]
        self._intensities[channel] = intensity
        print(f"[MockLaserArray] Channel {channel} (idx={idx}) intensity set to {intensity:.2f}")

    def waveform(self, intensities: np.array, dt: float):
        print(f"[MockLaserArray] Playing waveform with {intensities.shape[0]} steps, dt={dt}s")
        for i in range(intensities.shape[0]):
            for j, channel in enumerate(self.channels):
                self._intensities[channel] = intensities[i, j]
            time.sleep(dt)
        print("[MockLaserArray] Waveform complete")

    def on(self):
        print("[MockLaserArray] All lasers ON (intensity=1.0)")
        for channel in self.channels:
            self._intensities[channel] = 1.0

    def off(self):
        print("[MockLaserArray] All lasers OFF")
        for channel in self.channels:
            self._intensities[channel] = 0.0


class MockRedLasers(MockLaserArray):
    """Mock implementation of red laser array."""

    channels: list[int] = [5, 6, 19, 26]

    def model_post_init(self, _context=None):
        self._intensities = {channel: 0.0 for channel in self.channels}
        print(f"[MockRedLasers] Initialized with channels: {self.channels}")


class MockGreenLaser(MockLaserArray):
    """Mock implementation of green laser."""

    channels: list[int] = [2]

    def model_post_init(self, _context=None):
        self._intensities = {channel: 0.0 for channel in self.channels}
        print(f"[MockGreenLaser] Initialized with channels: {self.channels}")


class MockBlueLaser(MockLaserArray):
    """Mock implementation of blue laser."""

    channels: list[int] = [3]

    def model_post_init(self, _context=None):
        self._intensities = {channel: 0.0 for channel in self.channels}
        print(f"[MockBlueLaser] Initialized with channels: {self.channels}")


class MockCamera(BaseModel):
    """Mock implementation of the Raspberry Pi camera."""

    transform: Literal["none", "horizontal", "vertical", "both"] = "none"
    exposure_time: NonNegativeInt = 30000
    analog_gain: float = 1.0

    def model_post_init(self, _context=None):
        print(f"[MockCamera] Initialized with transform={self.transform}, exposure_time={self.exposure_time}, analog_gain={self.analog_gain}")

    def capture(self, file: str = "image"):
        print(f"[MockCamera] Capturing image to {file}.png")


class MockDevice(BaseModel):
    """Mock implementation of the main device controller."""

    trap: MockTrap = Field(default_factory=MockTrap)
    red_lasers: MockRedLasers = Field(default_factory=MockRedLasers)
    blue_laser: MockBlueLaser = Field(default_factory=MockBlueLaser)

    def model_post_init(self, _context=None):
        self._stop_event = threading.Event()
        print("[MockDevice] Device initialized")

    def stop(self):
        print("[MockDevice] Stopping task...")
        self._stop_event.set()

    def run(self, program):
        print(f"[MockDevice] Running program with {len(program)} steps")
        for i in range(len(program)):
            if self._stop_event.is_set():
                print("[MockDevice] Program interrupted.")
                break
            self.red_lasers.set_intensities(intensities=program.red_lasers_intensity[i])
            time.sleep(program.dt)

        self.red_lasers.off()
        print("[MockDevice] Program complete")
        return


if __name__ == "__main__":
    print("=== Testing MockDevice ===\n")

    device = MockDevice()

    print("\n--- Testing trap modes ---")
    device.trap.left()
    device.trap.right()
    device.trap.shake()
    device.trap.stop()

    print("\n--- Testing laser control ---")
    device.red_lasers.set_intensity(idx=0, intensity=0.5)
    device.red_lasers.on()
    device.red_lasers.off()

    print("\n--- Testing blue laser ---")
    device.blue_laser.on()
    device.blue_laser.off()

    print("\n=== Mock tests complete ===")
