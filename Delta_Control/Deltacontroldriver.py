from Delta_Control.igus_modbus import Robot  
import time

class DeltaRobotDriver:
    def __init__(self, ip_address, port=502):
        """
        Initialize the Delta Robot Driver. And reference the delta robot
        
        :param ip_address: IP address of the Delta Robot Modbus server.
        :param port: Port of the Modbus server (default is 502).
        """
        self.robot = Robot(ip_address, port)

        self.robot.enable()  # Make sure to enable the robot before any operations
        self.robot.set_override_velocity(100)
        print("------------------------- Enabling robot -------------------------")
        if self.robot.is_referenced() is False:
            self.robot.reference()
            print("------------------------- Referencing robot -------------------------")
            while self.robot.is_referenced() is False:        
                print("Referenced robot")   

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

    def set_digital_output(self, output_number, value):
        """
        Set a digital output on the robot.

        :param output_number: The number of the output to set.
        :param value: The value to set the output to (0 or 1).
        """
        self.robot.set_digital_output(output_number, value)

    def get_errors(self):
        """
        Get the current error codes from the robot.

        :return: A list of error codes.
        """
        return self.robot.get_robot_errors()