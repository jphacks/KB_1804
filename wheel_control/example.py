from wheel_control_rpi_class import WheelControl
import RPi.GPIO as GPIO
import time

try:
    wc = WheelControl()
    wc.forward(duty=100)
    time.sleep(1)
    wc.backward(duty=100)
    time.sleep(1)
    wc.rotate_left(duty=50)
    time.sleep(1)
    wc.rotate_right(duty=50)
    time.sleep(1)
    wc.stop()
    
    print("done")

finally:
    print("fin")
    GPIO.cleanup()
