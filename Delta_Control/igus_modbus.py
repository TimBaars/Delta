# {{{ Description
"""
igus_modbus Module
==================

Author: 
     Yaman Alsaady

Description:
    This module provides a Python interface for controlling a Delta Robot (from igus) using Modbus TCP communication.

Classes:
    - Robot: Represents the Robot and provides methods for controlling it.

Usage:
    To use this module, create an instance of the 'Robot' class with the IP address and the port of the Robot as a parameter.

Example:
    from igus_modbus import Robot
    
    # Create a Delta Robot instance with the IP address '192.168.1.11'
    delta_robot = Robot('192.168.3.11')
    
    # Perform actions with the Delta Robot
    delta_robot.enable()\n
    delta_robot.reference()\n
    delta_robot.set_position_endeffector(0, 0, 250)\n
    delta_robot.set_velocity(120)\n
    delta_robot.move_endeffector_absolute()\n

"""
# }}}

# {{{ Import
from time import sleep, time
from pyModbusTCP.client import ModbusClient
from ctypes import c_int32
from math import sin, cos, radians
from numpy import arange

# }}}


# {{{ Init
class Robot:
    is_connected = False
    break_time = 5

    def __init__(self, address: str, port: int = 502):
        """
        Initialize a Robot instance and establish the communication

        :param address: The IP address of the Robot.
        :type address: str
        :param port: The port for Modbus TCP communication (default is 502).
        :type port: int
        """
        self.address = address
        self.client = ModbusClient(host=address, port=port, timeout=1)
        self.is_connected = self.client.open()
        if self.is_connected:
            self.client.write_single_coil(134, False)
            self.client.write_single_coil(134, True)

    def __del__(self):
        """
        Close current TCP connection.

        :return: None
        """
        self.set_globale_signal(6, False)
        self.client.close()

    # }}}

    # {{{ Robot Control
    def shutdown(self):
        """
        Reset the Delta Robot.

        This method shut the robot down by writing a rising edge to the coil.

        :return: None
        """
        if not self.is_connected:
            return -1
        self.client.write_single_coil(51, False)
        self.client.write_single_coil(51, True)

    def reset(self):
        """
        Reset the Delta Robot.

        This method resets the robot by writing a rising edge to the coil.

        :return: None
        """
        if not self.is_connected:
            return
        self.controll_programs("stop")
        self.client.write_single_coil(52, False)
        self.client.write_single_coil(52, True)

    def enable(self):
        """
        Enable the motors of the Robot.

        This method enables the motors of the robot by writing 1 the coil 53.

        :return: None
        """
        if not self.is_connected:
            return
        if not self.is_enabled():
            self.client.write_single_coil(53, False)
        self.client.write_single_coil(53, True)
        sleep(0.1)
        return self.is_enabled()

    def disable(self):
        """
        Disable the motors of the Robot.

        This method disables the motors of the robot by writing 0 to the coil 53.

        :return: None
        """
        if not self.is_connected:
            return
        if self.is_enabled():
            self.client.write_single_coil(53, False)
        self.client.write_single_coil(53, True)
        sleep(0.1)

    def reference(self, force: bool = False):
        """
        Reference the Robot.

        This method references the robot by writing a rising edge to the coil 60.
        If 'only_once' is set to True (default), it will only reference the robot if it's not already referenced.

        :param force: If False, the robot will only be referenced if not already referenced,
                         otherwise, it will be referenced each time this method is called (default is False).
        :type force: bool
        :return: None
        """
        if not self.is_connected:
            return
        timeout = time() + self.break_time
        self.enable()
        if force:
            self.client.write_single_coil(60, False)
            self.client.write_single_coil(60, True)
            sleep(0.3)
            while not self.is_referenced():
                if time() > timeout:
                    break
            return
        else:
            if not self.is_referenced():
                self.client.write_single_coil(60, False)
                self.client.write_single_coil(60, True)
                sleep(0.3)
                while not self.is_referenced():
                    if time() > timeout:
                        break
            else:
                return

    # }}}

    # {{{ Info
    def is_enabled(self):
        """
        Check if the Robot is enabled.

        This method checks the state of the Robot's motors by reading coil 53.

        :return: True if the motors are enabled, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(53)[0]:
            return True
        else:
            return False

    def is_referenced(self):
        """
        Check if the Robot is referenced.

        This method checks if the Robot has been referenced by reading coil 60.

        :return: True if the Robot is referenced, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(60)[0]:
            return True
        else:
            return False

    def is_moving(self):
        """
        Check if the Robot is moving.

        This method checks the state of the Robot's motion by reading coil 112.

        :return: True if the Robot is currently moving, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(112)[0]:
            return True
        else:
            return False

    def is_general_error(self):
        """
        Check if the robot has general errors.

        This method checks the state of the robot's error status coil
        and returns True if the robot has general errors, or False if
        there are no errors.

        :return: True if the robot has general errors, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(20)[0]:
            return False
        else:
            return True

    def is_kinematics_error(self):
        """
        Check if the robot has kinematics-related errors.

        This method checks the state of the robot's kinematics error status coil
        and returns True if the robot has kinematics-related errors, or False if
        there are no kinematics errors.

        :return: True if the robot has kinematics-related errors, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(37)[0]:
            return False
        else:
            return True

    def is_program_loaded(self):
        """
        Check if a program is loaded.

        This method checks if a program is loaded on the robot controller.

        :return: True if a program is loaded, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(120)[0]:
            return True
        else:
            return False

    def is_zero_torque(self):
        """
        Check if the robot is in a zero torque state.

        This method reads a Modbus coil to determine if the robot is currently in a state
        where it applies zero torque. It returns True if zero torque is detected, False otherwise.

        :return: True if the robot is in a zero torque state, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if self.client.read_coils(111)[0]:
            return True
        else:
            return False

    # }}}

    # {{{ General
    def set_zero_torque(self, enable: bool = True):
        """
        Set the zero torque state for manual movement.

        This method allows you to enable or disable the zero torque state, which allows manual movement of the robot by hand.

        :param enable: True to enable zero torque (for manual movement), False to disable.
        :type enable: bool
        :return: None
        """
        if not self.is_connected:
            return
        if enable & (not self.is_zero_torque()):
            self.client.write_single_coil(111, False)
            self.client.write_single_coil(111, True)
        elif not enable & (self.is_zero_torque()):
            self.client.write_single_coil(111, False)
            self.reset()
            sleep(0.2)
            self.enable()

    def set_override_velocity(self, velocity: float = 20):
        """
        Set the override velocity for robot movements.

        This method allows you to adjust the velocity override for robot movements.
        The `velocity` parameter specifies the desired velocity as a percentage (0-100),
        with 100 being the maximum velocity. The default is 20%.

        :param velocity: The desired velocity override as a percentage (0-100).
        :type velocity: float
        :return: None
        """
        if not self.is_connected:
            return False
        if 0 < velocity <= 100:
            self.client.write_single_register(187, 100 * velocity)
            return True
        return False

    def set_velocity(self, velocity: bool):
        """
        Set the velocity of the Robot.

        This method sets the velocity of the robot in millimeters per second.
        For cartesian motions the value is set as a multiple of 1mm/s,
        for joint motions it is a multiple of 1% (relative to the maximum velocity)
        The actual motion speed also depends on the global override value (holding register 187).

        :param velocity: The desired velocity in millimeters per second (or in percent).
        :type velocity: float
        :return: None
        """
        if not self.is_connected:
            return
        self.client.write_single_register(180, velocity * 10)

    def set_and_move(
        self,
        val_1: float,
        val_2: float,
        val_3: float,
        movement: int = "cartesian",
        relative: str = None,
        wait: bool = True,
        velocity: float = None,
    ):
        """
        Set the target position and move the end effector.

        This method sets the target position of the end effector using the 'set_position_endeffector' method,
        adjusts the velocity if specified, and then moves the end effector to the target position using the 'move_endeffector' method.
        The movement can be relative to different reference frames (base, tool) based on the 'relative' parameter.
        You can choose to wait until the movement is complete before returning.

        :param val_1: The target position value (X, A1, or other axis, depending on the 'movement' parameter).
        :type val_1: float
        :param val_2: The target position value (Y, A2, or other axis, depending on the 'movement' parameter).
        :type val_2: float
        :param val_3: The target position value (Z, A3, or other axis, depending on the 'movement' parameter).
        :type val_3: float
        :param movement: Specifies the type of movement ('cartesian' or 'axes').
        :type movement: str
        :param relative: Specifies the reference frame for the movement (None for absolute, 'base', or 'tool').
        :type relative: str or None
        :param wait: If True (default), wait until the movement is complete before returning.
        :type wait: bool
        :param velocity: Optional velocity setting in millimeters per second.
        :type velocity: float or None
        """
        if not self.is_connected:
            return
        if velocity:
            self.set_velocity(velocity)
        if movement == "cartesian":
            self.set_position_endeffector(val_1, val_2, val_3)
            self.move_endeffector(wait=wait, relative=relative)
        elif movement == "axes":
            self.set_position_axes(val_1, val_2, val_3)
            self.move_axes(wait=wait, relative=relative)
        else:
            return

    # }}}

    # {{{ End effector
    def move_endeffector(self, wait: bool = True, relative: str = None):
        """
        Move the end effector to the target position.

        This method moves the end effector to the specified Cartesian position by controlling the appropriate coil.
        The movement can be relative to different reference frames (base, tool) based on the 'relative' parameter.
        To specify the position, use the method set_position_endeffector(x, y, z).

        :param wait: If True (default), wait until the movement is complete before returning.
        :type wait: bool
        :param relative: Specifies the reference frame for the movement (None for absolute, 'base', or 'tool').
        :type relative: str or None
        """
        if not self.is_connected:
            return False
        timeout = time() + self.break_time
        if wait:
            while self.is_moving():
                if time() > timeout:
                    self.reset()
                    break
                if self.is_general_error():
                    break
                if self.is_kinematics_error():
                    break
        if relative == None:
            self.client.write_single_coil(100, False)
            self.client.write_single_coil(100, True)
        if relative == "base":
            self.client.write_single_coil(101, False)
            self.client.write_single_coil(101, True)
        if relative == "tool":
            self.client.write_single_coil(102, False)
            self.client.write_single_coil(102, True)
        return True


    def set_position_endeffector(self, x_val: float, y_val: float, z_val: float):
        """
        Set the target position of the end effector in millimeters.

        This method sets the target position of the end effector in millimeters. The position can be absolute or relative
        to the base or to itself. To make the robot move to the specified position, use the 'move_endeffector' method.

        :param x_val: The target X position in millimeters.
        :type x_val: float
        :param y_val: The target Y position in millimeters.
        :type y_val: float
        :param z_val: The target Z position in millimeters.
        :type z_val: float
        :return: None
        """
        if not self.is_connected:
            return
        x_val = int(x_val * 100)
        y_val = int(y_val * 100)
        z_val = int(z_val * 100)

        self.client.write_single_register(130, (x_val & 0x0000FFFF))
        self.client.write_single_register(131, (x_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(132, (y_val & 0x0000FFFF))
        self.client.write_single_register(133, (y_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(134, (z_val & 0x0000FFFF))
        self.client.write_single_register(135, (z_val >> 16) & 0x0000FFFF)

    def set_orientation_endeffector(self, a_val: float, b_val: float, c_val: float):
        """
        Set the orientation of the end effector.

        This method allows you to set the orientation of the robot's end effector by specifying the angles
        'a_val', 'b_val', and 'c_val' for orientation around the X, Y, and Z axes, respectively.

        :param a_val: The orientation angle around the X-axis in degrees.
        :type a_val: float
        :param b_val: The orientation angle around the Y-axis in degrees.
        :type b_val: float
        :param c_val: The orientation angle around the Z-axis in degrees.
        :type c_val: float
        :return: None
        """
        if not self.is_connected:
            return
        a_val *= 100
        b_val *= 100
        c_val *= 100
        self.client.write_single_register(130, a_val)
        self.client.write_single_register(132, b_val)
        self.client.write_single_register(134, c_val)

    def get_position_endeffector(self):
        """
        Get the Cartesian position of the Delta Robot's end effector.
        This method reads the X, Y, and Z positions of the end effector from input registers and returns them in millimeters as a tuple.

        :return: A list (x_pos, y_pos, z_pos) representing the Cartesian position of the end effector in millimeters.
        :rtype: list[float]
        """
        if not self.is_connected:
            return []
        # Read the X, Y, and Z positions from input registers
        x_pos = self.client.read_input_registers(130)[0]
        x_pos2 = self.client.read_input_registers(131)[0]
        y_pos = self.client.read_input_registers(132)[0]
        y_pos2 = self.client.read_input_registers(133)[0]
        z_pos = self.client.read_input_registers(134)[0]
        z_pos2 = self.client.read_input_registers(135)[0]
        # Combine the two 16-bit values into a 32-bit integer for each position
        x_pos = c_int32(x_pos | (x_pos2 << 16)).value / 100
        y_pos = c_int32(y_pos | (y_pos2 << 16)).value / 100
        z_pos = c_int32(z_pos | (z_pos2 << 16)).value / 100
        return [x_pos, y_pos, z_pos]

    def get_orientation_endeffector(self):
        """
        Get the orientation of the Delta Robot's end effector.

        This method reads the orientation values from input registers and returns them.

        :return: A list (a, b, c) representing the orientation values.
        :rtype: list[float]
        """
        if not self.is_connected:
            return []
        a = self.client.read_input_registers(136)[0] / 100
        b = self.client.read_input_registers(138)[0] / 100
        c = self.client.read_input_registers(140)[0] / 100
        return [a, b, c]

    # }}}

    # {{{ Axes
    def move_axes(self, wait: bool = True, relative: str = False):
        """
        Move the end effector to the target position.

        This method moves the end effector to the specified axes position by controlling the appropriate coil.
        The movement can be relative or absolute 'relative' parameter.
        To specify the position, use the method set_position_axes.

        :param wait: If True (default), wait until the movement is complete before returning.
        :type wait: bool
        :param relative: If False (default), the movement will be absolute, otherwise will be relative to the current position
        :type relative: bool
        """
        if not self.is_connected:
            return
        timeout = time() + self.break_time
        if wait:
            while self.is_moving():
                if time() > timeout:
                    self.reset()
                    break
                if self.is_general_error():
                    break
                if self.is_kinematics_error():
                    break
        if relative:
            self.client.write_single_coil(104, False)
            self.client.write_single_coil(104, True)
        else:
            self.client.write_single_coil(103, False)
            self.client.write_single_coil(103, True)

    def set_position_axes(self, a1_val: float, a2_val: float, a3_val: float):
        """
        Set the target position of the endeffector

        This method allows you to set the target positions of the robot's axes.
        The input values 'a1_val', 'a2_val', and 'a3_val' represent the target positions for each axis.
        The positions are converted to the appropriate format and written to the respective registers.

        The position can be absolute or relative.
        To make the robot move, use the method move_axes().

        :param a1_val: The target position for axis A1.
        :type a1_val: float
        :param a2_val: The target position for axis A2.
        :type a2_val: float
        :param a3_val: The target position for axis A3.
        :type a3_val: float
        :return: None
        """
        if not self.is_connected:
            return
        a1_val *= 100
        a2_val *= 100
        a3_val *= 100

        self.client.write_single_register(142, (a1_val & 0x0000FFFF))
        self.client.write_single_register(143, (a1_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(144, (a2_val & 0x0000FFFF))
        self.client.write_single_register(145, (a2_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(146, (a3_val & 0x0000FFFF))
        self.client.write_single_register(147, (a3_val >> 16) & 0x0000FFFF)

    def get_position_axes(self):
        """
        Get the positions of the Delta Robot's axes.

        This method reads the positions of the robot's axes (A1, A2, and A3) from input registers
        and returns them as a tuple.

        :return: A list (a1_pos, a2_pos, a3_pos) representing the positions of the robot's axes.
        :rtype: list[float]
        """
        if not self.is_connected:
            return []
        a1_pos = self.client.read_input_registers(142)[0]
        a1_pos2 = self.client.read_input_registers(143)[0]
        a2_pos = self.client.read_input_registers(144)[0]
        a2_pos2 = self.client.read_input_registers(145)[0]
        a3_pos = self.client.read_input_registers(146)[0]
        a3_pos2 = self.client.read_input_registers(147)[0]

        # Combine the two 16-bit values into a 32-bit integer for each axis
        a1_pos = c_int32(a1_pos | (a1_pos2 << 16)).value / 100
        a2_pos = c_int32(a2_pos | (a2_pos2 << 16)).value / 100
        a3_pos = c_int32(a3_pos | (a3_pos2 << 16)).value / 100
        return [a1_pos, a2_pos, a3_pos]

    # }}}

    # {{{ Programs
    def controll_programs(self, action: str):
        """
        Control robot programs.

        This method allows you to control robot programs by sending specific commands.
        Supported actions are: 'start', 'continue', 'pause', and 'stop'.

        :param action: The action to perform ('start', 'continue', 'pause', or 'stop').
        :type action: str
        """
        if not self.is_connected:
            return False
        if action == "start":
            # self.client.write_single_coil(124, False)
            # self.client.write_single_coil(124, True)
            self.client.write_single_coil(122, False)
            self.client.write_single_coil(122, True)
            return self.get_program_runstate()
        elif action == "continue":
            self.client.write_single_coil(122, False)
            self.client.write_single_coil(122, True)
            return self.get_program_runstate()
        elif action == "pause":
            self.client.write_single_coil(123, False)
            self.client.write_single_coil(123, True)
            return self.get_program_runstate()
        elif action == "stop":
            self.client.write_single_coil(124, False)
            self.client.write_single_coil(124, True)
            return self.get_program_runstate()
        else:
         return False

    def set_program_replay_mode(self, mode: str = "once"):
        """
        Set the program replay mode for the robot.

        This method allows you to configure the program replay mode for the robot.
        The `mode` parameter specifies the desired mode and can take one of the following values:
        - "once" (Default): Play the program once.
        - "repeat": Repeat the program continuously.
        - "step": Step through the program one instruction at a time.
        - "fast": Not used (for future expansion).

        :param mode: The desired program replay mode.
        :type mode: str
        :return: 0 if 
        :rtype: int
        """
        if not self.is_connected:
            return -1
        if mode == "once":
            self.client.write_single_register(261, 0)
            return 0
        elif mode == "repeat":
            return self.client.write_single_register(261, 1)
        elif mode == "step":
            return self.client.write_single_register(261, 2)
        elif mode == "fast":
            return self.client.write_single_register(261, 3)
        else:
            return -2

    def set_program_name(self, name):
        """
        Set the name of the robot program.

        This method allows you to set the name of the robot program.

        :param name: The name of the robot program.
        :type name: str
        """
        if not self.is_connected:
            return False
        self.write_string(name, 267, 31)

    def get_program_name(self):
        """
        Get the name of the robot program.

        This method reads the name of the robot program.

        :return: The name of the robot program.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        read = self.client.read_holding_registers(267, 32)
        return self.read_string(read)

    def get_program_runstate(self):
        """
        Get the current run state of the robot program.

        This method reads the run state of the robot program and returns a descriptive string.
        The possible run states are:
        - "Program is not running": The robot program is not currently executing.
        - "Program is running": The robot program is actively running.
        - "Program is paused": The robot program is paused but can be resumed.

        :return: A descriptive string representing the current run state.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.client.read_holding_registers(260)[0]
        if code == 0:
            return "Program is not running"
        elif code == 1:
            return "Program is running"
        elif code == 2:
            return "Program is paused"
        else:
            return ""

    def get_program_replay_mode(self):
        """
        Get the current replay mode of the robot program.

        This method reads the replay mode of the robot program and returns a descriptive string.
        The possible replay modes are:
        - "Run program once": The robot program will run once and stop.
        - "Repeat program": The robot program will continuously repeat.
        - "Execute instructions step by step": The robot program will execute instructions one at a time.
        - "Fast" (Not used): A mode that is not currently used.

        :return: A descriptive string representing the current replay mode.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.client.read_holding_registers(260)[0]
        if code == 0:
            return "Run program once"
        elif code == 1:
            return "Repeat program"
        elif code == 2:
            return "Execute instructions step by step"
        elif code == 3:
            return "Fast"  # Not used
        else:
            return ""

    def get_number_of_loaded_programs(self):
        """
        Get the number of loaded programs on the Delta Robot.

        This method reads the number of loaded programs on the Delta Robot and returns the count.

        :return: The number of loaded programs.
        :rtype: int
        """
        if not self.is_connected:
            return 0
        return self.client.read_input_registers(262)[0]

    def get_number_of_current_program(self):
        """
        Get the number of currently active programs on the Delta Robot.

        This method reads the number of currently active programs on the Delta Robot and returns the count.
        Note: The main program is typically represented as program number 0.

        :return: The number of currently active programs.
        :rtype: int
        """
        if not self.is_connected:
            return 0
        return self.client.read_input_registers(263)[0]

    # }}}

    # {{{ Signals
    def set_globale_signal(self, number: int, state: bool):
        """
        Set the state of a global signal.

        This method allows you to set the state of a global signal by specifying its number and state.

        :param number: The number of the global signal (1 to 100).
        :type number: int
        :param state: The state to set (True for ON, False for OFF).
        :type state: bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 100:
            self.client.write_single_coil(199 + number, state)

    def set_digital_output(self, number: int, state: bool):
        """
        Set the state of a digital output.

        This method allows you to set the state of a digital output by specifying its number and state.

        :param number: The number of the digital output (1 to 64).
        :type number: int
        :param state: The state to set (True for ON, False for OFF).
        :type state: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.client.write_single_coil(299 + number, state)
        else:
            return False

    def get_globale_signal(self, number: int):
        """
        Get the state of a global signal.

        This method allows you to get the state of a global signal by specifying its number.

        :param number: The number of the global signal (1 to 100).
        :type number: int
        :return: The state of the global signal (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if 1 <= number <= 100:
            return self.client.read_coils(199 + number)[0]
        else:
            return False

    def get_digital_output(self, number):
        """
        Get the state of a digital output.

        This method allows you to get the state of a digital output by specifying its number.

        :param number: The number of the digital output (1 to 64).
        :type number: int
        :return: The state of the digital output (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.client.read_coils(299 + number)[0]
        else:
            return False

    def get_digital_input(self, number: int):
        """
        Get the state of a digital input.

        This method allows you to get the state of a digital input by specifying its number.

        :param number: The number of the digital input (1 to 64).
        :type number: int
        :return: The state of the digital input (True for ON, False for OFF).
        :rtype: bool
        """
        if not self.is_connected:
            return False
        number += 20
        if 1 <= number <= 64:
            return self.client.read_coils(263 + number)[0]
        else:
            return False
        # }}}

    # {{{ Variables
    def set_number_variables(self, number: int = 1, value: int = 0):
        """
        Set the value of a writable Modbus variable.

        This method allows you to set the value of a Modbus variable for program use. Please note that
        the variable name in your program should follow the naming convention: mb_num_w1 - mb_num_w16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :param value: The value to set for the Modbus variable.
        :type value: int
        :return: True if the operation was successful, False if the number is out of range.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 16:
            return self.client.write_single_register(439 + number, value)

    def set_position_variable(
        self,
        number=1,
        movement: str = "cartesian",
        a1: int = None,
        a2: int = None,
        a3: int = None,
        x: int = None,
        y: int = None,
        z: int = None,
        a: int = 0,
        b: int = 0,
        c: int = 180,
        conversion: int = 0,
    ):
        """
        Set the target position for robot movement in a robot program.

        This method allows you to set the target position for robot movement in a program. You can specify
        the target position either in Cartesian or axis values. Ensure the variable name in your program
        follows the naming convention, e.g., mb_pos_w1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :param movement: The type of movement (either "cartesian" or "axes").
        :type movement: str
        :param a1: The value of axis A1 (if movement is "axes").
        :type a1: int
        :param a2: The value of axis A2 (if movement is "axes").
        :type a2: int
        :param a3: The value of axis A3 (if movement is "axes").
        :type a3: int
        :param x: The X-coordinate value (if movement is "cartesian").
        :type x: int
        :param y: The Y-coordinate value (if movement is "cartesian").
        :type y: int
        :param z: The Z-coordinate value (if movement is "cartesian").
        :type z: int
        :param a: The orientation A value (if movement is "cartesian").
        :type a: int
        :param b: The orientation B value (if movement is "cartesian").
        :type b: int
        :param c: The orientation C value (if movement is "cartesian").
        :type c: int
        :param conversion: The conversion type (useful for converting between joint and cartesian positions).
        :type conversion: int
        :return: True if the operation was successful, False if the number is out of range or invalid parameters.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if not (1 <= number <= 16):
            return False
        number = 456 + (16 * (number - 1))
        if movement == "cartesian":
            x *= 10
            y *= 10
            z *= 10
            a *= 10
            b *= 10
            c *= 10
            return self.client.write_multiple_registers(
                number, [0, 0, 0, 0, 0, 0, 0, 0, 0, x, y, z, a, b, c, conversion]
            )
        elif movement == "axes":
            a1 *= 10
            a2 *= 10
            a3 *= 10
            return self.client.write_multiple_registers(
                number, [a1, a2, a3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, conversion]
            )
        else:
            return False

    def get_readable_number_variable(self, number: int):
        """
        Get the value of a readable Modbus variable.

        This method allows you to retrieve the value of a Modbus variable for reading. Please ensure that
        the variable name in your program follows the naming convention: mb_num_r1 - mb_num_r16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: The value of the Modbus variable, or False if the number is out of range.
        :rtype: int or bool
        """
        if not self.is_connected:
            return 0
        if 1 <= number <= 16:
            return self.client.read_input_registers(439 + number)[0]
        else:
            return 0

    def get_writable_number_variable(self, number: int):
        """
        Get the value of a writable Modbus variable.

        This method allows you to retrieve the value of a Modbus variable for writing. Ensure that the
        variable name in your program adheres to the naming convention: mb_num_w1 - mb_num_w16.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: The value of the Modbus variable, or False if the number is out of range.
        :rtype: int or bool
        """
        if not self.is_connected:
            return
        if 1 <= number <= 16:
            return self.client.read_holding_registers(439 + number)[0]
        else:
            return False

    def get_readable_position_variable(self, number: int):
        """
        Get the value of a readable position Modbus variable.

        This method allows you to retrieve the value of a readable position Modbus variable.
        Ensure that the variable name in your program follows the naming convention, e.g., mb_pos_r1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: A list containing axis, cartesian, orientation values, and conversion type,
                 or False if the number is out of range.
        :rtype: list
        """
        if not self.is_connected:
            return []
        if not (1 <= number <= 16):
            return []
        number = 456 + (16 * (number - 1))
        postion = self.client.read_input_registers(number, 16)
        if not postion:
            return []
        axes = {"a1": postion[0], "a2": postion[1], "a3": postion[2]}
        cartesian = {
            "x_val": postion[9],
            "y_val": postion[10],
            "z_val": postion[11],
        }
        orientation = {"a": postion[12], "b": postion[13], "c": postion[14]}
        conversion = postion[15]
        return [axes, cartesian, orientation, conversion]

    def get_writable_position_variable(self, number: int):
        """
        Get the value of a writable position Modbus variable.

        This method allows you to retrieve the value of a writable position Modbus variable.
        Ensure that the variable name in your program follows the naming convention, e.g., mb_pos_w1.

        :param number: The number of the Modbus variable (1 to 16).
        :type number: int
        :return: A list containing axis, cartesian, orientation values, and conversion type,
                 or False if the number is out of range.
        :rtype: list
        """
        if not self.is_connected:
            return []
        if not (1 <= number <= 16):
            return []
        number = 456 + (16 * (number - 1))
        postion = self.client.read_holding_registers(number, 16)
        if not postion:
            return []
        axes = {"a1": postion[0] / 10, "a2": postion[1] / 10, "a3": postion[2] / 10}
        cartesian = {
            "x_val": postion[9] / 10,
            "y_val": postion[10] / 10,
            "z_val": postion[11] / 10,
        }
        orientation = {
            "a": postion[12] / 10,
            "b": postion[13] / 10,
            "c": postion[14] / 10,
        }
        conversion = postion[15]
        return [axes, cartesian, orientation, conversion]

    # }}}

    # {{{ Messages
    def get_info_message(self):
        """
        Get the information or error message from the Delta Robot.

        This method reads the information or error message from the Delta Robot's control unit.
        The message is typically a short text, similar to what is displayed on a manual control unit.

        :return: The information or error message as a string.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        message = self.client.read_holding_registers(400, 32)
        return self.read_string(message)

    def get_robot_errors(self):
        """
        Get a list of error descriptions indicating the robot's current error states.

        This method reads the status of various error-related coils on the robot controller
        and returns a list of error descriptions if any errors are detected.

        :return: A list of error descriptions or "No error" if there are no errors.
        :rtype: list[str]
        """
        if not self.is_connected:
            return []
        errors_list = []

        if not self.is_general_error():
            errors_list.append("No error")
        else:
            if self.client.read_coils(21)[0]:
                errors_list.append("Temperature")
            if self.client.read_coils(22)[0]:
                errors_list.append("Emergency stop")
            if self.client.read_coils(23)[0]:
                errors_list.append("Motor not activated")
            if self.client.read_coils(24)[0]:
                errors_list.append("Communication")
            if self.client.read_coils(25)[0]:
                errors_list.append("Contouring error")
            if self.client.read_coils(26)[0]:
                errors_list.append("Encoder error")
            if self.client.read_coils(27)[0]:
                errors_list.append("Overcurrent")
            if self.client.read_coils(28)[0]:
                errors_list.append("Driver error")
            if self.client.read_coils(29)[0]:
                errors_list.append("Bus dead")
            if self.client.read_coils(30)[0]:
                errors_list.append("Module dead")

        return errors_list

    def get_kinematics_error(self):
        """
        Get the kinematics error description.

        This method reads the kinematics error code from the robot controller and returns a human-readable description of the error.

        :return: A string describing the kinematics error.
        :rtype: str
        """
        if not self.is_connected:
            return "Not connected"
        # code = self.client.read_input_registers(95)[0]
        else:
            if self.client.read_coils(37)[0]:
                return "no error"
            if self.client.read_coils(38)[0]:
                return "Axis limit Min"
            if self.client.read_coils(39)[0]:
                return "Axis limit Max"
            if self.client.read_coils(40)[0]:
                return "Central axis singularity"
            if self.client.read_coils(41)[0]:
                return "Out of range"
            if self.client.read_coils(42)[0]:
                return "Wrist singularity"
            if self.client.read_coils(43)[0]:
                return "Virtual box reached"
            if self.client.read_coils(44)[0]:
                return "Motion not allowed"
            else:
                return "Out of range"

    def get_stop_reason_description(self):
        """
        Get a description of the reason for the robot's current stop condition.

        This method reads the stop reason code from the robot controller and returns a human-readable description of the reason for the stop.

        :return: A string describing the reason for the stop.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.client.read_input_registers(266)[0]
        if code == 0:
            return "User (Teach pendant, CRI, Modbus, etc.)"
        if code == 1:
            return "PLC"
        if code == 2:
            return "Program (stop/pause instruction)"
        if code == 3:
            return "Replay Step (step operation)"
        if code == 4:
            return "Shoutdown (system shuts down)"
        if code == 100:
            return "Error"
        if code == 101:
            return "Path generator error 1"
        if code == 102:
            return "Path generator error 2"
        if code == 103:
            return "Error in state machine"
        else:
            return ""

    def get_operation_mode(self):
        """
        Get the operation mode description.

        This method reads the operation mode code from the robot controller and returns a human-readable description of the mode.

        :return: A string describing the operation mode.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        code = self.client.read_input_registers(96)[0]
        if code == 0:
            return "Standerd - normal operation"
        if code == 1:
            return "Serious error, control must be restarted"
        if code == 2:
            return "CAN-Bridge (CRI, e.g. retrieve firmware parameters)"
        else:
            return ""

    # }}}

    # {{{ Misc
    def move_circular(
        self,
        radius: float,
        step: float = 0.5,
        start_angle: int = 0,
        stop_angle: int = 360,
    ):
        """
        Move the robot's end effector in a circular path.

        This method moves the robot's end effector in a circular path in the X-Y plane.
        The circular path is defined by a radius, and you can specify the step size, start angle, and stop angle.

        :param radius: The radius of the circular path in millimeters.
        :type radius: float
        :param step: The step size in degrees for moving along the circular path (default is 0.5 degrees).
        :type step: float
        :param start_angle: The starting angle of the circular path in degrees (default is 0 degrees).
        :type start_angle: float
        :param stop_angle: The stopping angle of the circular path in degrees (default is 360 degrees).
        :type stop_angle: float
        """
        if not self.is_connected:
            return
        timeout = time() + self.break_time
        while self.is_moving():
            if time() > timeout:
                self.reset()
                break
            if self.is_general_error():
                self.reset()
                break
            if self.is_kinematics_error():
                self.reset()
                break
        x_val, y_val, z_val = self.get_cartesian_position()
        for angle in arange(start_angle, stop_angle, step):
            x = radius * cos(radians(angle)) + x_val
            y = radius * sin(radians(angle)) + y_val
            print(round(x, 2))
            print(round(y, 2))
            self.set_and_move(round(x, 2), round(y, 2), z_val)

    def get_list_of_porgrams(self):
        """
        Get a list of available robot programs.

        This method retrieves a list of robot programs from the robot controller.
        It communicates with the robot controller to gather program names.

        :return: A list of program names.
        :rtype: list
        """
        if not self.is_connected:
            return []
        program_list = []

        num_programs = self.client.read_input_registers(331)[0]

        # Ensure that the list starts from the top by repeatedly navigating to the previous program
        for _ in range(num_programs):
            self.client.write_single_coil(131, False)
            self.client.write_single_coil(131, True)

        # Loop through the program indices
        for _ in range(num_programs):
            program_name = self.read_string(self.client.read_input_registers(333, 32))
            # Remove null characters from the program name
            program_name = str(program_name).replace("\x00", "")
            program_list.append(program_name)

            # Trigger the robot controller to move to the next program
            self.client.write_single_coil(130, False)
            self.client.write_single_coil(130, True)

        return program_list

    def print_list_of_programs(self):
        """
        Print a list of available robot programs.

        This method retrieves a list of robot programs and prints them to the console.
        If the robot is not connected, it will return without performing any action.

        :return: None
        """
        if not self.is_connected:
            return
        list = self.get_list_of_porgrams()
        for count, i in enumerate(list):
            print(count, i)

    def read_string(self, read):
        """
        Read a string from a sequence of registers.

        This method reads a string from a sequence of registers and returns the decoded string.

        :param read: The sequence of registers containing the string data.
        :type read: list
        :return: The decoded string.
        :rtype: str
        """
        if not self.is_connected:
            return ""
        string = ""
        for i in read:
            if i:
                string += chr(i & 0x00FF)
                string += chr(i >> 8)
        return string

    def write_string(self, string, ad, number=32):
        """
        Write a string to a sequence of registers.

        This method allows you to write a string to a sequence of registers, starting from a specified address.

        :param string: The string to write.
        :type string: str
        :param ad: The starting address to write the string.
        :type ad: int
        :param number: The maximum number of characters to write (default is 32).
        :type number: int
        """
        if not self.is_connected:
            return ""
        string = iter(string)
        for count, i in enumerate(string):
            if count == number:
                break
            try:
                val = ord(next(string)) << 8 | ord(i)
            except:
                val = ord(i)
            self.client.write_single_register(count + ad, val)

    def control_gripper(self, opening: int, orientation: int, signal: int = 6):
        """
        Control the gripper using specified values and a Modbus signal.

        :param opening: The value for the gripper opening.
        :type opening: int
        :param orientation: The value for the gripper orientation.
        :type orientation: int
        :param signal: The Modbus signal number to enable/disable gripper control.
                       Default is 6.
        :type signal: int
        :return: True if the gripper control was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        self.set_number_variables(15, opening)
        self.set_number_variables(16, orientation)
        self.set_globale_signal(signal, True)
        sleep(0.2)
        self.set_globale_signal(signal, False)
        return True

    def is_gripper_moving(self):
        return self.get_globale_signal(7)
    
    def change_table_hight(self, direction: int=0,movement_time: int=0, signal: int = 6):
        if not self.is_connected:
            return False
        self.set_number_variables(13, direction)
        self.set_number_variables(14, movement_time)
        self.set_globale_signal(signal, True)
        sleep(0.2)
        self.set_globale_signal(signal, False)
        return True
    # }}}


# vim:foldmethod=marker
