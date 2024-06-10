from time import sleep
import RPi.GPIO as gpio
import time

direction_pin = 20
puls_pin = 21
cw_direction = 0
ccw_direction = 1

# Setup
gpio.setmode(gpio.BCM)
buttonPin = 23  # GPIO pin number for GPIO 23
gpio.setup(buttonPin, gpio.IN, pull_up_down=gpio.PUD_UP)

def read_with_debounce(pin, debounce_time=0.05):
    current_state = gpio.input(pin)
    time.sleep(debounce_time)
    next_state = gpio.input(pin)
    return current_state if current_state == next_state else None


gpio.setmode(gpio.BCM)
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)
gpio.output(direction_pin, cw_direction)

gpio.setup(buttonPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)

try:
    #for y in range(20):
    while True:
        print('direction CW')
        sleep(.5)
        gpio.output(direction_pin, cw_direction)
        while True:
            gpio.output(puls_pin, gpio.HIGH)
            sleep(.001)
            gpio.output(puls_pin, gpio.LOW)
            sleep(.0005)

            state = read_with_debounce(buttonPin)
            if state is True:
                print("button pressed")
                break
        
        print('Direction CCW')
        sleep(.5)
        gpio.output(direction_pin, ccw_direction)
        for x in range(30):
            gpio.output(puls_pin, gpio.HIGH)
            sleep(.001)
            gpio.output(puls_pin, gpio.LOW)
            sleep(.0005)
        sleep(1)
        
except KeyboardInterrupt:
    gpio.cleanup()
