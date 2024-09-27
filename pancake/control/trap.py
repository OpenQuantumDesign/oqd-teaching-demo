from pydantic import BaseModel
from gpiozero import LED
import time


class Trap(BaseModel):
    pin_left: int = 14
    pin_right: int = 15
    pin_reset: int = 18
    period: float = 0.2

    def model_post_init(self, _context=None):
        self._pin_left = LED(self.pin_left)
        self._pin_right = LED(self.pin_right)
        self._pin_reset = LED(self.pin_reset)

        self.off()

    def reset(self):
        self._pin_reset.off()
        time.sleep(0.1)
        self._pin_reset.on()

    def off(self):
        for pin in [self._pin_left, self._pin_right, self._pin_reset]:
            pin.on()

    def left(self):
        self._pin_left.off()
        self._pin_right.on()

    def right(self):
        self._pin_left.on()
        self._pin_right.off()

    def shake(self):
        """
        Shakes the trap positions in a sawtooth motion, with a period of `Trap.period`.
        Returns:

        """
        for i in range(10):
            self.left()
            time.sleep(self.period/2)
            self.right()
            time.sleep(self.period/2)
        self.off()

if __name__ == "__main__":
    trap = Trap(period=0.9)
    trap.shake()
    # trap.reset()

