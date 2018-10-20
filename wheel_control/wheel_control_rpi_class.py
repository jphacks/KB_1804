import RPi.GPIO as GPIO
import time
# GPIO.setwarnings(False)

class WheelControl:

    def __init__(self):
        self.PWM_A = 12
        self.PWM_B = 32

        self.Ain1, self.Ain2 = 11, 13
        self.Bin1, self.Bin2 = 21, 23
        self.STBY = 40
        self.FREQ_PWM = 8000

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STBY, GPIO.OUT)
        GPIO.setup([self.Ain1,
                    self.Ain2,
                    self.Bin1,
                    self.Bin2],
                   GPIO.OUT)
        GPIO.setup(self.PWM_A,
                   GPIO.OUT)
        GPIO.setup(self.PWM_B,
                   GPIO.OUT)

        self.pwm_A = GPIO.PWM(self.PWM_A, self.FREQ_PWM)
        self.pwm_B = GPIO.PWM(self.PWM_B, self.FREQ_PWM)
        self.pwm_A.start(0)
        self.pwm_B.start(0)
            
    def backward(self, duty):
        GPIO.output(self.STBY, GPIO.HIGH)
        GPIO.output(self.Ain1, GPIO.LOW)
        GPIO.output(self.Ain2, GPIO.HIGH)
        GPIO.output(self.Bin1, GPIO.HIGH)
        GPIO.output(self.Bin2, GPIO.LOW)
        
        self.pwm_A.ChangeDutyCycle(duty)
        self.pwm_B.ChangeDutyCycle(duty)
       
    def forward(self, duty):
        GPIO.output(self.STBY, GPIO.HIGH)
        GPIO.output(self.Ain1, GPIO.HIGH)
        GPIO.output(self.Ain2, GPIO.LOW)
        GPIO.output(self.Bin1, GPIO.LOW)
        GPIO.output(self.Bin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(duty)
        self.pwm_B.ChangeDutyCycle(duty)
        
    def rotate_left(self, duty):
        GPIO.output(self.STBY, GPIO.HIGH)
        GPIO.output(self.Ain1, GPIO.HIGH)
        GPIO.output(self.Ain2, GPIO.LOW)
        GPIO.output(self.Bin1, GPIO.HIGH)
        GPIO.output(self.Bin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(duty)
        self.pwm_B.ChangeDutyCycle(duty)
        
    def rotate_right(self, duty):
        GPIO.output(self.STBY, GPIO.HIGH)
        GPIO.output(self.Ain1, GPIO.LOW)
        GPIO.output(self.Ain2, GPIO.HIGH)
        GPIO.output(self.Bin1, GPIO.LOW)
        GPIO.output(self.Bin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(duty)
        self.pwm_B.ChangeDutyCycle(duty)
        
    def stop(self, ):
        GPIO.output(self.STBY, GPIO.HIGH)
        GPIO.output(self.Ain1, GPIO.LOW)
        GPIO.output(self.Ain2, GPIO.LOW)
        GPIO.output(self.Bin1, GPIO.LOW)
        GPIO.output(self.Bin2, GPIO.LOW)

        self.pwm_A.stop()
        self.pwm_B.stop()

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
