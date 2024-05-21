import random
import time
import pika

# Establish a connection to RabbitMQ server
host = '192.168.178.107'
credentials = pika.PlainCredentials('rabbitmq', 'orangepi')
parameters = pika.ConnectionParameters(host=host, credentials=credentials)
connection = pika.BlockingConnection(parameters)

# Create a channel
channel = connection.channel()

# Declare an exchange
exchange_name = "system"
exchange_type = "fanout"
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

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
    return {
        "position": position,
        "drilling": drilling,
        "extended": extended,
        "angle": angle,
        "running": running
    }

# Main loop to send messages every 0.5 seconds
x = 0
while x < 100:
    message = generate_random_message()
    channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
    print(f" [x] Sent {message}")
    
    time.sleep(0.5)
    x += 1

# Declare a queue
queue_name = 'queueName'
channel.queue_declare(queue=queue_name)

# Bind the queue to the exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name)

# Callback function to process incoming messages
def callback(ch, method, properties, body):
    print("Received %r" % body)

# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
# Blocking call to wait for messages
channel.start_consuming()
