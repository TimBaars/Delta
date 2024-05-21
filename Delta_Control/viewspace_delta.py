""" 2D Plotting of the Delta Robot Working Envelope
import matplotlib.pyplot as plt
import numpy as np

# Original data
x = [0, 50, 75, 80, 90, 160, 210,270, 210, 160, 90, 80, 75, 50, 0]
y = [0,100,150,220,320, 250,190,0, -190,-250,-320,-220,-150,-100,0]

# Plotting the rotated and mirrored graph
plt.plot(y, x)

# Setting the labels and title with updated orientation
plt.xlabel('Height (mm)')
plt.ylabel('Radius (mm)')
plt.title('Rotated and Mirrored View of Delta Robot Working Envelope')

# Set the aspect of the plot to be equal, so the circle isn't skewed
plt.axis('equal')
# Show grid
plt.grid(True)
plt.gca().invert_yaxis()
# Show the plot
plt.show()
"""
"""3D Plotting of the Delta Robot Working Envelope"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Original 2D data
x = np.array([0, 50, 75, 80, 90, 160, 210, 270, 210, 160, 90, 80, 75, 50, 0])
y = np.array([0, 100, 150, 220, 320, 250, 190, 0, -190, -250, -320, -220, -150, -100, 0])
z = np.array([0])

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create grid values for theta (angle for revolution)
theta = np.linspace(-np.pi, np.pi, 100)
# Convert polar coordinates to Cartesian for X and Y using meshgrid, Z remains the same
X, T = np.meshgrid(x, theta)
Y, Z = np.meshgrid(y, z)

# Use the meshgrid outputs for transformation
# X remains the same, Y and Z are transformed based on the angle theta
X3 = X
Y3 = Y * np.cos(T)
Z3 = Y * np.sin(T)

# Plotting the surface
ax.plot_surface(X3, Y3, Z3, rstride=1, cstride=1, color='b', alpha=0.5, edgecolor='none')

# Labeling axes
ax.set_xlabel('Radius (mm)')
ax.set_ylabel('X (mm)')
ax.set_zlabel('Y (mm)')
ax.set_title('3D Representation of the Delta Robot Working Envelope')

# Show plot
plt.show()