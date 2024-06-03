from time import sleep
import RPi.GPIO as gpio

direction_pin = 20
puls_pin = 21
cw_direction = 0
ccw_direction = 1
ENA = 3 
IN1 = 8
IN2 = 9
    

gpio.setmode(gpio.BCM)
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)
gpio.output(direction_pin, cw_direction)
gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(ENA, gpio.OUT)


#we need to have 3 functions. one to go up and down by __ mm. one to start drill and one to stop drill.
distance = 0 
try:
    distance = 15
    
    gpio.output(IN1, gpio.HIGH)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 200)
    sleep(2)
    
    #Switch on the drill
    gpio.output(IN1, gpio.HIGH)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 200)
    print('direction CW')
    sleep(.5)
    gpio.output(direction_pin, cw_direction)
    for x in range(distance):
        gpio.output(puls_pin, gpio.HIGH)
        sleep(.001)
        gpio.output(puls_pin, gpio.LOW)
        sleep(.0005)
           
    print('Direction CCW')
    sleep(.5)
    gpio.output(direction_pin, ccw_direction)
    for x in range(distance):
        gpio.output(puls_pin, gpio.HIGH)
        sleep(.001)
        gpio.output(puls_pin, gpio.LOW)
        sleep(.0005)
        
    gpio.output(IN1, gpio.LOW)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 0)     
        
    
    gpio.cleanup()
    
    #After block is finished turn off the drill
    
    
         
except KeyboardInterrupt:
    gpio.cleanup()
