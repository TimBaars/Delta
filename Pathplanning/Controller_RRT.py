import logging
import traceback
import cv2
import os
import sys

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s, %(filename)s, %(lineno)d, %(message)s')

sys.path.append('/home/koen/git/Delta/')  # Replace with the actual path to the Delta directory
from Pathplanning.RRT.rrt import RRT
from Pathplanning.Converting import SegmentationProcessor
from Delta_Control.Deltacontroldriver import DeltaRobotDriver
from Pathplanning.PathOptimize import PathOptimizer
from functions import convert_nodes_to_flat_list, convert_to_tuples

target_width = 300
target_height = 300

class Controller_RRT:
    def __init__(self):
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
        # Printing errors from delta robot
        print(self.robot_driver.get_errors)
        try:
            print("Starting the process")

            # First, get the weed centers
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
            camera information from another group is needed for this part
            """

            # Move the robot to the calculated path
            for path in scaled_paths:
                for position in path:
                    x, y = position
                    print(f"Moving to: {x}, {y}")  # Optional: print the target position for debugging
                    self.robot_driver.drive_to_location_and_wait(x, y, 100, self.robot_velocity)  # Command the robot to move to the new position

            print("Path traversal complete.")

        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside run", exc_info=exc_info)
            print("Error inside run")
            traceback.print_exc()

    def calculate_path(self, weed_centers, image):
        """Calculate the path from the start to the endpoint using the provided image.

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
            cv2.imwrite("Pathplanning/temp.jpg", img_color)
            for coordinates in weed_centers:
                # Create coords list for the current start and end position
                self.Calculating_Coords[0] = self.start_x
                self.Calculating_Coords[1] = self.start_y
                self.Calculating_Coords[2] = int(coordinates[0])
                self.Calculating_Coords[3] = int(coordinates[1])
                print(f"Planning algorithm from {self.Calculating_Coords[0]}, {self.Calculating_Coords[1]} to {self.Calculating_Coords[2]}, {self.Calculating_Coords[3]}")
                x_list = []
                y_list = [] 
                # Run the RRT algorithm
                _, x_list, y_list = self.RRT_Algorithm.RRT(img_gray, img_color, self.Calculating_Coords, self.stepSize)
                if x_list and y_list is None:
                    print("No path found")
                x_list.insert(0, self.Calculating_Coords[0])
                y_list.insert(0, self.Calculating_Coords[1])
                x_list.append(self.Calculating_Coords[2])
                y_list.append(self.Calculating_Coords[3])
                #print(f"Path nodes: X = {x_list}, Y = {y_list} and length = {len(x_list)}, {len(y_list)}")
                # Convert nodes to flat list
                flat_nodes = convert_to_tuples(x_list, y_list)
                print(f"Flat Path: {flat_nodes}")

                # Optimize the path
                self.optimizer.load_image("Pathplanning/out.jpg")
                optimized_nodes = self.optimizer.optimize_path(flat_nodes)
                self.optimizer.visualize_path(flat_nodes, optimized_nodes)
                print(f"Optimized Path: {optimized_nodes}")
                # Update the start coordinates
                self.start_x = int(coordinates[0])
                self.start_y = int(coordinates[1])

                # Append optimized nodes to path coordinates
                path_coordinates.extend(optimized_nodes)

            return path_coordinates

        except Exception as e:
            # Improved error handling
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
            scaled_paths = []
            difference = 150
            for path in nodes:  # Assuming 'nodes' is a list of tuples [(x1, y1), (x2, y2), ...]
                scaled_path = [(x * scale_factor_x - difference, y * scale_factor_y - difference) for x, y in path]
                scaled_paths.append(scaled_path)
            return scaled_paths
