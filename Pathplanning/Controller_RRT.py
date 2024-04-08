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

class Controller_RRT():
    def __init__(self) -> None:
        try:
            os.system("rm -rf Pathplanning/media")
        except:
            print("Dir already clean")
            os.mkdir("Pathplanning/media")
        # Placeholders for testing replace with actual implentation with other group
        number = 6 #random.randint(1, 18)
        txt_path = f'Pathplanning/Paths/BLP0000{number}.txt'
        img_path = f'Pathplanning/Paths/BLP0000{number}.jpg'
        self.start_x = 500 # Needs to be determined when working with the robot.
        self.start_y = 500 # Needs to be determined when working with the robot.

        # Variables
        self.stepSize = 100  # stepsize for RRT
        self.Calculating_Coords = [0,0,0,0]
        self.node_list = [0]

        # Setup of classes
        self.processor = SegmentationProcessor(txt_path, img_path)
    
    def run(self):
        """Starting the process"""
        try: 
            print("Starting the process")

            # First get the weed centers
            weed_centers, image = self.processor.process_segmentation_file()

            # Run the RRT network
            self.calculate_path(weed_centers, image)

            # Convert the path to delta locations
            """ TODO , camera information from other group is needed for this part"""

            # Drive the delta robot to the calculated path
            """ TODO integrate the delta robot"""

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

        except Exception as e:
            # Improved error handling
            logging.error("Error inside calculate_path", exc_info=True)
            print(f"Error inside calculate path: {e}")
