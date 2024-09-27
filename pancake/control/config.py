# from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device, PWMLED, LED, LEDBoard
# Device.pin_factory = LGPIOFactory(chip=4)
import time


ch = LED(pin=16)
ch.on()
time.sleep(3)