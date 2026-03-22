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