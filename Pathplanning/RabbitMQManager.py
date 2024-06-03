import pika
import json
import time

class RabbitMQManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RabbitMQManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', username='guest', password='guest'):
        if self._initialized:
            return
        self.host = host
        self.username = username
        self.password = password
        self._connection = None
        self._channel = None
        self.connect()
        self._initialized = True

    def connect(self):
        while True:
            try:
                print(f"Attempting to connect to RabbitMQ at {self.host}...")
                self._connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=self.host,
                    credentials=pika.PlainCredentials(self.username, self.password)
                ))
                self._channel = self._connection.channel()
                print("Connected to RabbitMQ")
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def close_connection(self):
        if self._channel:
            self._channel.close()
        if self._connection:
            self._connection.close()
        self._connection = None
        self._channel = None

    def setup_consumer(self, exchange_name, callback):
        while True:
            try:
                self._channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
                result = self._channel.queue_declare(queue='', exclusive=True, auto_delete=True)
                queue_name = result.method.queue
                self._channel.queue_bind(exchange=exchange_name, queue=queue_name)
                self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
                break
            except (pika.exceptions.AMQPChannelError, pika.exceptions.AMQPConnectionError) as e:
                print(f"Error setting up consumer: {e}. Reconnecting...")
                self.close_connection()
                self.connect()

    def start_consuming(self):
        while True:
            try:
                print(' [*] Waiting for messages. To exit press CTRL+C')
                self._channel.start_consuming()
            except (pika.exceptions.StreamLostError, pika.exceptions.AMQPConnectionError) as e:
                print(f"Error during consuming: {e}. Reconnecting...")
                self.close_connection()
                self.connect()

    def send_message(self, exchange_name, body):
        while True:
            try:
                message = json.dumps(body)
                self._channel.basic_publish(exchange=exchange_name, routing_key='', body=message)
                break
            except (pika.exceptions.AMQPChannelError, pika.exceptions.AMQPConnectionError) as e:
                print(f"Error sending message: {e}. Reconnecting...")
                self.close_connection()
                self.connect()
