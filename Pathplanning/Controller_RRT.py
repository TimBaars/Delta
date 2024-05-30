import json
import logging
import traceback
import cv2
import os
import sys
import time

from Pathplanning.RabbitMQManager import RabbitMQManager

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
    def system_callback(self, ch, method, properties, body):
        print(f" [Python] Received from system_exchange: {body}")

        self.stop = json.loads(body)['running'] != "true"
        self.status = "shutdown"

    def actuator_callback(self, ch, method, properties, body):
        print(f" [Python] Received from actuator_exchange: {body}")
        
        self.await_actuator = False
        ch.stop_consuming()
    
    def sendRobotUpdate(self):
        current_position = self.robot_driver.get_current_position()
        mapping = ["x", "y", "z"]
        position = {mapping[i]: current_position[i] for i in range(3)}

        status = self.status # TODO get actual status [awaiting_actuator, moving, searching_path, shutdown]
        velocity = self.robot_velocity # TODO get actual velocity
        
        mapping = ["from_x", "from_y", "to_x", "to_y"]
        direction = {mapping[i]: self.Calculating_Coords[i] for i in range(4)} # TODO get actual direction

        # turn message into JSON
        message = json.dumps({"position": position, "status": status, "velocity": velocity, "direction": direction})

        self.manager.send_message('delta', message)
    
    def sendImageUpdate(self, location):
        date = time.gmtime()
        endpoint = f"http://192.168.201.78/images/{location}.jpg"

        # turn message into JSON
        message = json.dumps({"url": endpoint, "date": date})

        self.manager.send_message(location, message)
    
    def sendMessages(self, image_name):
        self.sendRobotUpdate()
        self.sendImageUpdate(image_name)

    def receiveActuator(self):
        self.await_actuator = True
        self.manager.setup_consumer('actuator', self.actuator_callback)
        self.manager.start_consuming()

        # while (self.await_actuator):
        #     print("Waiting for actuator...")
        #     time.sleep(0.1)

        # ToDo threading and listening
        # self.actuator_callback(None, None, None, None)
        return True

    def __init__(self):
        self.status = "shutdown"
        self.stop = True
        self.manager = RabbitMQManager(host='192.168.201.78', username='python', password='python')
        self.manager.setup_consumer('system', self.system_callback)
        
        try:
            os.system("rm -rf Pathplanning/media")
        except:
            print("Dir already clean")
            os.mkdir("Pathplanning/media")
        # Placeholders for testing replace with actual implementation with another group
        self.number = 4  # random.randint(1, 18)
        txt_path = f'Pathplanning/Paths/BLP0000{self.number}.txt'
        img_path = f'Pathplanning/Paths/BLP0000{self.number}.jpg'
        self.start_x = 0  # Needs to be determined when working with the robot.
        self.start_y = 0  # Needs to be determined when working with the robot.

        # Variables
        self.stepSize = 100  # stepsize for RRT
        self.Calculating_Coords = [0, 0, 0, 0]
        self.robot_velocity = 750

        # Setup of classes
        self.processor = SegmentationProcessor(txt_path, img_path)
        self.RRT_Algorithm = RRT()
        self.optimizer = PathOptimizer()
        self.robot_driver = DeltaRobotDriver(ip_address="192.168.3.11")

    def run(self):
        """Starting the process"""
        try:
            if self.stop == True:
                print("Starting the process")

                # First, get the weed centers
                weed_centers, image = self.processor.process_segmentation_file()

                # Iterate through each weed center, calculate the path, and move the robot
                for weed_center in weed_centers:
                    # Update the coordinates for the current weed center
                    self.Calculating_Coords[0] = self.start_x
                    self.Calculating_Coords[1] = self.start_y
                    self.Calculating_Coords[2] = int(weed_center[0])
                    self.Calculating_Coords[3] = int(weed_center[1])

                    # Calculate the path to the current weed center
                    path = self.calculate_path(self.Calculating_Coords, image)
                    self.status = "searching_path"
                    # 'planned path ready'
                    self.sendMessages("planned_path")
                    
                    # If a path is found, scale the coordinates and move the robot
                    if path:
                        # Scale the coordinates
                        scaled_path = self.scale_coordinates(path, target_width / image.shape[1], target_height / image.shape[0])
                        #print(f"Scaled path: {scaled_path}")
                        # 'optimized path ready'
                        self.sendMessages("optimized_path")

                        # TODO add wait for go to next path message = Communication.recieve('topic')
                        # Move the robot to each point in the scaled path
                        # TODO addition of the time
                        self.status = "awaiting_actuator"

                        if self.receiveActuator():
                            self.status = "moving"

                            for position in scaled_path:
                                x, y = position
                                x = x - (target_width/2)
                                y = y - (target_height/2)
                                print(f"Moving to: {x}, {y}")
                                # time.sleep(1) # TODO remove the sleep
                                self.robot_driver.drive_to_location_and_wait(x, y, 200, self.robot_velocity)

                            # Update the start coordinates to the current weed center
                            self.start_x, self.start_y = weed_center

                            # TODO Wait for feedback before continuing to the next path
                            # while not self.robot_driver.get_feedback_ready():
                            #     print("Waiting for feedback...")
                            #     time.sleep(1)
                            print("Point traversal complete.")
                print("Path traversal complete.")

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

            print(f"Planning algorithm from {coords[0]}, {coords[1]} to {coords[2]}, {coords[3]}")
            x_list = []
            y_list = []
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
            #print(f"Flat Path: {flat_nodes}")

            # OPTIMIZE the path
            self.optimizer.load_image("Pathplanning/out.jpg")
            optimized_nodes = self.optimizer.optimize_path(flat_nodes)
            self.optimizer.visualize_path(flat_nodes, optimized_nodes)
            #print(f"Optimized Path: {optimized_nodes}")

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
