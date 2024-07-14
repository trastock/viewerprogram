from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import numpy as np

def plot(data):
    
    x_points = []
    y_points = []
    nr = []
    
    #r = 20
    #area = np.pi * r**2
    
    for shot in data:
        #print("Skott:", type(data[shot]))
        if type(data[shot]) == list:
            if len(data[shot]) == 5:
                x_points.append(data[shot][2])
                y_points.append(data[shot][3])
                nr.append(int(''.join(i for i in shot if i.isdigit())))
    x = sort_list(x_points, nr)
    y = sort_list(y_points, nr)
    nr.sort()
    
    
    x = np.array(x_points)
    y = np.array(y_points)
    
    radii = np.ones(x.shape)*0.0056/2
    
    # Calculate radius and theta for polar coordinates
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # Desired radius in points for the scatter plot
    dot_radius = 20  # example radius in points

    # Create the polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6,6))

    
    # Set the radius limits to center the plot around (0,0)
    try:
        ax.set_ylim(0, np.max(r) + 0.0056)  # Adjust the limit as necessary
    except:
        pass
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
        else:
            return len(lines)
        
    if len(r) == 0:
        N = 2
    else:    
        N = get_most_outer_line(np.max(r), lines)

    all_radii_lines = np.array(lines[:N])
    all_radii_lines = np.sort(all_radii_lines)  # Sort to ensure correct order
    ax.set_yticks(all_radii_lines)

    # Optionally, set custom labels
    labels = []
    ax.set_yticklabels(labels)

    # Add circles with fixed size
    n = len(x)
    i = 0
    for x, y, r in zip(x, y, radii):
        if i + 1 == n:
            color = "red"
        else:
            color = "blue"
        circle = Circle((x, y), radius=r, transform=ax.transData._b, edgecolor='black', facecolor=color)
        ax.add_patch(circle)
        ax.text(x, y, nr[i], color="black", ha='center', va='center', fontsize=10, transform=ax.transData._b)
        i += 1

    # Add circular grid lines
    ax.grid(True)
    

    return fig, ax

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
 
    return z