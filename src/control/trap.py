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
from gpiozero import LED, PWMLED
import time
import lgpio as gpio
import atexit
from typing import Literal


class Trap(BaseModel):
    pin_left: int = 20
    pin_right: int = 16
    pin_reset: int = 21
    frequency: float = 1
    duty: float = 50

    def model_post_init(self, _context=None):
        self._h = gpio.gpiochip_open(0) # Pi's main gpiochip

        gpio.gpio_claim_output(self._h, self.pin_reset) # claim G1 of gpiochip
        gpio.gpio_claim_output(self._h, self.pin_left) # claim G1 of gpiochip
        gpio.gpio_claim_output(self._h, self.pin_right, lFlags=gpio.SET_ACTIVE_LOW)

        gpio.gpio_write(self._h, self.pin_reset, 1)

    def left(self):
        gpio.gpio_write(self._h, self.pin_left, 1)
        gpio.gpio_write(self._h, self.pin_right, 1)

    def right(self):
        gpio.gpio_write(self._h, self.pin_left, 0)
        gpio.gpio_write(self._h, self.pin_right, 0)

    def stop(self):
        gpio.gpio_write(self._h, self.pin_right, 0)
        gpio.gpio_write(self._h, self.pin_left, 1)
        
    def shake(self):
        """
        Shakes the trap positions in a sawtooth motion, with a period of `Trap.period`.
        Returns:

        """
        gpio.tx_pwm(self._h, self.pin_left, self.frequency, self.duty)
        gpio.tx_pwm(self._h, self.pin_right, self.frequency, self.duty)

    def mode(self, mode: Literal['left', 'right', 'shake', 'stop']):
        if mode == "left":
            self.left()
        elif mode == "right":
            self.right()
        elif mode == "shake":
            self.shake()
        elif mode == "stop":
            self.stop()
        else:
            pass

    def close(self):
        gpio.gpio_write(self._h, self.pin_right, 0)
        time.sleep(0.05)
        gpio.gpio_write(self._h, self.pin_left, 1)
        time.sleep(0.05)
        

if __name__ == "__main__":
    trap = Trap()
    trap.left()
    
    input()
    trap.right()

    input()
    trap.shake()

    input()
    trap.close()
    