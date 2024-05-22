import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

class PathOptimizer:
    """
    This class optimizes a path to avoid black pixels in an image.
    """

    def __init__(self):
        """
        Initializes the optimizer.
        """
        self.image = None

    def load_image(self, image_path):
        """
        Loads an image from the specified path and converts it to a NumPy array.

        Args:
            image_path: The path to the image file.

        Raises:
            ValueError: If the image cannot be loaded.
        """
        try:
            image = Image.open(image_path).convert('L')  # Convert to grayscale
            self.image = np.array(image)
        except Exception as e:
            raise ValueError(f"Failed to load image: {e}")

    def set_image(self, image):
        """
        Sets the image data for the optimizer.

        Args:
            image: A 2D NumPy array representing the image, where True indicates black pixels.
        """
        self.image = image

    def is_visible(self, p1, p2):
        """
        Checks if the line segment from p1 to p2 is visible in the image.

        Args:
            p1: A tuple representing a point (x, y).
            p2: A tuple representing a point (x, y).

        Returns:
            True if the line segment is visible, False otherwise.
        """
        x1, y1 = int(p1[0]), int(p1[1])
        x2, y2 = int(p2[0]), int(p2[1])
        num_points = max(abs(x2 - x1), abs(y2 - y1)) + 1

        x_coords = np.linspace(x1, x2, num_points).astype(int)
        y_coords = np.linspace(y1, y2, num_points).astype(int)

        for x, y in zip(x_coords, y_coords):
            if x < 0 or x >= self.image.shape[1] or y < 0 or y >= self.image.shape[0] or self.image[y, x] == 0:
                return False
        return True

    def optimize_path(self, path):
        """
        Optimizes the path to avoid black pixels in the image.

        Args:
            path: A list of tuples representing points (x, y) in the path.

        Returns:
            A list of tuples representing the optimized path.
        """
        if self.image is None:
            raise ValueError("Image not set. Please use set_image(image) before calling optimize_path.")

        optimized_path = [path[0]]  # Always include the first point
        current_index = 0

        for i in range(1, len(path)):
            if not self.is_visible(optimized_path[-1], path[i]):
                optimized_path.append(path[i - 1])
                current_index = i - 1

        optimized_path.append(path[-1])  # Always include the last point
        return optimized_path

    def visualize_path(self, path, optimized_path=None, original_image=None):
        """
        Visualizes the original and optimized paths on the image.

        Args:
            path: A list of tuples representing the original path points (x, y).
            optimized_path: A list of tuples representing the optimized path points (x, y).
            original_image: Optional original color image for visualization overlay.
        """
        if original_image is not None:
            image_color = original_image
        else:
            image_color = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        # Draw the original path in red
        for i in range(len(path) - 1):
            cv2.line(image_color, (int(path[i][0]), int(path[i][1])), (int(path[i + 1][0]), int(path[i + 1][1])),
                     (0, 0, 255), 2)

        # Draw the optimized path in green if available
        if optimized_path:
            for i in range(len(optimized_path) - 1):
                cv2.line(image_color, (int(optimized_path[i][0]), int(optimized_path[i][1])),
                         (int(optimized_path[i + 1][0]), int(optimized_path[i + 1][1])), (0, 255, 0), 2)

        #plt.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
        #plt.axis("off")
        #plt.show()
        cv2.imwrite("/var/www/html/images/optimized_path.jpg", image_color)

# # Example usage
# if __name__ == "__main__":
#     optimizer = PathOptimizer()
#     optimizer.load_image("Pathplanning/temp.jpg")

#     path = [(0, 0), (89.58567538648958, 44.434297176241174), (186.51265549025769, 69.0343079072092),
#             (277.95350941045626, 109.51356474753302), (253.88255398349355, 206.57328401785225),
#             (348.2872728357661, 239.5543249114228), (446.26569960570504, 259.56002129239664),
#             (507.2925624016569, 338.77947608277043), (533.1131524803211, 435.3884670100624),
#             (632.9123293532482, 441.72284112959636), (697.5708179848444, 518.0070455750629),
#             (781.7868614297224, 571.9297497588333), (876.7385931739244, 603.3012119303212),
#             (957.7089381228778, 661.9851385103268), (978.585130214481, 759.7817877563746),
#             (907.9854882400024, 830.6033279336076), (873.9002778401567, 924.6150209935577),
#             (867.7893667664416, 1024.428130181926), (812.2354510078317, 1107.5771677222683),
#             (847.4583230593768, 1201.168563076972), (1435, 1290)]

#     optimized_path = optimizer.optimize_path(path)
#     optimizer.visualize_path(path, optimized_path)