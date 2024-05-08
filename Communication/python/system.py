import random

class System:
    def run(self, channel):
        # Declare an exchange
        exchange_name = "system"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish messages to the exchange
        # Define the parameters and their ranges
        boolean_def = ('true', 'false')

        # Function to generate a message with randomized values
        def generate_random_message():
            running = random.choice(boolean_def)
            return {
                "running":running
            }

        message = generate_random_message()

        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [A] Sent {message}")