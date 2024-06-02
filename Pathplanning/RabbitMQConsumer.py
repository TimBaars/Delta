import json
import pika

from RabbitMQManager import RabbitMQManager

class RabbitMQConsumer:
    def __init__(self, status_manager):
        self.status_manager = status_manager

    def start_consuming(self):
        print("Starting RabbitMQ consumer")
        manager = RabbitMQManager()
        connection = RabbitMQManager(host='192.168.201.78', username='python', password='python')

        def callback(ch, method, properties, body):
            print("received - " + str(body))
            message = json.loads(body)
            runningData = message['running']
            new_status = runningData == True or runningData == 'true' or runningData.lower() == 'true'
            self.status_manager.update_status(new_status)

        manager.setup_consumer('system', callback)
        print("Started consuming RabbitMQ messages")
        manager.start_consuming()