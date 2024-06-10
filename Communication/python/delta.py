import random

class Delta:
    def run(self, channel):
        # Declare an exchange
        exchange_name = "delta"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish messages to the exchange
        # Define the parameters and their ranges
        position_x_range = (0, 100)
        position_y_range = (0, 100)
        position_z_range = (50, 100)
        boolean_def = ('true', 'false')

        # Function to generate a message with randomized values
        def generate_random_message():
            position = {
                "x": random.randint(*position_x_range),
                "y": random.randint(*position_y_range),
                "z": random.randint(*position_z_range)
            }
            direction = {
                "from_x": random.randint(*position_x_range),
                "from_y": random.randint(*position_y_range),
                "to_x": random.randint(*position_x_range),
                "to_y": random.randint(*position_y_range),
            }
            return {
                "position": position,
                "status": "running",
                "velocity": random.randint(0, 750),
                "direction": direction
            }

        message = generate_random_message()

        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [D] Sent {message}")