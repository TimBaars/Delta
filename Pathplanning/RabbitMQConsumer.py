import json
import time
from threading import Thread
from Pathplanning.RabbitMQManager import RabbitMQManager

class RabbitMQConsumer:
    def __init__(self, status_manager, host="192.168.201.78", username='python', password='python', exchange_name='system'):
        self.status_manager = status_manager
        self.host = host
        self.username = username
        self.password = password
        self.exchange_name = exchange_name
        self.manager = RabbitMQManager(host=self.host, username=self.username, password=self.password)
        self.thread = Thread(target=self.start_consuming)
        self.thread.start()

    def start_consuming(self):
        print("Starting RabbitMQ consumer")
        def callback(ch, method, properties, body):
            message = json.loads(body)
            runningData = message.get('running', 'false')
            new_status = runningData == True or runningData == 'true' or runningData.lower() == 'true'
            self.status_manager.update_status(new_status)

        while True:
            try:
                self.manager.setup_consumer(self.exchange_name, callback)
                self.manager.start_consuming()
            except Exception as e:
                print(f"Exception in consumer thread: {e}. Restarting consumer...")
                time.sleep(5)  # Wait before retrying

    def stop_consuming(self):
        if self.manager._channel is not None:
            try:
                self.manager._channel.stop_consuming()
            except Exception as e:
                print(f"Error stopping consumer: {e}")
        if self.manager._connection is not None:
            try:
                self.manager._connection.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
