import json
import threading
from time import sleep
import RPi.GPIO as gpio

from RabbitMQManager import RabbitMQManager
from RabbitMQConsumer import RabbitMQConsumer
from StatusManager import StatusManager

# DC Motor Pin Definitions
direction_pin = 20
puls_pin = 21
cw_direction = 0
ccw_direction = 1
ENA = 3
IN1 = 8
IN2 = 9

# Stepper Motor Pin Definitions
in1 = 13
in2 = 12
in3 = 11
in4 = 10
speedPinA = 6
speedPinB = 5

# Setup GPIO mode
gpio.setmode(gpio.BCM)

# DC Motor Pin Setup
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)
gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(ENA, gpio.OUT)

# Stepper Motor Pin Setup
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(speedPinA, gpio.OUT)
gpio.setup(speedPinB, gpio.OUT)

# Initial statesimport json
import threading
from time import sleep
import RPi.GPIO as gpio

from RabbitMQManager import RabbitMQManager
from RabbitMQConsumer import RabbitMQConsumer
from StatusManager import StatusManager
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.HIGH)
gpio.output(in3, gpio.HIGH)
gpio.output(in4, gpio.HIGH)

# Setup PWM for Stepper Motor
pwmA = gpio.PWM(speedPinA, 1000)  # 1000 Hz frequency
pwmB = gpio.PWM(speedPinB, 1000)  # 1000 Hz frequency
pwmA.start(0)  # Start PWM with 0% duty cycle
pwmB.start(0)  # Start PWM with 0% duty cycle

# Functions to control Stepper Motor
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

def stepper_down():
    # Move stepper motor down
    mRight(in1, in2)
    mRight(in3, in4)
    mSetSpeed(pwmA, 50)  # Example speed value
    mSetSpeed(pwmB, 50)
    sleep(1)  # Adjust time as needed
    mStop(in1, in2)
    mStop(in3, in4)
    mSetSpeed(pwmA, 0)
    mSetSpeed(pwmB, 0)
 


def stepper_up():
    # Move stepper motor up
    mLeft(in1, in2)
    mLeft(in3, in4)
    mSetSpeed(pwmA, 50)  # Example speed value
    mSetSpeed(pwmB, 50)
    sleep(1)  # Adjust time as needed
    mStop(in1, in2)
    mStop(in3, in4)
    mSetSpeed(pwmA, 0)
    mSetSpeed(pwmB, 0)

# Functions to control DC Motor
def dc_motor_spin(direction, duration):
    gpio.output(IN1, gpio.HIGH)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 200)  # Adjust speed as needed
    gpio.output(direction_pin, direction)
    sleep(duration)
    gpio.output(IN1, gpio.LOW)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 0)

def dc_motor_spin_up(duration):
    dc_motor_spin(cw_direction, duration)  # Spin for the given duration

def dc_motor_stop():
    gpio.output(IN1, gpio.LOW)
    gpio.output(IN2, gpio.LOW)
    gpio.output(ENA, 0)

# Main Sequence
try:
    client = RabbitMQManager(host='192.168.201.78', username='rabbitmq', password='pi')
    
    def delta_callback(ch, method, properties, body):
        print(f" [Python] Received from actuator_exchange: {body}")
        ch.stop_consuming()
        
    def receiveDelta():
        client.setup_consumer('actuator', delta_callback)
        client.start_consuming()

    status_manager = StatusManager()        

    rabbitmq_consumer = RabbitMQConsumer(status_manager)
    rabbitmq_thread = threading.Thread(target=rabbitmq_consumer.start_consuming)
    rabbitmq_thread.daemon = True
    rabbitmq_thread.start()

    while True:
        # Check if system is running
        status_thread = threading.Thread(target=status_manager.check_status, args=[False])
        status_thread.daemon = True
        status_thread.start()
        status_thread.join()

        # Wait for message from delta that it stopped moving
        actuator_thread = threading.Thread(target=receiveDelta)
        actuator_thread.start()
        actuator_thread.join()

        # Enable drill
        # Move actuator down
            # Wait for movement to finish

        # ...?

        # Move actuator up
            # Wait for movement to finish
        # Disable drill

        # Send message to pathplanning that actuator is ready
        client.send_message('actuator', {'running': 'false'})
        print(" [Python] Sent to pathplanning: Actuator is ready")
        
        if (gpio.input(23)==gpio.HIGH):
                stepper_up()
        signal = input("Enter 1 to move stepper motor up, 2 to spin up DC motor or 3 to stepper down")
        if signal == '1':
            stepper_up()
        elif signal == '2':
            duration = float(input("Enter duration to spin up DC motor (in seconds): "))
            dc_motor_spin_up(duration)
            dc_motor_stop()
        elif signal == '3':
            stepper_down()
        else:
            print("Invalid input, please enter 1 or 2.")

except KeyboardInterrupt:
    pass

finally:
    pwmA.stop()
    pwmB.stop()
    gpio.cleanup()
