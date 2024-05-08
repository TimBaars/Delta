import asyncio
import time
import pika

from actuator import Actuator
from delta import Delta
from masked import Masked
from rrt import Rrt
from system import System

# Establish a connection to RabbitMQ server
host = '192.168.178.170'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('rabbitmq', 'orangepi')))

# Create a channel
channel = connection.channel()

running = True
messages = 10

# Define instances
actuator = Actuator()
delta = Delta()
system = System()
masked = Masked()
rrt = Rrt()

x = 0

# Run the instances
while x < messages:
    actuator.run(channel)
    delta.run(channel)
    system.run(channel)
    masked.run(channel)
    rrt.run(channel)

    x += 1

    time.sleep(0.5)

# Close the connection
connection.close()
