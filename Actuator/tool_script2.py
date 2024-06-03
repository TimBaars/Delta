import RPi.GPIO as gpio
import time

in1 = 13
in2 = 12
in3 = 11
in4 = 10

speedPinA = 6
speedPinB = 5

# Setup GPIO mode
gpio.setmode(gpio.BCM)

# Setup pin modes
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(speedPinA, gpio.OUT)
gpio.setup(speedPinB, gpio.OUT)

# Initial states
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.HIGH)
gpio.output(in3, gpio.HIGH)
gpio.output(in4, gpio.HIGH)

# Setup PWM
pwmA = gpio.PWM(speedPinA, 1000) # 1000 Hz frequency
pwmB = gpio.PWM(speedPinB, 1000) # 1000 Hz frequency

pwmA.start(0) # Start PWM with 0% duty cycle
pwmB.start(0) # Start PWM with 0% duty cycle

def mRight(pin1, pin2):
    gpio.output(pin1, gpio.HIGH)
    gpio.output(pin2, gpio.LOW)
    
def mLeft(pin1, pin2):
    gpio.output(pin1, gpio.LOW)
    gpio.output(pin2, gpio.HIGH)
    
def mStop(pin1, pin2):
    gpio.output(pin1, gpio.HIGH)
    gpio.output(pin2, gpio.HIGH)
    
def mSetSpeed(pwm, speedValue):
    pwm.ChangeDutyCycle(speedValue)
    
try:
    while True:
        mRight(in1, in2)
        mRight(in3, in4)
        
        '''
        Assuming analogRead(A0) equivalent is some input function in python
        For example, a potentiometer connected to an ADC
        Here, we'll just simulate with a value
        '''
        
        n = 50 # Simulate an analog read value scaled to 0-100
        mSetSpeed(pwmA, n)
        mSetSpeed(pwmB, n)
        time.sleep(1) # Add some delay to simulate the loop
        
        mLeft(in1, in2)
        mLeft(in3, in4)

        time.sleep(1)

        mStop(in1, in2)
        mStop(in3, in4)
        
except Exception as e:
    print("Program interrupted:", e)
except KeyboardInterrupt:
    pass    

finally:
    pwmA.stop()
    pwmB.stop()
    gpio.cleanup()