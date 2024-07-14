import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Example data
#x = np.random.uniform(-1, 1, 100)
#y = np.random.uniform(-1, 1, 100)

x = [-0.01223708, -0.00290666, -0.00709459, -0.00206037, -0.0032147,   0.00382276, 0.00252428, -0.0145177,  -0.00135969,  0.00666336]
y = [-0.01822811,  0.0016458,   0.00084074, -0.00392927,  0.00082587, -0.01064382, 0.0088492,   0.00038413, -0.00394837, -0.01607028]
x = np.array(x)
y = np.array(y)


radii = np.ones(x.shape)*0.0056/2
#radii = np.random.uniform(0.01, 0.1, 100)  # Example radii for circles

# Calculate radius and theta for polar coordinates
r = np.sqrt(x**2 + y**2)
theta = np.arctan2(y, x)

# Desired radius in points for the scatter plot
dot_radius = 20  # example radius in points

# Create the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Set the radius limits to center the plot around (0,0)
ax.set_ylim(0, np.max(r) + 0.0056)  # Adjust the limit as necessary

# Customize angular ticks to show only at 0, 90, 180, and 270 degrees
ax.set_xticks([])
ax.set_xticklabels([])  # Optionally, you can set custom labels

# Set fixed distance between radii lines
lines = [0.005/2, 0.0104/2, 0.0264/2, 0.0424/2, 
         0.0584/2, 0.0744/2, 0.0904/2, 0.1064/2,
         0.1224/2, 0.1384/2, 0.1544/2]

# Function to get the most outer line (assuming it's defined elsewhere)
def get_most_outer_line(r, lines):
    for i, line in enumerate(lines):
        if line > (r + 0.0056):
            return i 
N = get_most_outer_line(np.max(r), lines)

all_radii_lines = np.array(lines[:N])
all_radii_lines = np.sort(all_radii_lines)  # Sort to ensure correct order
ax.set_yticks(all_radii_lines)

# Optionally, set custom labels
labels = []
ax.set_yticklabels(labels)

# Add circles with fixed size
n = len(x)
i = 1
for x, y, r in zip(x, y, radii):
    if i == n:
        color = "red"
    else:
        color = "blue"
    circle = Circle((x, y), radius=r, transform=ax.transData._b, edgecolor='black', facecolor=color)
    ax.add_patch(circle)
    ax.text(x, y, str(i), color="black", ha='center', va='center', fontsize=10, transform=ax.transData._b)
    i += 1

# Add circular grid lines
ax.grid(True)

plt.show()


