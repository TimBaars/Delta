import logging
import traceback
import cv2
import os
import sys
import time
import threading
from queue import Queue

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

class PathPlanningWorker(threading.Thread):
    def __init__(self, task_queue, result_queue, stepSize, optimizer):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.stepSize = stepSize
        self.optimizer = optimizer

    def run(self):
        while not self.task_queue.empty():
            coords, image = self.task_queue.get()
            try:
                # Convert the input image to grayscale for processing
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # Use the original image for colored visualization purposes
                img_color = image
                path_coordinates = []

                int_coords = list(map(int, coords))
                # Run the RRT algorithm
                rrt_algorithm = RRT()
                _, x_list, y_list = rrt_algorithm.RRT(img_gray, img_color, int_coords, self.stepSize)
                if x_list is None or y_list is None:
                    self.result_queue.put((coords, None))
                    continue

                x_list.insert(0, int_coords[0])
                y_list.insert(0, int_coords[1])
                x_list.append(int_coords[2])
                y_list.append(int_coords[3])

                # Convert nodes to flat list
                flat_nodes = convert_to_tuples(x_list, y_list)

                # Optimize the path
                self.optimizer.load_image("Pathplanning/out.jpg")
                optimized_nodes = self.optimizer.optimize_path(flat_nodes)
                self.optimizer.visualize_path(flat_nodes, optimized_nodes)

                self.result_queue.put((coords, optimized_nodes))

            except Exception as e:
                logging.error("Error inside PathPlanningWorker", exc_info=True)
                self.result_queue.put((coords, None))
            finally:
                self.task_queue.task_done()

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
        self.initial_start_x = 0  # Initial start coordinates
        self.initial_start_y = 0
        self.start_x = self.initial_start_x  # These will be updated as the robot moves
        self.start_y = self.initial_start_y

        # Variables
        self.stepSize = 100  # stepsize for RRT
        self.Calculating_Coords = [0, 0, 0, 0]
        self.robot_velocity = 750

        # Setup of classes
        self.processor = SegmentationProcessor(txt_path, img_path)
        self.optimizer = PathOptimizer()
        self.robot_driver = DeltaRobotDriver(ip_address="192.168.3.11")

    def run(self):
        """Starting the process"""
        # Printing errors from delta robot
        print(self.robot_driver.get_errors())
        try:
            print("Starting the process")

            # First, get the weed centers
            weed_centers, image = self.processor.process_segmentation_file()

            # Prepare task queue and result queue
            task_queue = Queue()
            result_queue = Queue()

            current_x, current_y = self.initial_start_x, self.initial_start_y
            for weed_center in weed_centers:
                coords = [current_x, current_y, int(weed_center[0]), int(weed_center[1])]
                task_queue.put((coords, image))
                current_x, current_y = int(weed_center[0]), int(weed_center[1])

            # Start worker threads
            for _ in range(4):  # Number of worker threads
                worker = PathPlanningWorker(task_queue, result_queue, self.stepSize, self.optimizer)
                worker.setDaemon(True)
                worker.start()

            # Process paths as they become ready
            last_coords = None
            while not task_queue.empty() or not result_queue.empty():
                try:
                    coords, path = result_queue.get(timeout=1)  # Wait for a path to become available
                    if path:
                        if last_coords is not None:
                            while coords[0] != last_coords[2] or coords[1] != last_coords[3]:
                                time.sleep(0.1)  # Wait until previous path is traversed

                        # Scale the coordinates
                        scaled_path = self.scale_coordinates(path, target_width / image.shape[1], target_height / image.shape[0])
                        print(f"Scaled path: {scaled_path}")

                        # Move the robot to each point in the scaled path
                        for position in scaled_path:
                            x, y = position
                            print(f"Moving to: {x}, {y}")
                            self.robot_driver.drive_to_location_and_wait(x, y, 100, self.robot_velocity)

                        last_coords = coords

                except Queue.Empty:
                    continue

            print("Path traversal complete.")
            # Reinitialize the start coordinates for the next run
            self.start_x = self.initial_start_x
            self.start_y = self.initial_start_y

        except Exception:
            exc_info = sys.exc_info()  # Get current exception info
            logging.error("Error inside run", exc_info=exc_info)
            print("Error inside run")
            traceback.print_exc()

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
if __name__ == "__main__":
    controller = Controller_RRT()
    controller.run()
