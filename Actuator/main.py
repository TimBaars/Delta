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
in1 = 13
in2 = 12
in3 = 11
in4 = 10
speedPinA = 6
speedPinB = 5

# Other Pin Definitions
ENA = 3
IN1 = 8
IN2 = 9
buttonPin = 23

# Setup GPIO mode
gpio.setmode(gpio.BCM)

# Stepper Motor Pin Setup
gpio.setup(direction_pin, gpio.OUT)
gpio.setup(puls_pin, gpio.OUT)

# DC Motor Pin Setup
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(speedPinA, gpio.OUT)
gpio.setup(speedPinB, gpio.OUT)

# Other Pin Setup
gpio.setup(buttonPin, gpio.OUT)
gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(ENA, gpio.OUT)

# Initial states
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.HIGH)
gpio.output(in3, gpio.HIGH)
gpio.output(in4, gpio.HIGH)
gpio.output(direction_pin, cw_direction)

# Setup PWM
pwmA = gpio.PWM(speedPinA, 1000)  # 1000 Hz frequency
pwmB = gpio.PWM(speedPinB, 1000)  # 1000 Hz frequency
pwmA.start(50)  # Start PWM with 50% duty cycle
pwmB.start(50)  # Start PWM with 50% duty cycle

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

def stepper_down(stepper_range):
    # Move stepper motor down
    # mRight(in1, in2)
    # mRight(in3, in4)
    # mSetSpeed(pwmA, 50)  # Example speed value
    # mSetSpeed(pwmB, 50)
    # sleep(1)  # Adjust time as needed
    # mStop(in1, in2)
    # mStop(in3, in4)
    # mSetSpeed(pwmA, 0)
    # mSetSpeed(pwmB, 0)
    sleep(0.5)
    gpio.output(direction_pin, ccw_direction)
    for x in range(stepper_range):
        gpio.output(puls_pin, gpio.HIGH)
        sleep(.001)
        gpio.output(puls_pin, gpio.LOW)
        sleep(.0005)
 
def stepper_up(stepper_range):
    # Move stepper motor up
    # mLeft(in1, in2)
    # mLeft(in3, in4)
    # mSetSpeed(pwmA, 50)  # Example speed value
    # mSetSpeed(pwmB, 50)
    # sleep(1)  # Adjust time as needed
    # mStop(in1, in2)
    # mStop(in3, in4)
    # mSetSpeed(pwmA, 0)
    # mSetSpeed(pwmB, 0)
    sleep(0.5)
    gpio.output(direction_pin, cw_direction)
    for x in range(stepper_range):
        gpio.output(puls_pin, gpio.HIGH)
        sleep(.001)
        gpio.output(puls_pin, gpio.LOW)
        sleep(.0005)

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
    sender = RabbitMQManager(host='192.168.201.78', username='rabbitmq', password='pi')
    
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

        status = "Doing important stuff"
        sendMessage(True, True, status)

# ToDo Start Example implementation (Done by Tim so needs to be revised by the actuator team)
        
    # Enable drill for x seconds
        dc_motor_thread = threading.Thread(target=dc_motor_spin_up, args=[5])
        dc_motor_thread.daemon = True
        dc_motor_thread.start()

    # Move actuator down
        status = "Moving actuator down"
        sendMessage(True, True, status)
        stepper_down(100)

    # ToDo Run other stuff/wait for a bit,...?
        time.sleep(0.5)

    # Move actuator up
        status = "Moving actuator up"
        sendMessage(True, True, status)
        stepper_up(100)

    # Disable drill
        dc_motor_thread.join()
        dc_motor_stop()

# ToDo End Example implementation (Done by Tim so needs to be revised by the actuator team)

        status = "Finished important stuff"
        sendMessage(False, False, status)

# ToDo Make the actuator do above steps instead of manual input (after testing)
        # if (buttonPin == gpio.HIGH):
        #     stepper_up(20)
        # signal = input("Enter command: 1 - move stepper motor up; 2 - spin up DC motor; 3 - stepper down; 4 - End program: ")
        # if signal == '1':
        #     print("Moving stepper motor up")
        #     stepper_up(100)
        # elif signal == '2':
        #     duration = float(input("Enter duration to spin up DC motor (in seconds): "))
        #     dc_motor_spin_up(duration)
        #     dc_motor_stop()
        # elif signal == '3':
        #     print("Moving stepper motor down")
        #     stepper_down(100)
        # elif signal == '4':
        #     print("Ending program")
        #     break
        # else:
        #     print("Invalid input, please enter 1 or 2.")

except KeyboardInterrupt:
    pass

finally:
    pwmA.stop()
    pwmB.stop()
    gpio.cleanup()