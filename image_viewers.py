import cv2
from tools import get_sheet_dimensions, color_search
import numpy as np

def preview_colors(image, color1, color2, color3, base_color):
    
    # colors are reversed for consistency between the viewer and visualizer
    color1.reverse()
    color2.reverse()
    color3.reverse()

    if base_color == "NA":
        # create an array of pixel colors [color, color, color]
        pixels = []
        # retireve colors found in image
        image_colors = color_search(image, 3)
        for y in range(len(image)):
            pixel_row = []
            for x in range(len(image[y])):
                # light colors are painted last
                if image[y][x] == image_colors[2]:
                    color = color3
                # darker colors are painted first
                elif image[y][x] == image_colors[0]:
                    color = color1
                else:
                    color = color2
                pixel_row.append(color)
            pixels.append(pixel_row)
        numpy_array = np.array(pixels, dtype=np.uint8)
    else:
        # create an array of pixel colors [color, color, color]
        pixels = []
        # retireve colors found in image
        image_colors = color_search(image, 4)
        for y in range(len(image)):
            pixel_row = []
            for x in range(len(image[y])):
                # light colors are painted last
                if image[y][x] == image_colors[3]:
                    color = base_color
                elif image[y][x] == image_colors[2]:
                    color = color3
                # darker colors are painted first
                elif image[y][x] == image_colors[0]:
                    color = color1
                else:
                    color = color2
                pixel_row.append(color)
            pixels.append(pixel_row)
        numpy_array = np.array(pixels, dtype=np.uint8)
    return numpy_array

def viewer(image, color1, color2, color3, base_color, sheet_size):
    size = 250
    if (int(sheet_size[-1]) % 2) == 0:
        x = size
        y = int(x*(2**0.5))
    else:
        x = int(size*(2**0.5))
        y = size

    # display image
    image = preview_colors(image, color1, color2, color3, base_color)
    image = cv2.resize(image, (x, y))
    cv2.imshow("Processed Image", cv2.convertScaleAbs(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()