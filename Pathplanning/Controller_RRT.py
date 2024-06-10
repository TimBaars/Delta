import json
import logging
import threading
import traceback
import cv2
import os
import sys
import time
import random

from Pathplanning.RabbitMQConsumer import RabbitMQConsumer
from Pathplanning.RabbitMQManager import RabbitMQManager
from Pathplanning.StatusManager import StatusManager

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s, %(filename)s, %(lineno)d, %(message)s')

sys.path.append('/home/koen/git/Delta/')  # Replace with the actual path to the Delta directory
from Pathplanning.RRT.rrt import RRT
from Pathplanning.Converting import SegmentationProcessor
from Delta_Control.Deltacontroldriver import DeltaRobotDriver
from Pathplanning.PathOptimize import PathOptimizer
from functions import convert_nodes_to_flat_list, convert_to_tuples

target_width = 250
target_height = 250

class Controller_RRT:
    def sendRobotUpdate(self):
        current_position = None
        try:
            current_position = self.robot_driver.get_current_position()
        except Exception as e:
            print(f"Error in getting current position: {e}")
        if current_position is None or len(current_position) < 3:
            current_position = [9999, 9999, 9999]
        mapping = ["x", "y", "z"]
        position = {mapping[i]: current_position[i] for i in range(3)}
        print(f"status = {self.status}")
        status = self.status  # TODO get actual status [awaiting_actuator, moving, searching_path, shutdown]
        velocity = self.robot_velocity if self.status == "moving" else 0  # TODO get actual velocity
        mapping = ["from_x", "from_y", "to_x", "to_y"]
        direction = {mapping[i]: self.Calculating_Coords[i] for i in range(4)}  # TODO get actual direction

        # turn message into JSON
        message = json.dumps({"position": position, "status": status, "velocity": velocity, "direction": direction})
        self.sender.send_message('delta', message)

    def sendActuatorStart(self):
        self.actuator_status_manager.update_status(True)

        message = json.dumps({"running": "true"})
        self.sender.send_message('actuator', message)

    def sendImageUpdate(self, location):
        date = time.gmtime()
        endpoint = f"http://192.168.201.254/images/{location}.jpg"

        # turn message into JSON
        message = json.dumps({"url": endpoint, "date": date})
        self.sender.send_message(location, message)

    def sendMessages(self, image_name):
        self.sendRobotUpdate()
        self.sendImageUpdate(image_name)

    def sendDataUpdate(self):
        while True:
            system_status_thread = threading.Thread(target=self.system_status_manager.check_status, args=[False])
            system_status_thread.daemon = True
            system_status_thread.start()
            system_status_thread.join()

            self.sendRobotUpdate()
            time.sleep(0.1)

    def __init__(self):
        self.status = "shutdown"
        self.stop = True

        self.sender = RabbitMQManager(host='192.168.201.254', username='rabbitmq', password='pi')
        
        self.system_status_manager = StatusManager(name="system")
        rabbitmq_system_consumer = RabbitMQConsumer(self.system_status_manager, username='python', password='python', exchange_name='system')
        rabbitmq_system_thread = threading.Thread(target=rabbitmq_system_consumer.start_consuming)
        rabbitmq_system_thread.daemon = True
        rabbitmq_system_thread.start()
        
        self.actuator_status_manager = StatusManager(name="actuator")
        rabbitmq_actuator_consumer = RabbitMQConsumer(self.actuator_status_manager, username='actuator', password='actuator', exchange_name='actuator')
        rabbitmq_actuator_thread = threading.Thread(target=rabbitmq_actuator_consumer.start_consuming)
        rabbitmq_actuator_thread.daemon = True
        rabbitmq_actuator_thread.start()

        try:
            os.system("rm -rf Pathplanning/media")
        except:
            print("Dir already clean")
            os.mkdir("Pathplanning/media")
        # Placeholders for testing replace with actual implementation with another group

        # Harder paths
        # self.paths = (3, 4)
        # Easier paths
        self.paths = (1, 2, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18)

        self.number = random.choice(self.paths)
        self.number_str = '{num:0{width}}'.format(num=self.number, width=5)
        txt_path = f'Pathplanning/Paths/BLP{self.number_str}.txt'
        img_path = f'Pathplanning/Paths/BLP{self.number_str}.jpg'
        self.start_x = 0  # Needs to be determined when working with the robot.
        self.start_y = 0  # Needs to be determined when working with the robot.

        # Variables
        self.stepSize = 100  # stepsize for RRT
        self.Calculating_Coords = [0, 0, 0, 0]
        self.robot_velocity = 250

        # Setup of classes
        self.processor = SegmentationProcessor(txt_path, img_path)
        self.RRT_Algorithm = RRT()
        self.optimizer = PathOptimizer()
        self.robot_driver = DeltaRobotDriver(ip_address="192.168.3.11")

        # Constant data updates thread
        self.status = "waiting for start"
        
        # ToDo Make use of this data thread when a more powerful system is available
        # data_update_thread = threading.Thread(target=self.sendDataUpdate)
        # data_update_thread.daemon = True
        # data_update_thread.start()


    def run(self):
        """Starting the process"""

        try:
            self.number = random.choice(self.paths)
            self.number_str = '{num:0{width}}'.format(num=self.number, width=5)
            txt_path = f'Pathplanning/Paths/BLP{self.number_str}.txt'
            img_path = f'Pathplanning/Paths/BLP{self.number_str}.jpg'
            self.processor.txt_path = txt_path
            self.processor.img_path = img_path

            # if self.stop == True:
            # First, get the weed centers
            weed_centers, image = self.processor.process_segmentation_file()

            # Iterate through each weed center, calculate the path, and move the robot
            for weed_center in weed_centers:
                self.status = "searching_path"
                self.sendRobotUpdate()
                # Update the coordinates for the current weed center
                self.Calculating_Coords[0] = self.start_x
                self.Calculating_Coords[1] = self.start_y
                self.Calculating_Coords[2] = int(weed_center[0])
                self.Calculating_Coords[3] = int(weed_center[1])

                # Calculate the path to the current weed center
                path = self.calculate_path(self.Calculating_Coords, image)
                self.status = "optimizing_path"
                # 'planned path ready'
                self.sendMessages("planned_path")

                # If a path is found, scale the coordinates and move the robot
                if path:
                    # Scale the coordinates
                    scaled_path = self.scale_coordinates(path, target_width / image.shape[1], target_height / image.shape[0])
                    self.status = "awaiting_actuator"
                    self.sendMessages("optimized_path")

                    # Check if the system is running
                    if (self.system_status_manager.check_current_status() == False):
                        self.status = "System stopped"
                        self.sendRobotUpdate()

                        system_status_thread = threading.Thread(target=self.system_status_manager.check_status, args=[False])
                        system_status_thread.daemon = True
                        system_status_thread.start()
                        system_status_thread.join()

                    try:
                        # Check if the actuator is ready
                        if (self.system_status_manager.check_current_status() == True):
                            self.status = "Awaiting actuator"
                            self.sendRobotUpdate()
                        
                            actuator_status_thread = threading.Thread(target=self.actuator_status_manager.check_status, args=[True])
                            actuator_status_thread.daemon = True
                            actuator_status_thread.start()
                            actuator_status_thread.join()

                        # Check if the system is running
                        if (self.system_status_manager.check_current_status() == False):
                            self.status = "System stopped"
                            self.sendRobotUpdate()

                            system_status_thread = threading.Thread(target=self.system_status_manager.check_status, args=[False])
                            system_status_thread.daemon = True
                            system_status_thread.start()
                            system_status_thread.join()
                    except Exception as e:
                        print("Error in checking status:", e)
                    
                    self.status = "moving"
                    self.sendRobotUpdate()

                    for position in scaled_path:
                        x, y = position
                        x = x - (target_width / 2)
                        y = y - (target_height / 2)
                        self.robot_driver.drive_to_location_and_wait(x, y, 275, self.robot_velocity)

                    # Update the start coordinates to the current weed center
                    self.sendActuatorStart()
                    self.status = "Started actuator"
                    self.sendRobotUpdate()
                    self.start_x, self.start_y = weed_center

        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside run", exc_info=exc_info)
            print("Error inside run")
            traceback.print_exc()

    def calculate_path(self, coords, image):
        """Calculate the path from the start to the endpoint using the provided image.

        Args:
            coords (list): List of coordinates [start_x, start_y, end_x, end_y].
            image (numpy.ndarray): The input image, which will be used directly for visualization
                                   and converted to grayscale for processing.
        """
        try:
            # Convert the input image to grayscale for processing
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Use the original image for colored visualization purposes
            img_color = image
            path_coordinates = []
            cv2.imwrite("Pathplanning/temp.jpg", img_color)

            # Ensure coordinates are integers
            int_coords = list(map(int, coords))
            # Run the RRT algorithm
            _, x_list, y_list = self.RRT_Algorithm.RRT(img_gray, img_color, int_coords, self.stepSize)
            if x_list is None or y_list is None:
                print("No path found")
                return []

            x_list.insert(0, int_coords[0])
            y_list.insert(0, int_coords[1])
            x_list.append(int_coords[2])
            y_list.append(int_coords[3])

            # Convert nodes to flat list
            flat_nodes = convert_to_tuples(x_list, y_list)

            # OPTIMIZE the path
            self.optimizer.load_image("Pathplanning/out.jpg")
            optimized_nodes = self.optimizer.optimize_path(flat_nodes)
            self.optimizer.visualize_path(flat_nodes, optimized_nodes)

            return optimized_nodes

        except Exception as e:
            logging.error("Error inside calculate_path", exc_info=True)
            print(f"Error inside calculate path: {e}")
            return []

    def scale_coordinates(self, nodes, scale_factor_x, scale_factor_y):
        """
        Scales down the coordinates of the RRT path.

        Args:
            nodes (list of tuples): The RRT path nodes as a list of (x, y) tuples.
            scale_factor_x (float): Scale factor for the x dimension.
            scale_factor_y (float): Scale factor for the y dimension.

        Returns:
            list: Scaled down coordinates of the RRT path.
        """
        if nodes is not None:
            scaled_path = [(int(x * scale_factor_x), int(y * scale_factor_y)) for x, y in nodes]
            return scaled_path
        return []

# Example run
# if __name__ == "__main__":
#     controller = Controller_RRT()
#     controller.run()
