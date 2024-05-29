import pika
import json

class RabbitMQManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RabbitMQManager, cls).__new__(cls)
            cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, host='localhost', username='guest', password='guest'):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            credentials=pika.PlainCredentials(username, password)
        ))
        self._channel = self._connection.channel()

    def setup_consumer(self, exchange_name, callback):
        # Declare a unique, auto-delete queue
        result = self._channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange
        self._channel.queue_bind(exchange=exchange_name, queue=queue_name)

        # Bind the callback function to the queue
        self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def send_message(self, exchange_name, body):
        # Ensure the body is JSON encoded
        message = json.dumps(body)
        self._channel.basic_publish(exchange=exchange_name, routing_key='', body=message)

    def start_consuming(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()