"""
Env 2D
@author: huiming zhou
"""
import cv2

class Env:
    def __init__(self):
        self.x_range = 320  # size of background
        self.y_range = 320
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """
        # Read the grayscale image
        img = cv2.imread('Pathplanning/bw_output.png', cv2.IMREAD_GRAYSCALE)

        # Check if image loading failed
        if img is None:
            print(f"Failed to load image")
            exit()

        # Get the original image dimensions
        orig_height, orig_width = img.shape[:2]

        # Define the desired downscaled dimensions
        new_width = 100
        new_height = 100
        # Calculate the aspect ratio for rescaling
        aspect_ratio = orig_width / orig_height

        # Determine the rescaling method based on aspect ratio
        if aspect_ratio > 1:
            # Wider image, scale based on width
            new_height = int(new_width / aspect_ratio)
        else:
            # Taller image, scale based on height
            new_width = int(new_height * aspect_ratio)

        # Resize the image using interpolation (optional)
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        print(f"Original image shape: {orig_height}x{orig_width}")
        print(f"Resized image shape: {new_height}x{new_width}")

        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))
        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))
        for i in range(y):
            obs.add((x - 1, i))

        for i in range(10, 21):
            obs.add((i, 15))
        for i in range(15):
            obs.add((20, i))

        for i in range(80, 100):
            obs.add((30, i))
        for i in range(16):
            obs.add((40, i))

        return obs

