import RPi.GPIO as gpio
import time

in1 = 3
in2 = 4
ena = 2

# Setup GPIO mode
gpio.setmode(gpio.BCM)

# Setup pin modes
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(ena, gpio.OUT)

# Initial states
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.HIGH)

# Setup PWM
pwm = gpio.PWM(ena, 100) # 100 Hz frequency
pwm.start(75) # Start PWM with 75% duty cycle

def mRight(pin1, pin2):
    gpio.output(pin1, gpio.HIGH)
    gpio.output(pin2, gpio.LOW)
    
def mLeft(pin1, pin2):
    gpio.output(pin1, gpio.LOW)
    gpio.output(pin2, gpio.HIGH)
    
def mStop(pin1, pin2):
    gpio.output(pin1, gpio.LOW)
    gpio.output(pin2, gpio.LOW)
    
try:
    while True:
        mRight(in1, in2)
        time.sleep(1)
        
        mLeft(in1, in2)
        time.sleep(1)

        mStop(in1, in2)
        time.sleep(1)
        
except Exception as e:
    print("Program interrupted:", e)
except KeyboardInterrupt:
    print("Program interrupted by user")
    pass    

finally:
    pwm.stop()
    gpio.cleanup()