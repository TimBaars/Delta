import json
import random
import time
import pika

# Establish a connection to RabbitMQ server
host = 'localhost'
exchange_name = "system"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('rabbitmq', 'orangepi')))

# Create a channel
channel = connection.channel()
channel.queue_declare(queue=exchange_name)

# Function to generate a message with randomized values
def generate_random_message():
    position = {
        "x": random.randint(0, 100),
        "y": random.randint(0, 100),
        "z": random.randint(50, 100)
    }
    drilling = random.choice(('true', 'false'))
    extended = random.randint(0, 100)
    angle = {
        "x": random.randint(-45, 45),
        "y": random.randint(-45, 45)
    }
    running = random.choice(('true', 'false'))
    return json.dumps({
        "running": random.choice(('true', 'false')),
    })

# Main loop to send messages every 1.5 seconds
x = 0
while x < 1:
    message = generate_random_message()
    channel.basic_publish(exchange=exchange_name, routing_key='#*', body=str(message), properties=pika.BasicProperties(delivery_mode=2))

    print(f" [x] Sent {message}")
    
    time.sleep(1.5)
    x += 1
