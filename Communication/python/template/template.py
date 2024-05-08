import random

class Template:
    def run(self, channel):
        # Declare an exchange
        exchange_name = "template"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish messages to the exchange
        # Define the parameters and their ranges
        position_x_range = (0, 100)
        position_y_range = (0, 100)
        position_z_range = (50, 100)
        extend_range = (0, 100)
        angle_x_range = (-45, 45)
        angle_y_range = (-45, 45)
        boolean_def = ('true', 'false')

        # Function to generate a message with randomized values
        def generate_random_message():
            position = {
                "x": random.randint(*position_x_range),
                "y": random.randint(*position_y_range),
                "z": random.randint(*position_z_range)
            }
            moving = random.choice(boolean_def)
            drilling = random.choice(boolean_def)
            extended = random.randint(*extend_range)
            angle = {
                "x": random.randint(*angle_x_range),
                "y": random.randint(*angle_y_range)
            }
            running = random.choice(boolean_def)
            return {
                "position": position,
                "moving": moving,
                "drilling": drilling,
                "extended": extended,
                "angle": angle,
                "running":running
            }

        message = generate_random_message()

        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [T] Sent {message}")