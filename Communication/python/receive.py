import random
import time
import pika

# Establish a connection to RabbitMQ server
host = '192.168.201.254'
exchange_name = "system"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('python', 'python')))

channel = connection.channel()

# Declare a queue
queue_name = 'system'
channel.queue_declare(queue=queue_name)

# Bind the queue to the exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='python')

# Callback function to process incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

    method.ack()

# Bind the callback function to the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
# Blocking call to wait for messages
channel.start_consuming()
