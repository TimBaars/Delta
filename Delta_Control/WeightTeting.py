import time, sys
import csv

sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory
from Delta_Control.igus_modbus import Robot

class DeltaRobotDriver:
    def __init__(self, ip_address, port=502, height=200):
        self.robot = Robot(ip_address, port)
        self.height = height
        self.robot.enable()
        if not self.robot.is_referenced():
            self.robot.reference()
            print("------------------------- Referencing robot -------------------------")
            time.sleep(20)
            print("Referenced robot")

    def drive_to_location_and_wait(self, x, y, z):
        self.robot.set_position_endeffector(x, y, z)
        self.robot.move_endeffector()
        while self.robot.is_moving():
            time.sleep(0.1)

    def set_speed(self, speed):
        self.robot.set_velocity(speed)

    def execute_path(self, speed):
        self.set_speed(speed)
        positions = [(200, 200), (200, -200), (-200, -200), (-200, 200), (200, 200)]
        start_time = time.time()
        for x, y in positions:
            self.drive_to_location_and_wait(x, y, self.height)
        end_time = time.time()
        return end_time - start_time

    def shutdown_robot(self):
        self.robot.disable()

if __name__ == "__main__":
    try:
        speeds = [200, 400, 600, 800]
        times = []

        weight_kg = input("Enter the weight in kilograms: ")

        robot_driver = DeltaRobotDriver("192.168.3.11")
        try:
            for speed in speeds:
                time_taken = robot_driver.execute_path(speed)
                times.append(time_taken)
                print(f"Speed: {speed} mm/s, Time: {time_taken:.2f} seconds")
        finally:
            robot_driver.shutdown_robot()

        # Write data to CSV
        with open('robot_speeds_times.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Check if the file is empty to decide whether to write headers
            file.seek(0, 2)  # Move to the end of the file
            if file.tell() == 0:  # Check if the file is empty
                writer.writerow(['Speed (mm/s)', 'Time (seconds)', 'Weight (kg)'])
            for speed, time_taken in zip(speeds, times):
                writer.writerow([speed, time_taken, weight_kg])
        print("Data appended to robot_speeds_times.csv.")

    except KeyboardInterrupt:
        print("Exiting")
        robot_driver.shutdown_robot()
