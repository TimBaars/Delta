import threading

from testStatusManager import StatusManager
from testRabbitMQConsumer import RabbitMQConsumer

# Main def
if __name__ == "__main__":
    status_manager = StatusManager()

    rabbitmq_consumer = RabbitMQConsumer(status_manager)
    rabbitmq_thread = threading.Thread(target=rabbitmq_consumer.start_consuming)
    rabbitmq_thread.daemon = True
    rabbitmq_thread.start()

    last_status = False

    while True:
        status_thread = threading.Thread(target=status_manager.check_status, args=[last_status])
        status_thread.daemon = True
        status_thread.start()
        status_thread.join()

        last_status = not last_status