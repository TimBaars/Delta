import json
import pika

from RabbitMQManager import RabbitMQManager

class RabbitMQConsumer:
    def __init__(self, status_manager, host="192.168.201.78", username='python', password='python', exchange_name='system'):
        self.status_manager = status_manager
        self.host = host
        self.username = username
        self.password = password
        self.exchange_name = exchange_name

    def start_consuming(self):
        print("Starting RabbitMQ consumer")
        manager = RabbitMQManager(host=self.host, username=self.username, password=self.password)

        def callback(ch, method, properties, body):
            print("received - " + str(body))
            message = json.loads(body)
            runningData = message['running']
            new_status = runningData == True or runningData == 'true' or runningData.lower() == 'true'
            self.status_manager.update_status(new_status)

        manager.setup_consumer(self.exchange_name, callback)
        print("Started consuming RabbitMQ messages")
        manager.start_consuming()