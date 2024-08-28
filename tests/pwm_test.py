# import pigpio
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

print(GPIO.RPI_INFO)
channels = [29, 31, 33, 35, 37]

for channel in channels:
    GPIO.setup(channel, GPIO.OUT)

dc = 10.0
for channel in channels:
    # GPIO.output(channel, True)
    p = GPIO.PWM(channel, 100)  # channel 10, frequency in Hz
    p.start(dc)   # where dc is the duty cycle (0.0 <= dc <= 100.0)

input('Press return to stop:')
# p.stop()

GPIO.cleanup()