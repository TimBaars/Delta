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
        number = 2 #random.randint(1, 18)
        txt_path = f'Pathplanning/Paths/BLP0000{number}.txt'
        img_path = f'Pathplanning/Paths/BLP0000{number}.jpg'
        self.start_x = 100 # Needs to be determined when working with the robot.
        self.start_y = 100 # Needs to be determined when working with the robot.

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
            weed_centers = self.processor.process_segmentation_file()

            # Run the RRT network
            self.calculate_path(weed_centers)

            # Drive the delta robot to the calculated path
            """ TODO integrate the delta robot"""

        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside run", exc_info=exc_info)
            # Optionally, keep the print statements or handle the error as needed
            print("Error inside run")
            traceback.print_exc()

    def calculate_path(self, weed_centers, imagePath="Pathplanning/bw_output.png"):
        """Calculate the path from the start to the end point"""
        try:
            img = cv2.imread(imagePath, 0)  # load grayscale maze image
            img2 = cv2.imread(imagePath)  # load colored maze image
            for coordinates in weed_centers:
                # Create coords list for the current start and end position
                self.Calculating_Coords[0] = self.start_x
                self.Calculating_Coords[1] = self.start_y
                self.Calculating_Coords[2] = int(coordinates[0])
                self.Calculating_Coords[3] = int(coordinates[1])  

                RRT_Algorithm = RRT()
                # Run the RRT algorithm
                print(self.Calculating_Coords)    
                Nodes = RRT_Algorithm.RRT(img, img2, self.Calculating_Coords, self.stepSize)
                # if len(Nodes) > 2:
                #     print("Lenght bigger then 2")
                #     """ TODO add the simplification of the path"""
                #     #Simplified_Path = Testing.simplify_path(Nodes)
                #     #print(f"Simplified: {Simplified_Path[-1].parent_x}, {Simplified_Path[-1].parent_y}")

                print(f"Path: {Nodes[-1].parent_x}, {Nodes[-1].parent_y}")
                # Update the start coordinates
                self.start_x = int(coordinates[0])
                self.start_y = int(coordinates[1])
        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside calculate_path", exc_info=exc_info)
            # Optionally, keep the print statements or handle the error as needed
            print("Error inside calculate path")
            traceback.print_exc()