import matplotlib.pyplot as plt
import numpy as np

# Example data
num_points = 50
angles = np.random.uniform(0, 2 * np.pi, num_points)
radii = np.random.uniform(0, 10, num_points)
x = radii * np.cos(angles)
y = radii * np.sin(angles)

# Desired radius in points
r = 20  # example radius, try adjusting this value

# Create the scatter plot with the specified dot size
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Convert cartesian coordinates to polar
theta = np.arctan2(y, x)
radii = np.sqrt(x**2 + y**2)

# Create the scatter plot
ax.scatter(theta, radii, s=r**2)

# Set the radius limits to center the plot around (0,0)
#ax.set_ylim(0, 1)  # Adjust the limit as necessary
regular_radii_lines = np.arange(0, 0.1544/2, 0.01/2)
irregular_line = [0.005/2]  # Example irregular radius
all_radii_lines = np.concatenate((regular_radii_lines, irregular_line))
all_radii_lines = np.sort(all_radii_lines)  # Sort to ensure correct order
ax.set_yticks(all_radii_lines)

# Customize angular ticks to show only at 0, 90, 180, and 270 degrees
ax.set_xticks([])
ax.set_xticklabels([])  # Optionally, you can set custom labels
ax.set_yticklabels([]) # Optionally, you can set custom

# Add circular grid lines
ax.grid(True)

#plt.title('Scatter plot with circular grid lines and selected angle labels')
plt.show()


