import random
import time

class GroundTruth:
    def run(self, channel):
        # Declare an exchange
        exchange_name = "ground_truth"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish messages to the exchange
        # Define the parameters and their ranges
        endpoint = "http://192.168.178.170/images/ground_truth_image.png"
        now = time.time()
        

        # Function to generate a message with randomized values
        def generate_random_message():
            return {
                "url": endpoint,
                "time": now
            }

        message = generate_random_message()

        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [G] Sent {message}")
