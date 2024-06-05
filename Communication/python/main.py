import time
import pika

from ground_truth import GroundTruth
from actuator import Actuator
from delta import Delta
from masked import Masked
from rrt import Rrt
from system import System

# Establish a connection to RabbitMQ server
host = '192.168.201.254'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('rabbitmq', 'pi')))

# Create a channel
channel = connection.channel()

running = True
messages = 100

# Define instances
actuator = Actuator()
delta = Delta()
system = System()
masked = Masked()
rrt = Rrt()
ground_truth = GroundTruth()

x = 0

# Run the instances
while x < messages:
    actuator.run(channel)
    delta.run(channel)
    system.run(channel)
    masked.run(channel)
    rrt.run(channel)
    ground_truth.run(channel)

    x += 1

    time.sleep(1.5)

# Close the connection
connection.close()
