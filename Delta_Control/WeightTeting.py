from Delta_Control.igus_modbus import Robot
import time

class DeltaRobotDriver:
    def __init__(self, ip_address, port=502, height=250):
        """
        Initialize the Delta Robot Driver. And reference the delta robot

        :param ip_address: IP address of the Delta Robot Modbus server.
        :param port: Port of the Modbus server (default is 502).
        :param height: Fixed height for the robot operations.
        """
        self.robot = Robot(ip_address, port)
        self.height = height
        self.speed = 100  # Default speed, can be adjusted with set_speed method

        self.robot.enable()  # Make sure to enable the robot before any operations
        self.robot.set_override_velocity(self.speed)
        if self.robot.is_referenced() is False:
            self.robot.reference()
            print("------------------------- Referencing robot -------------------------")
            time.sleep(20)
            print("Referenced robot")

    def drive_to_location_and_wait(self, x, y, z):
        """
        Drive the delta robot to a location and wait until it reaches that location.

        :param x: X position in millimeters.
        :param y: Y position in millimeters.
        :param z: Z position in millimeters.
        """
        self.robot.set_position_endeffector(x, y, z)
        self.robot.move_endeffector()
        while self.robot.is_moving():
            time.sleep(0.1)  # Polling interval to check if the robot is still moving

    def set_speed(self, speed):
        """
        Set the movement speed of the robot.

        :param speed: Speed in mm/s.
        """
        self.speed = speed

    def execute_path(self):
        """
        Execute a predefined path of positions.
        """
        positions = [(250, 250), (250, -250), (-250, -250), (-250, 250), (250, 250)]
        start_time = time.time()

        for x, y in positions:
            self.drive_to_location_and_wait(x, y, self.height)
        
        end_time = time.time()
        print(f"Completed path in {end_time - start_time:.2f} seconds.")

    def shutdown_robot(self):
        """
        Properly shutdown the robot.
        """
        self.robot.disable()  # Ensure to disable the robot when done

# Example usage
if __name__ == "__main__":
    robot_driver = DeltaRobotDriver("192.168.1.11")
    robot_driver.execute_path()
    robot_driver.shutdown_robot()
