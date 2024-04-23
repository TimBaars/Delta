import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Offsets as given in the image
x_offset_camera = 250  # in mm
y_offset_camera = -500  # in mm (assuming down is negative)
z_offset_robot = 200  # in mm

# Coordinates of the camera and the robot center
camera_coords = (x_offset_camera, y_offset_camera, 0)  # Assuming the camera is at z=0
robot_center_coords = (0, 0, z_offset_robot)  # Assuming the robot center is at x=0, y=0

# Create a new matplotlib figure and 3D axes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the camera position
ax.scatter(*camera_coords, color='red', s=100, label='Camera')

# Plot the center of the robot
ax.scatter(*robot_center_coords, color='yellow', s=100, label='Center of Robot')

# Connect the points to show the offset lines
# Line from camera to its projection on the XY plane (vertical line)
ax.plot([camera_coords[0], camera_coords[0]], [camera_coords[1], camera_coords[1]], [0, camera_coords[2]], 'gray', linestyle='--')
# Horizontal line in the XY plane from the projection to the robot center
ax.plot([camera_coords[0], robot_center_coords[0]], [camera_coords[1], robot_center_coords[1]], [0, 0], 'gray', linestyle='--')
# Vertical line from robot center in the Z direction
ax.plot([robot_center_coords[0], robot_center_coords[0]], [robot_center_coords[1], robot_center_coords[1]], [0, z_offset_robot], 'gray', linestyle='--')

# Annotate the distances
ax.text(x_offset_camera/2, y_offset_camera/2, 0, f"X offset = {x_offset_camera}mm", color='blue')
ax.text(x_offset_camera, y_offset_camera/2, z_offset_robot/2, f"Y offset = {abs(y_offset_camera)}mm", color='blue')
ax.text(0, 0, z_offset_robot/2, f"Z offset = {z_offset_robot}mm", color='blue')

# Set plot labels and legend
ax.set_xlabel('X axis (mm)')
ax.set_ylabel('Y axis (mm)')
ax.set_zlabel('Z axis (mm)')
ax.legend()

# Set the ticks for better visualization
ax.set_xticks(range(-500, 501, 100))
ax.set_yticks(range(-500, 501, 100))
ax.set_zticks(range(0, 201, 50))

# Show the plot
plt.show()
