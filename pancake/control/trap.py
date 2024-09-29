from pydantic import BaseModel
from gpiozero import LED, PWMLED
import time
import lgpio as gpio
# import rgpio as gpio
import atexit


class Trap(BaseModel):
    pin_left: int = 16
    pin_right: int = 20
    pin_reset: int = 21
    frequency: float = 1
    duty: float = 50

    def model_post_init(self, _context=None):
        # self._pin_left = LED(self.pin_left)
        # self._pin_left =  PWMLED(self.pin_left, active_high=False, frequency=0.5, initial_value=1)
        # self._pin_right = LED(self.pin_right)
        # self._pin_right =  PWMLED(self.pin_right, active_high=False, frequency=0.5, initial_value=1)
        # self._pin_reset = LED(self.pin_reset)
        # self._pin_left.off()
        # self._pin_right.off()
        # self._pin_reset.off()
        # self.off()

        # sbc = gpio.sbc()
        # self._h = sbc.gpiochip_open(0) # Pi's main gpiochip
        self._h = gpio.gpiochip_open(0) # Pi's main gpiochip

        gpio.gpio_claim_output(self._h, self.pin_reset) # claim G1 of gpiochip
        gpio.gpio_claim_output(self._h, self.pin_left) # claim G1 of gpiochip
        gpio.gpio_claim_output(self._h, self.pin_right, lFlags=gpio.SET_ACTIVE_LOW)

        gpio.gpio_write(self._h, self.pin_reset, 1)


    # def reset(self):
    #     self._pin_reset.off()
    #     time.sleep(0.1)
    #     self._pin_reset.on()

    # def off(self):
    #     self._pin_left.off()
    #     self._pin_right.on()
    #     # for pin in [self._pin_left, self._pin_right, self._pin_reset]:
    #         # pin.on()

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

    def close(self):
        # self._h.stop()
        # self.left()
        # self.right()
        gpio.gpio_write(self._h, self.pin_right, 0)
        time.sleep(0.05)
        gpio.gpio_write(self._h, self.pin_left, 1)
        time.sleep(0.05)
        




if __name__ == "__main__":
    trap = Trap()
    # trap.shake()
    # trap.right()
    trap.left()
    
    input()
    trap.right()

    input()
    trap.shake()

    input()
    trap.close()
    