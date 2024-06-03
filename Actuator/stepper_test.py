from time import sleep
import RPi.GPIO as gpio

direction_pin = 20
puls_pin = 21
cw_direction = 0
ccw_direction = 1

gpio.setmode(gpio.BCM)
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)
gpio.output(direction_pin, cw_direction)

try:
    #for y in range(20):
    while True:
        print('direction CW')
        sleep(.5)
        gpio.output(direction_pin, cw_direction)
        for x in range(20):
            gpio.output(puls_pin, gpio.HIGH)
            sleep(.001)
            gpio.output(puls_pin, gpio.LOW)
            sleep(.0005)
        
        print('Direction CCW')
        sleep(.5)
        gpio.output(direction_pin, ccw_direction)
        for x in range(20):
            gpio.output(puls_pin, gpio.HIGH)
            sleep(.001)
            gpio.output(puls_pin, gpio.LOW)
            sleep(.0005)
        sleep(1)
        
except KeyboardInterrupt:
    gpio.cleanup()