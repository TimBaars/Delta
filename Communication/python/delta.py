import random
import sys
import os

# Append the current main directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Delta_Control.igus_modbus import Robot

class Delta:
    def __init__(self, ip_address="192.168.3.11", port=502):
        self.robot = Robot(ip_address, port)
        if not self.robot.is_connected:
            raise ConnectionError(f"Failed to connect to Delta Robot at {ip_address}:{port}")

    def run(self, channel):
        # Declare an exchange
        exchange_name = "delta"
        exchange_type = "fanout"
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Function to get the current position of the Delta robot
        def get_current_position():
            position = self.robot.get_position_endeffector()
            moving = self.robot.is_moving()
            return {
                "position": {
                    "x": position[0],
                    "y": position[1],
                    "z": position[2]
                },
                "moving": "true" if moving else "false"
            }

        message = get_current_position()

        channel.basic_publish(exchange=exchange_name, routing_key='', body=str(message))
        print(f" [D] Sent {message}")