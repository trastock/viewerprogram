from matplotlib import pyplot as plt
import numpy as np

def plot(data):
    
    x_points = []
    y_points = []
    
    
    #r = 20
    #area = np.pi * r**2
    
    for shot in data:
        if shot != "Inner tens" or shot != "Tot":
            x_points.append(data[shot][2])
            y_points.append(data[shot][3])
    x = np.array(x_points)
    y = np.array(y_points)
    
    """
    min_x = np.min(x_points)
    max_x = np.max(x_points)
    if abs(min_x) > max_x:
        max_x = abs(min_x)
    
    min_y = np.min(y_points)
    max_y = np.max(y_points)
    if abs(min_y) > max_y:
        max_y = abs(min_y)
    
    max_x += 0.0056
    max_y += 0.0056
    
    plt.xlim(-max_x, max_x)
    plt.ylim(-max_y, max_y)
    
    
    y_points = np.array(y_points)
    
    
    plt.scatter(x_points, y_points, s=area)
    plt.show()
    
    """
    # Convert Cartesian coordinates to polar coordinates
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    # Desired radius in points for the scatter plot
    dot_radius = 20  # example radius, try adjusting this value

    # Create the polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Create the scatter plot with the specified dot size
    ax.scatter(theta, r, s=dot_radius**2)

    # Set the radius limits to center the plot around (0,0)
    ax.set_ylim(0, np.max(r) * 1)  # Adjust the limit as necessary

    # Customize angular ticks to show only at 0, 90, 180, and 270 degrees
    ax.set_xticks([])
    ax.set_xticklabels([])  # Optionally, you can set custom labels

    # Set fixed distance between radii lines
    
    lines = [0.005/2, 0.0104/2, 0.0264/2, 0.0424/2, 
             0.0584/2, 0.0744/2, 0.0904/2, 0.1064/2,
             0.1224/2, 0.1384, 0.1544]
    
    N = get_most_outer_line(np.max(r), lines)
    
    
    #regular_radii_lines = np.arange(0, get_most_outer_line(np.max(r)), 0.01/2)
    #irregular_line = [0.005/2]  # Example irregular radius
    all_radii_lines = np.array(lines[:N])
    all_radii_lines = np.sort(all_radii_lines)  # Sort to ensure correct order
    ax.set_yticks(all_radii_lines)

    # Optionally, set custom labels
    labels = []
    ax.set_yticklabels(labels)

    # Add circular grid lines
    ax.grid(True)

    plt.title('Scatter plot with circular grid lines and additional irregular line')
    plt.show()

def get_most_outer_line(r, lines):
    for i, line in enumerate(lines):
        if line > (r + 0.0056):
            return i + 1