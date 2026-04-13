def get_sheet_dimensions(sheet_size):
    if sheet_size == "A0":
        x = 841 #mm
        y = 1190 #mm
    if sheet_size == "A1":
        x = 841 #mm
        y = 594 #mm
    if sheet_size == "A2":
        x = 420 #mm
        y = 594 #mm
    if sheet_size == "A3":
        x = 420 #mm
        y = 297 #mm
    if sheet_size == "A4":
        x = 210 #mm
        y = 297 #mm
    if sheet_size == "A5":
        x = 210 #mm
        y = 148 #mm
    if sheet_size == "A6":
        x = 105 #mm
        y = 148 #mm
    if sheet_size == "A7":
        x = 105 #mm
        y = 74 #mm
    
    return x, y

def color_search(image, num_colors):
    found_colors = []
    for y in range(len(image)):
        for x in range(len(image[y])):
            if num_colors == len(found_colors):
                return sorted(found_colors)
            if image[y][x] not in found_colors:
                found_colors.append(int(image[y][x]))
    i = 0
    while len(found_colors) < num_colors:
        found_colors.append(found_colors[i])
        i += 1

    return sorted(found_colors)

def color_reformatter(color1: list, color2: list, color3: list):
    # colors are reversed for consistency between the viewer and visualizer
    color1.reverse()
    color2.reverse()
    color3.reverse()
    colors = [color1, color2, color3]

    resultant_colors = []
    for color in colors:
        r = color[0]/255
        g = color[1]/255
        b = color[2]/255
        reduced_color = [r, g, b]
        resultant_colors.append(reduced_color)

    return resultant_colors


