import json
import threading
from time import sleep
import time
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
    sender = RabbitMQManager(host='192.168.201.254', username='rabbitmq', password='pi')

    # RabbitMQ Functions
    def sendMessage(running, drilling, status):
        timestamp = time.time()

        # turn message into JSON
        message = json.dumps({"running": running, "drilling": drilling, "status": status, "timestamp": timestamp})
        sender.send_message("actuator", message)
    
    system_status_manager = StatusManager(name="system")
    rabbitmq_system_consumer = RabbitMQConsumer(system_status_manager, username='python', password='python', exchange_name='system')
    rabbitmq_system_thread = threading.Thread(target=rabbitmq_system_consumer.start_consuming)
    rabbitmq_system_thread.daemon = True
    rabbitmq_system_thread.start()
    
    actuator_status_manager = StatusManager(name="actuator")
    rabbitmq_actuator_consumer = RabbitMQConsumer(actuator_status_manager, username='actuator', password='actuator', exchange_name='actuator')
    rabbitmq_actuator_thread = threading.Thread(target=rabbitmq_actuator_consumer.start_consuming)
    rabbitmq_actuator_thread.daemon = True
    rabbitmq_actuator_thread.start()

    while True:
        # Check if the system is running
        if (system_status_manager.check_current_status() == False):
            status = "System stopped"

            system_status_thread = threading.Thread(target=system_status_manager.check_status, args=[False])
            system_status_thread.daemon = True
            system_status_thread.start()
            system_status_thread.join()

        # Check if the delta moved to position
        print(f"Actuator status: {actuator_status_manager.check_current_status()}")
        if (system_status_manager.check_current_status() == True):
            status = "Awaiting Delta"
        
            actuator_status_thread = threading.Thread(target=actuator_status_manager.check_status, args=[False])
            actuator_status_thread.daemon = True
            actuator_status_thread.start()
            actuator_status_thread.join()

        # Check if the system is running
        if (system_status_manager.check_current_status() == False):
            status = "System stopped"

            system_status_thread = threading.Thread(target=system_status_manager.check_status, args=[False])
            system_status_thread.daemon = True
            system_status_thread.start()
            system_status_thread.join()

        down_Logic()

        time.sleep(0.5)

        up_Logic()

        status = "Finished important stuff"
        sendMessage(False, False, status)

except Exception as e:
    print("Program interrupted:", e)
except KeyboardInterrupt:
    print("Program interrupted by user")
    pass 

finally:
    pwm.stop()
    gpio.cleanup()
