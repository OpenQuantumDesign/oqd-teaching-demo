from pydantic import BaseModel
from gpiozero import LED, PWMLED
import time
import lgpio
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
        self._h = lgpio.gpiochip_open(0) # Pi's main gpiochip

        lgpio.gpio_claim_output(self._h, self.pin_reset) # claim G1 of gpiochip
        lgpio.gpio_claim_output(self._h, self.pin_left) # claim G1 of gpiochip
        lgpio.gpio_claim_output(self._h, self.pin_right, lFlags=lgpio.SET_ACTIVE_LOW)

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
        lgpio.gpio_write(self._h, self.pin_left, 1)
        lgpio.gpio_write(self._h, self.pin_right, 1)

    def right(self):
        lgpio.gpio_write(self._h, self.pin_left, 0)
        lgpio.gpio_write(self._h, self.pin_right, 0)

    def shake(self):
        """
        Shakes the trap positions in a sawtooth motion, with a period of `Trap.period`.
        Returns:

        """
        lgpio.tx_pwm(self._h, self.pin_left, self.frequency, self.duty)
        lgpio.tx_pwm(self._h, self.pin_right, self.frequency, self.duty)

    def close(self):
        # lgpio.gpio_claim_output(self._h, self.pin_left) # claim G1 of gpiochip
        # lgpio.gpio_claim_output(self._h, self.pin_right)
        lgpio.gpio_write(self._h, self.pin_left, 1)
        lgpio.gpio_write(self._h, self.pin_right, 0)




if __name__ == "__main__":
    trap = Trap()
    trap.shake()
    # trap.right()
    
    for i in range(10):
        print(i)
        time.sleep(0.1)
    # time.sleep(1)
    # import lgpio as sbc

    # G1=16
    # G2=20

    # FREQ = 2
    # DUTY = 50

    # h = sbc.gpiochip_open(0) # Pi's main gpiochip

    # sbc.gpio_claim_output(h, G1) # claim G1 of gpiochip
    # sbc.gpio_claim_output(h, G2)#, lFlags=sbc.SET_ACTIVE_LOW) #, lFlags=sbc.SET_ACTIVE_LOW) # claim G2 of gpiochip
    # sbc.gpio_write(h, G1, 1)
    # sbc.gpio_write(h, G2, 1)

    # sbc.tx_pwm(h, G1, FREQ, DUTY)
    # sbc.tx_pwm(h, G2, FREQ, DUTY)
    input()
    trap.close()
    # time.sleep(30)
    # import RPi.GPIO as GPIO
    # GPIO.setmode(GPIO.BCM)
    # pin = 16
    # GPIO.setup(pin, GPIO.OUT)
    # GPIO.output(pin, False)

    # pin = 20
    # GPIO.setup(pin, GPIO.OUT)
    # GPIO.output(pin, True)

    # pin = 21
    # GPIO.setup(pin, GPIO.OUT)
    # GPIO.output(pin, False)
    
    # input()
    # GPIO.cleanup()
    # time.sleep(10)
    # LED(14, active_high=True).on()
    # trap.shake()
    # time.sleep(10)
    # trap.off()
    # trap.reset()
    # PI = pigpio.pi()
    # PI.hardware_PWM(12, 400, 200000)

    # import time = 

    # input()