def KNN_order_optimization(data):

    for y in range(len(data)-1):
        for x in range(1, len(data[y])-1):
            # define all next points
            xp1_y = data[y][x+1]
            xp1_yp1 = data[y+1][x+1]
            x_yp1 = data[y+1][x]
            xm1_yp1 = data[y+1][x-1]

            # compute distances
            distance_xp1_y = (((xp1_y[0]-data[y][x][0])**2)+((xp1_y[1]-data[y][x][1])**2))**0.5
            distance_xp1_yp1 = (((xp1_yp1[0]-data[y][x][0])**2)+((xp1_yp1[1]-data[y][x][1])**2))**0.5
            distance_x_yp1 = (((x_yp1[0]-data[y][x][0])**2)+((x_yp1[1]-data[y][x][1])**2))**0.5
            distance_xm1_yp1 = (((xm1_yp1[0]-data[y][x][0])**2)+((xm1_yp1[1]-data[y][x][1])**2))**0.5

            distances = [distance_xp1_y, distance_xp1_yp1, distance_x_yp1, distance_xm1_yp1]

            # swap points
            if (distance_x_yp1 == min(distances)) and (x_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = x_yp1
                data[y+1][x] = temp

            elif (distance_xp1_yp1 == min(distances)) and (xp1_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xp1_yp1
                data[y+1][x+1] = temp

            elif (distance_xm1_yp1 == min(distances)) and (xm1_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xm1_yp1
                data[y+1][x-1] = temp
            
    return data

def KNN_order_optimization_2nd_order(data):

    for y in range(len(data)-2):
        for x in range(2, len(data[y])-2):
            # define all next points
            xp1_y = data[y][x+1]
            xp1_yp1 = data[y+1][x+1]
            x_yp1 = data[y+1][x]
            xm1_yp1 = data[y+1][x-1]

            xp2_y = data[y][x+2]
            xp2_yp2 = data[y+2][x+2]
            x_yp2 = data[y+2][x]
            xm2_yp2 = data[y+2][x-2]

            # compute distances
            distance_xp1_y = (((xp1_y[0]-data[y][x][0])**2)+((xp1_y[1]-data[y][x][1])**2))**0.5
            distance_xp1_yp1 = (((xp1_yp1[0]-data[y][x][0])**2)+((xp1_yp1[1]-data[y][x][1])**2))**0.5
            distance_x_yp1 = (((x_yp1[0]-data[y][x][0])**2)+((x_yp1[1]-data[y][x][1])**2))**0.5
            distance_xm1_yp1 = (((xm1_yp1[0]-data[y][x][0])**2)+((xm1_yp1[1]-data[y][x][1])**2))**0.5

            distance_xp2_y = (((xp2_y[0]-data[y][x][0])**2)+((xp2_y[1]-data[y][x][1])**2))**0.5
            distance_xp2_yp2 = (((xp2_yp2[0]-data[y][x][0])**2)+((xp2_yp2[1]-data[y][x][1])**2))**0.5
            distance_x_yp2 = (((x_yp2[0]-data[y][x][0])**2)+((x_yp2[1]-data[y][x][1])**2))**0.5
            distance_xm2_yp2 = (((xm2_yp2[0]-data[y][x][0])**2)+((xm2_yp2[1]-data[y][x][1])**2))**0.5

            distances = [distance_xp1_y, distance_xp1_yp1, distance_x_yp1, distance_xm1_yp1, distance_xp2_y, distance_xp2_yp2, distance_x_yp2, distance_xm2_yp2]

            # swap points
            if (distance_x_yp1 == min(distances)) and (x_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = x_yp1
                data[y+1][x] = temp

            elif (distance_xp1_yp1 == min(distances)) and (xp1_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xp1_yp1
                data[y+1][x+1] = temp

            elif (distance_xm1_yp1 == min(distances)) and (xm1_yp1[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xm1_yp1
                data[y+1][x-1] = temp

            elif (distance_xp2_y == min(distances)) and (xp2_y[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xp2_y
                data[y][x+2] = temp

            elif (distance_xp2_yp2 == min(distances)) and (xp2_yp2[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xp2_yp2
                data[y+2][x+2] = temp
            
            elif (distance_x_yp2 == min(distances)) and (x_yp2[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = x_yp2
                data[y+2][x] = temp
            
            elif (distance_xm2_yp2 == min(distances)) and (xm2_yp2[2] == data[y][x][2]):
                temp = data[y][x+1]
                data[y][x+1] = xm2_yp2
                data[y+2][x-2] = temp
            
    return data


def KNN_order_optimization_multi_order(data, order):
    
    for y in range(len(data)-order):
        for x in range(order, len(data[y])-order):
            distances = []
            # define all next points
            next_points = []
            indices = []
            for j in range(len(data[y:y+order])):
                for i in range(len(data[j])):
                    next_points.append(data[j][i])
                    indices.append([j, i])

            # compute distances
            for i in range(len(next_points)):
                distances.append((((next_points[i][0]-data[y][x][0])**2)+((next_points[i][1]-data[y][x][1])**2))**0.5)

            # swap points
            for i in range(len(distances)):
                if (distances[i] == min(distances)) and (next_points[i][2] == data[y][x][2]):
                    temp = data[y][x+1]
                    data[y][x+1] = next_points[i]
                    data[indices[i][0]][indices[i][1]] = temp

            
    return data

def KNN_optimization_new(data, order):
    output = []
    for y in range(len(data)-order):
        output_row = []
        for x in range(order, len(data[y])-order):
            distances = []
            # define all next points
            next_points = []
            indices = []
            for j in range(len(data[y:y+order])):
                for i in range(len(data[j])):
                    next_points.append(data[j][i])
                    indices.append([j, i])

            # compute distances
            for i in range(len(next_points)):
                distances.append((((next_points[i][0]-data[y][x][0])**2)+((next_points[i][1]-data[y][x][1])**2))**0.5)

            # swap points
            for i in range(len(distances)):
                if (distances[i] == min(distances)) and (next_points[i][2] == data[y][x][2]):
                    temp = data[y][x+1]
                    data[y][x+1] = next_points[i]
                    data[indices[i][0]][indices[i][1]] = temp

            
    return output