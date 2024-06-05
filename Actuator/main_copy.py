import json
import threading
from time import sleep
import RPi.GPIO as gpio

from RabbitMQManager import RabbitMQManager
from RabbitMQConsumer import RabbitMQConsumer
from StatusManager import StatusManager

# Stepper Motor Pin Definitions
direction_pin = 20
puls_pin = 21
cw_direction = 0
ccw_direction = 1

# DC Motor Pin Definitions
in1 = 3
in2 = 4 
ena = 2

# Button Pin Definitions
buttonPin = 23

# Setup GPIO mode
gpio.setmode(gpio.BCM)

# Stepper Motor Pin Setup
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)

# DC Motor Pin Setup
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(ena, gpio.OUT)

# Button Pin Setup
gpio.setup(buttonPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Initial states
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.HIGH)
gpio.output(direction_pin, cw_direction)

# Setup PWM
pwm = gpio.PWM(ena, 100) # 100 Hz frequency
pwm.start(75) # Start PWM with 75% duty cycle

# Functions to control DC Motor
def mRight(pin1, pin2):
    print("Turning DC motor right")
    gpio.output(pin1, gpio.HIGH)
    gpio.output(pin2, gpio.LOW)
    
def mLeft(pin1, pin2):
    print("Turning DC motor left")
    gpio.output(pin1, gpio.LOW)
    gpio.output(pin2, gpio.HIGH)
    
def mStop(pin1, pin2):
    print("Stopping DC motor")
    gpio.output(pin1, gpio.LOW)
    gpio.output(pin2, gpio.LOW)

# Move stepper motor down
def stepper_down(stepper_range):
    print("Moving tool down")
    sleep(0.5)
    gpio.output(direction_pin, ccw_direction)
    for x in range(stepper_range):
        gpio.output(puls_pin, gpio.HIGH)
        sleep(.001)
        gpio.output(puls_pin, gpio.LOW)
        sleep(.0005)

# Move stepper motor up 
def stepper_up(stepper_range=0):
    print("Moving tool up")
    sleep(0.5)
    gpio.output(direction_pin, cw_direction)
    
    if stepper_range == 0:
        while True:
            if gpio.input(buttonPin) == gpio.HIGH:
                break
            else:
                gpio.output(puls_pin, gpio.HIGH)
                sleep(.001)
                gpio.output(puls_pin, gpio.LOW)
                sleep(.0005)
    else:    
        for x in range(stepper_range):
            if gpio.input(buttonPin) == gpio.HIGH:
                break
            else:
                gpio.output(puls_pin, gpio.HIGH)
                sleep(.001)
                gpio.output(puls_pin, gpio.LOW)
                sleep(.0005)
        
def down_Logic():
    print("Down logic")
    
    stepper_down(175)
    mRight(in1, in2)
    
    sleep(2)
    mStop(in1, in2)
    
    sleep(0.5)
    mLeft(in1, in2)
    
    sleep(0.5)
    mStop(in1, in2)
    
    
def up_Logic():
    print("Up logic")
    stepper_up()
    sleep(0.5)
    stepper_down(30)
    

# Main Sequence
try:
    # client = RabbitMQManager(host='192.168.201.78', username='rabbitmq', password='pi')
    
    # def delta_callback(ch, method, properties, body):
    #     print(f" [Python] Received from actuator_exchange: {body}")
    #     ch.stop_consuming()
        
    # def receiveDelta():
    #     client.setup_consumer('actuator', delta_callback)
    #     client.start_consuming()

    # status_manager = StatusManager()        

    # rabbitmq_consumer = RabbitMQConsumer(status_manager)
    # rabbitmq_thread = threading.Thread(target=rabbitmq_consumer.start_consuming)
    # rabbitmq_thread.daemon = True
    # rabbitmq_thread.start()

    while True:
        # Check if system is running
        # status_thread = threading.Thread(target=status_manager.check_status, args=[False])
        # status_thread.daemon = True
        # status_thread.start()
        # status_thread.join()

        # # Wait for message from delta that it stopped moving
        # actuator_thread = threading.Thread(target=receiveDelta)
        # actuator_thread.start()
        # actuator_thread.join()

        # Actuator Logic
        # signal = input("Enter command: 1 - move tool up; 2 - spin up DC motor; 3 - move tool down; 4 - button test; 5 - End program: ")
        # if signal == '1':
            # stepper_up(100)
        # elif signal == '2':
            # direction = input("Enter direction of dc motor: 1 - right; 2 - left: ")
            # duration = float(input("Enter duration in seconds to spin up DC motor: "))

            # if direction == '1':
                # mRight(in1, in2)
            # else:
                # mLeft(in1, in2)
            
            # sleep(duration)
            # mStop(in1, in2)
        # elif signal == '3':
            # stepper_down(100)
        # elif signal == '4':
            # print("Testing button")
            # while True:
               	# if gpio.input(buttonPin) == gpio.HIGH:
                    # print("Button was pressed")
                    # break
        # elif signal == '5':
            # print("Ending program")
            # break
        # else:
            # print("Invalid input, please enter valid command")
            
            signal = input("Enter signal: 1 - down logic; 2 - up logic; other - end program: ")
            if signal == '1':
                down_Logic()
            elif signal == '2':
                up_Logic()
            else:
                break
        
        
        # Send message to pathplanning that actuator is ready
        # client.send_message('actuator', {'running': 'false'})
        # print(" [Python] Sent to pathplanning: Actuator is ready")

except Exception as e:
    print("Program interrupted:", e)
except KeyboardInterrupt:
    print("Program interrupted by user")
    pass 

finally:
    pwm.stop()
    gpio.cleanup()
