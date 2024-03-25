import cv2
import os
import time
import sys
sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory
from Pathplanning.RRT.rrt import RRT


def display_image(window_name, img_path, wait_time=500):
    """
    Displays an image in a window.
    :param window_name: Name of the window in which the image will be displayed.
    :param img_path: Path to the image file.
    :param wait_time: Time in milliseconds for which the image is displayed.
    """
    img = cv2.imread(img_path)
    cv2.imshow(window_name, img)
    cv2.waitKey(wait_time)

if __name__ == '__main__':
    Testing = RRT()
    imagePath = "Pathplanning/RRT/world3.png"
    stepSize = 50  # stepsize for RRT

    # remove previously stored data
    try:
        os.system("rm -rf Pathplanning/media")
    except:
        print("Dir already clean")
    os.mkdir("Pathplanning/media")

    img = cv2.imread(imagePath, 0)  # load grayscale maze image
    img2 = cv2.imread(imagePath)  # load colored maze image

    # Define a sequence of coordinates (startX, startY, endX, endY)
    coordinate_sequence = [
        (10, 10, 500, 250),  # First set of coordinates
        (500, 250, 250, 250)  # Second set of coordinates
    ]

    for coordinates in coordinate_sequence:
        # Run the RRT algorithm
        fps = time.time()
        Testing.RRT(img, img2, coordinates, stepSize)
        print(f"Total time for processing = {time.time() - fps} seconds")

        # Assuming the output image is saved at PathPlanning/media/1.jpg after each RRT run
        # Display the updated path in a live window
        display_image("RRT Path Planning", "PathPlanning/media/1.jpg", 2000)  # Adjust wait_time as needed

    cv2.destroyAllWindows()  # Close the window when all paths are planned