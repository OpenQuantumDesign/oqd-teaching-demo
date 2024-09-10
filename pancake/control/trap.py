from pydantic import BaseModel
import RPi.GPIO as GPIO
import time


class Trap(BaseModel):
    pin_left: int = 14
    pin_right: int = 15
    pin_reset: int = 18
    period: float = 0.2

    def model_post_init(self, _context=None):
        GPIO.setmode(GPIO.BOARD)

        self.off()

        # self.reset()

    def reset(self):
        GPIO.output(self.pin_reset, False)
        time.sleep(0.1)
        GPIO.output(self.pin_reset, True)

    def off(self):
        channels = [29, 31, 33, 35, 37]

        for channel in channels:
            GPIO.setup(channel, GPIO.OUT)

        for channel in channels:
            GPIO.output(channel, True)

    def left(self):
        GPIO.output(self.pin_left, False)
        GPIO.output(self.pin_right, True)

    def right(self):
        GPIO.output(self.pin_left, True)
        GPIO.output(self.pin_right, False)

    def shake(self):
        for i in range(10):
            self.left()
            time.sleep(self.period/2)
            self.right()
            time.sleep(self.period/2)

    def close(self):
        # self.off()
        GPIO.cleanup()


if __name__ == "__main__":
    trap = Trap(period=0.9)
    trap.shake()
    trap.close()

