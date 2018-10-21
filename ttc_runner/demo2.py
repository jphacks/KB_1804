import RPi.GPIO as GPIO
import time
from wheel_control import WheelControl

try:
    wc = WheelControl()

    wc.forward(duty=100)
    time.sleep(1)
    wc.rotate_left(duty=30)
    time.sleep(0.5)
    wc.forward(duty=100)
    time.sleep(3)
    wc.forward(duty=0)
    print("done")

finally:
    print("fin")
    GPIO.cleanup()