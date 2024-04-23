from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

# Load the image
image_path = 'images/RRT.jpg'
image = cv2.imread(image_path)

# Convert the image to RGB (OpenCV uses BGR by default)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define the range for red color in RGB
lower_red = np.array([150, 0, 0])
upper_red = np.array([255, 100, 100])

# Create a mask for red color
mask = cv2.inRange(image_rgb, lower_red, upper_red)

# Find the contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the centroids of the red dots and store them
red_dot_locations = []
for cnt in contours:
    # Compute the center of the contour
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        red_dot_locations.append((cX, cY))

# Assuming the image is a top-down view, we'll treat the x and y coordinates from the image as x and y in 3D space.
# The z-coordinate will be set to zero for all points.

# Now, we'll plot these points in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Unpack the red dot locations into their respective lists
xs, ys = zip(*red_dot_locations)
zs = [0] * len(xs)  # All points are on the z=0 plane

# Plot each red dot
ax.scatter(xs, ys, zs, c='r', marker='o', s=50)

# Plot a box with a width and height of 500mm (we assume the pixels to mm conversion is 1 to 1)
# For demonstration, the center of the box will be the mean of the red dot coordinates
center_x, center_y = np.mean(xs), np.mean(ys)
box_half_size = 250  # Half of 500mm for width and height

# Create lines for the box
box_xs = [center_x - box_half_size, center_x + box_half_size, center_x + box_half_size, center_x - box_half_size, center_x - box_half_size]
box_ys = [center_y - box_half_size, center_y - box_half_size, center_y + box_half_size, center_y + box_half_size, center_y - box_half_size]
box_zs = [0, 0, 0, 0, 0]

# Plot the box
ax.plot(box_xs, box_ys, box_zs, color='b')

# Set labels and show the plot
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('3D Plot of Red Dots and Center Box')

plt.show()