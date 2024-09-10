from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device, PWMLED
Device.pin_factory = LGPIOFactory(chip=4)