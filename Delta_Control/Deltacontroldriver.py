import sys

sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory
from igus_modbus import Robot  
import time

class DeltaRobotDriver:
    def __init__(self, ip_address, port=502):
        """
        Initialize the Delta Robot Driver.
        
        :param ip_address: IP address of the Delta Robot Modbus server.
        :param port: Port of the Modbus server (default is 502).
        """
        self.robot = Robot(ip_address, port)
        self.robot.enable()  # Make sure to enable the robot before any operations

    def drive_to_location(self, x, y, z, velocity=None):
        """
        Drive the delta robot to a specified Cartesian location.

        :param x: X position in millimeters.
        :param y: Y position in millimeters.
        :param z: Z position in millimeters.
        :param velocity: Optional movement velocity in mm/s.
        """
        if velocity:
            self.robot.set_velocity(velocity)
        self.robot.set_position_endeffector(x, y, z)
        self.robot.move_endeffector()

    def drive_to_location_and_wait(self, x, y, z, velocity=None):
        """
        Drive the delta robot to a location and wait until it reaches that location.

        :param x: X position in millimeters.
        :param y: Y position in millimeters.
        :param z: Z position in millimeters.
        :param velocity: Optional movement velocity in mm/s.
        """
        self.drive_to_location(x, y, z, velocity)
        while self.robot.is_moving():
            time.sleep(0.1)  # Polling interval to check if the robot is still moving

    def get_current_position(self):
        """
        Get the current Cartesian position of the delta robot's end effector.

        :return: A tuple of (x, y, z) positions in millimeters.
        """
        return self.robot.get_position_endeffector()

    def shutdown_robot(self):
        """
        Properly shutdown the robot.
        """
        self.robot.disable()  # Ensure to disable the robot when done

# Example usage:
if __name__ == "__main__":
    robot_driver = DeltaRobotDriver(ip_address="192.168.1.11")
    robot_driver.drive_to_location_and_wait(100, 100, 200, velocity=120)
    print("Reached the destination.")
    print(f"Current Position: {robot_driver.get_current_position()}")
    robot_driver.shutdown_robot()
