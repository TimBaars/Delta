from pyModbusTCP.client import ModbusClient
# Configuration
ROBOT_IP = '192.168.3.1'
PORT = 502  # Default Modbus TCP port

def main():
    # Create a Modbus client
    client = ModbusClient(ROBOT_IP, port=PORT)

    try:
        # Attempt to connect to the robot
        connection = client.is_open
        client.write_single_coil(52, False)
        client.write_single_coil(52,True)
        client.write_single_coil(53, False)
        client.write_single_coil(53, True)
        client.write_single_coil(60, False)
        client.write_single_coil(60, True)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main()

# from Modbus.src.igus_modbus import Robot

# # Configuration
# ROBOT_IP = '192.168.3.1'
# PORT = 502  # Default Modbus TCP port

# def main():
#     """
#     This function creates an instance of the Robot class, establishes a connection to the robot, and executes a predefined sequence of movements.
#     """
#     delta = Robot("192.168.3.1")
#     wait = True

#     if delta.is_connected:
#         print("connected")

# if __name__ == "__main__":
#     main()