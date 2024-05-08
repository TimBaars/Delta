import random

class Actuator:
    def run(self, channel):
        # Declare an exchange
        exchange_name = "actuator"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish messages to the exchange
        # Define the parameters and their ranges
        extend_range = (0, 100)
        angle_x_range = (-45, 45)
        angle_y_range = (-45, 45)
        boolean_def = ('true', 'false')

        # Function to generate a message with randomized values
        def generate_random_message():
            drilling = random.choice(boolean_def)
            extended = random.randint(*extend_range)
            angle = {
                "x": random.randint(*angle_x_range),
                "y": random.randint(*angle_y_range)
            }
            return {
                "drilling": drilling,
                "extended": extended,
                "angle": angle,
            }

        message = generate_random_message()
        
        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [A] Sent {message}")