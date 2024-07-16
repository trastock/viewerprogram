from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec

import numpy as np

def plot(data, score_dict):
    
    x_points = []
    y_points = []
    nr = []
    
    #r = 20
    #area = np.pi * r**2
    shot_scores = []
    
    score_text = ""
    for shot in data:
        #print("Skott:", type(data[shot]))
        if type(data[shot]) == list:
            if len(data[shot]) == 5:
                x_points.append(data[shot][2])
                y_points.append(data[shot][3])
                shot_scores.append([data[shot][0], data[shot][1]])
                nr.append(int(''.join(i for i in shot if i.isdigit())))
    x = sort_list(x_points, nr)
    y = sort_list(y_points, nr)
    shot_scores = sort_list(shot_scores, nr)
    nr.sort()
    """
    for i, shot in enumerate(shot_scores):
        score_text += str(nr[i]) + ": " + str(shot[0]) + "\n"
    """
    x = np.array(x_points)
    y = np.array(y_points)
    
    radii = np.ones(x.shape)*0.0056/2
    
    # Calculate radius and theta for polar coordinates
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # Desired radius in points for the scatter plot
    dot_radius = 20  # example radius in points

    # Create the polar plot
    fig = Figure()
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])  # Create a grid with 2 columns

    ax = fig.add_subplot(gs[0], polar = True)

    #fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6,6))

    
    # Set the radius limits to center the plot around (0,0)

    try:
        ax.set_ylim(0, np.max(r) + 0.0056)  # Adjust the limit as necessary
    except:
        ax.set_ylim(0, 0.1544/2 + 0.0056)  # Adjust the limit as necessary
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
        N = 10
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
    
    # Scoreboard
    ax_score = fig.add_subplot(gs[1])
    ax_score.axis('off')  # Turn off the axis
    scoreboard_title_obj = ax_score.set_title("", fontsize=8, y=0.8)
    
    #ax_score.set_title(list(score_dict.keys())[0])
    # Display the scores
    for item in score_dict["Score"]:
        if item:
            if score_text:
                score_text += ", "
            score_text += str(item)
    score_text += "\n" + str(score_dict["Tot"])
    text_obj = ax_score.text(0.5, 0.1, score_text, ha='center', va='center', transform=ax_score.transAxes)
    
    #shot_obj = ax_score.text(0.1, 0.1, shot_text, ha='center', va='center', transform=ax_score.transAxes)
    def on_resize(event):
        fig_width, fig_height = fig.get_size_inches()
        new_fontsize = fig_width * 2  # Adjust this multiplier as needed
        text_obj.set_fontsize(new_fontsize)
        #shot_obj.set_fontsize(new_fontsize)
        scoreboard_title_obj.set_fontsize(new_fontsize)
        scoreboard_title_obj.set_text(score_dict["Name"])  # Set the updated scoreboard title text
        fig.canvas.draw()

    fig.canvas.mpl_connect('resize_event', on_resize)
    
    
    fig.tight_layout()

    
    return fig, (ax, ax_score)

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
 
    return z