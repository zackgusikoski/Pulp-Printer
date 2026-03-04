import matplotlib.pyplot as plt
from tools import color_reformatter


def visualize_dots(filename, color1, color2, color3):
    color_list = color_reformatter(color1, color2, color3)

    gcode = open(filename, 'r')
    lines = gcode.readlines()

    x = 0
    y = 0
    x_vals = []
    y_vals = []
    coordinates = []
    for line in lines:
        if line[:4] == 'G0 X':
            line = line[2:].replace('X', '').replace('Z', '').replace(' ', '').replace('\n', '')
            if 'Y' in line:
                [x, y] = line.split('Y')
            x_vals.append(float(x))
            y_vals.append(float(y))
        if (line[:2] == "M8") or (line[:2] == "M3"):
            coordinates.append([x_vals, y_vals])
            x_vals = []
            y_vals = []
    coordinates.append([x_vals, y_vals])
    gcode.close()

    for i in range(len(coordinates)):
        plt.scatter(coordinates[i][0], coordinates[i][1], color=color_list[i] , alpha=0.3)

    plt.show()

def visualize_path(filename, color1, color2, color3):
    color_list = color_reformatter(color1, color2, color3)

    gcode = open(filename, 'r')
    lines = gcode.readlines()

    x = 0
    y = 0
    x_vals = []
    y_vals = []
    coordinates = []
    for line in lines:
        if line[:4] == 'G0 X':
            line = line[2:].replace('X', '').replace('Z', '').replace(' ', '').replace('\n', '')
            if 'Y' in line:
                [x, y] = line.split('Y')
            x_vals.append(float(x))
            y_vals.append(float(y))
        if (line[:2] == "M8") or (line[:2] == "M3"):
            coordinates.append([x_vals, y_vals])
            x_vals = []
            y_vals = []
    coordinates.append([x_vals, y_vals])
    gcode.close()

    for i in range(len(coordinates)):
        plt.plot(coordinates[i][0], coordinates[i][1], color=color_list[i] , alpha=0.3)

    plt.show()

def visualizer(filename, visualizer_type, color1, color2, color3):

    if visualizer_type == "Path":
        visualize_path(filename, color1, color2, color3)

    else:
        visualize_dots(filename, color1, color2, color3)