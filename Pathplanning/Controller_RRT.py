import logging
import traceback
import cv2
import os
import time
import sys
import random

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s, %(filename)s, %(lineno)d, %(message)s')

sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory
from Pathplanning.RRT.rrt import RRT
from Pathplanning.Converting import SegmentationProcessor
from Delta_Control.Deltacontroldriver import DeltaRobotDriver

target_width = 300
target_height = 300

class Controller_RRT():
    def __init__(self) -> None:
        try:
            os.system("rm -rf Pathplanning/media")
        except:
            print("Dir already clean")
            os.mkdir("Pathplanning/media")
        # Placeholders for testing replace with actual implentation with other group
        self.number = 4 #random.randint(1, 18)
        txt_path = f'Pathplanning/Paths/BLP0000{self.number}.txt'
        img_path = f'Pathplanning/Paths/BLP0000{self.number}.jpg'
        self.start_x = 0 # Needs to be determined when working with the robot.
        self.start_y = 0 # Needs to be determined when working with the robot.

        # Variables
        self.stepSize = 100  # stepsize for RRT
        self.Calculating_Coords = [0,0,0,0]
        self.node_list = [0]
        self.robot_velocity = 750

        # Setup of classes
        self.processor = SegmentationProcessor(txt_path, img_path)
        self.robot_driver = DeltaRobotDriver(ip_address="192.168.3.11")
    
    def run(self):
        """Starting the process"""
        # Printing errors from delta robot
        print(self.robot_driver.get_errors)
        try: 
            print("Starting the process")

            # First get the weed centers
            weed_centers, image = self.processor.process_segmentation_file()

            # Run the RRT network
            nodes = self.calculate_path(weed_centers, image)

            # Convert the path to delta locations
            img = cv2.imread(f"Pathplanning/out.jpg")
            original_height, original_width, _ = img.shape

            # Calculate scale factors
            scale_factor_x = target_width / original_width
            scale_factor_y = target_height / original_height

            scaled_paths = self.scale_coordinates(nodes, scale_factor_x, scale_factor_y)
            print(f"Scaled paths = {scaled_paths}")

            """ TODO ,
            Actual calculation of real camera points with the real coordinates and camera
            camera information from other group is needed for this part
            """

            # Move the robot to the calculated path
            for path in scaled_paths: 
                for position in path: 
                    x, y = position  
                    print(f"Moving to: {x}, {y}")  # Optional: print the target position for debugging
                    self.robot_driver.drive_to_location_and_wait(x, y, 100, self.robot_velocity)  # Command the robot to move to the new position

            print("Path traversal complete.")
            for a in range(64):
                print(f"Setting digital output {a}")
                self.robot_driver.set_digital_output(a,True)
                print(f"After setting true: {self.robot_driver.robot.get_digital_output(a)}")
                time.sleep(2)
                #self.robot_driver.set_digital_output(a,True)
                print(f"After setting false: {self.robot_driver.robot.get_digital_output(a)}")

        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside run", exc_info=exc_info)
            print("Error inside run")
            traceback.print_exc()

    def calculate_path(self, weed_centers, image):
        """Calculate the path from the start to the end point using the provided image.
        
        Args:
            weed_centers (list): List of tuples representing the x, y coordinates of weed centers.
            image (numpy.ndarray): The input image, which will be used directly for visualization
                                and converted to grayscale for processing.
        """
        try:
            # Convert the input image to grayscale for processing
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Use the original image for colored visualization purposes
            img_color = image
            path_coordinates = []

            for coordinates in weed_centers:
                # Create coords list for the current start and end position
                self.Calculating_Coords[0] = self.start_x
                self.Calculating_Coords[1] = self.start_y
                self.Calculating_Coords[2] = int(coordinates[0])
                self.Calculating_Coords[3] = int(coordinates[1])

                RRT_Algorithm = RRT()
                # Run the RRT algorithm
                #print(self.Calculating_Coords)    
                Nodes = RRT_Algorithm.RRT(img_gray, img_color, self.Calculating_Coords, self.stepSize)
                # Optional code for handling path length and simplification commented out

                print(f"Path: {Nodes[-1].parent_x}, {Nodes[-1].parent_y}")
                # Update the start coordinates
                self.start_x = int(coordinates[0])
                self.start_y = int(coordinates[1])
                for node in Nodes:
                    # Append each node's coordinates as a tuple to the list
                    path_coordinates.append((node.parent_x, node.parent_y))
            return path_coordinates
            
        except Exception as e:
            # Improved error handling
            logging.error("Error inside calculate_path", exc_info=True)
            print(f"Error inside calculate path: {e}")

    def scale_coordinates(self, nodes, scale_factor_x, scale_factor_y):
        """
        Scales down the coordinates of the RRT path.
        
        Args:
            nodes (list of lists): The RRT path nodes, where each path is a list of [x, y] coordinates.
            scale_factor_x (float): Scale factor for the x dimension.
            scale_factor_y (float): Scale factor for the y dimension.
        
        Returns:
            list of lists: Scaled down coordinates of the RRT path.
        """
        scaled_paths = []
        difference = 150
        for path in nodes:  # Assuming 'nodes' is a list of paths where each path is a list of [x,y] coordinates.
            scaled_path = [[(x * scale_factor_x)- difference,(y * scale_factor_y)- difference] for x, y in zip(path[0], path[1])]
            scaled_paths.append(scaled_path)
        return scaled_paths


