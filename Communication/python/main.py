import random
import time
import pika

# Establish a connection to RabbitMQ server
# host = '192.168.178.170'
host = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('rabbitmq', 'orangepi')))

# Create a channel
channel = connection.channel()

# Declare an exchange
exchange_name = "actuator"
exchange_type = "fanout"
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

# Publish messages to the exchange
# Define the parameters and their ranges
position_x_range = (0, 100)
position_y_range = (0, 100)
position_z_range = (50, 100)
drilling_range = ('true', 'false')
extend_range = (0, 100)
angle_x_range = (-45, 45)
angle_y_range = (-45, 45)

# Function to generate a message with randomized values
def generate_random_message():
    position = {
        "x": random.randint(*position_x_range),
        "y": random.randint(*position_y_range),
        "z": random.randint(*position_z_range)
    }
    drilling = random.choice(drilling_range)
    extend = random.randint(*extend_range)
    angle = {
        "x": random.randint(*angle_x_range),
        "y": random.randint(*angle_y_range)
    }
    return {
        "position": position,
        "drilling": drilling,
        "extend": extend,
        "angle": angle
    }

# Main loop to send messages every 0.5 seconds
x = 0

while x < 100:
    message = generate_random_message()
    # Assuming exchange_name is defined elsewhere in your code
    channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
    print(f" [x] Sent {message}")
    
    # Wait for 0.5 seconds before sending the next message
    time.sleep(0.5)
    x += 1

# Close the connection
connection.close()
