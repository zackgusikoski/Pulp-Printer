import math
import cv2
import numpy as np
from PIL import Image

PAINT_DROP_SIZE = 30 #mm^2
FEED_RATE = 400
FLOW_RATE = 200
FLOW_STEP = 2 #mm
DROPLETS = 3 #number of droplets deposited per dot
DELAY = 0.01 #delay between droplet deposition (seconds)
SHEET_SIZE = "A0"
IMAGE = "test_image15.jpg"
BASE_COLOR = True
BASE_COLOR_VALUES = [255, 255, 255]
WRITE = True

# TODO Make program pull colors from image and present them as suggestions
# NOTE posters, comics and playing cards work really well

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

def rotate(input_image):
    # if width is greater than length, rotate 90 degrees, otherwise, return input image as is
    if (input_image.shape[1] > input_image.shape[0]) and (int(SHEET_SIZE[-1])%2) == 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    elif (input_image.shape[0] > input_image.shape[1]) and (int(SHEET_SIZE[-1])%2) != 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    else:
        return input_image


def compress_image(image):
    # get sheet dimensions
    x, y = get_sheet_dimensions(SHEET_SIZE)

    # get number of pixels in x and y
    x_pixels = int(x/math.sqrt(PAINT_DROP_SIZE))
    y_pixels = int(y/math.sqrt(PAINT_DROP_SIZE))
    # calculate compression ratio (number of pixels in image per one pixel on sheet)
    compression_ratio_y = int(image.shape[0]/y_pixels)
    compression_ratio_x = int(image.shape[1]/x_pixels)

    # remove y pixels
    y_list = []
    for y in range(0, image.shape[0], compression_ratio_y):
        y_list.append(image[y])

    # remove x pixels
    compressed_image_list = []
    for row in y_list:
        x_list = []
        for x in range(0, image.shape[1], compression_ratio_x):
            x_list.append(row[x])
        compressed_image_list.append(x_list)
    
    compressed_image = np.asarray(compressed_image_list, np.uint16)

    return compressed_image

def crop_image(image):
    # get sheet dimensions
    x, y = get_sheet_dimensions(SHEET_SIZE)

    # get number of pixels in x and y
    x_pixels = int(x/math.sqrt(PAINT_DROP_SIZE))
    y_pixels = int(y/math.sqrt(PAINT_DROP_SIZE))

    # clip edges
    y_cropped = image[:y_pixels]
    cropped_list = []
    for i in y_cropped:
        cropped_list.append(i[:x_pixels])
    
    cropped_image = np.asarray(cropped_list, np.uint16)

    return cropped_image

def separate_colors(image, num_colors):
    """Compare each pixel to all other pixels to find similarities"""
    # reshape image into single list containing lists of color values
    image_flat = np.reshape(image, (-1, 3))
    diff_results = []
    for i in image_flat[:4]:
        diff = 0
        diff_results_row = []
        for j in image_flat[:4]:
            for k in range(3):# 3 colors
                diff += image_flat[i][k] - image_flat[j][k]
            diff_results_row.append(diff)
        diff_results.append(diff_results_row)
    print(diff_results)
    return None


def separate_colors_grayscale(image, shape):
    #global BASE_COLOR
    # convert from array to PIL image
    gray_image = Image.fromarray(image)
    # convert to grayscale
    gray_image = gray_image.convert('L')
    # create array
    gray_image = np.array(gray_image)
    # reshape image to column vector
    gray_image = np.reshape(gray_image, -1)

    # round pixels to one of three colors
    processed_image_list = []
    average_color = 0
    length = len(gray_image)
    for i in gray_image:
        average_color += i/length
    
    if average_color < 128:
        color_val = 255 - average_color
    else:
        color_val = 255
    
    if BASE_COLOR == False:
        # split colors into 3
        for i in gray_image:
            if i >= int(color_val*2/3):
                processed_image_list.append(int(255))

            elif int(color_val/3) <= i < int(color_val*2/3):
                processed_image_list.append(int(color_val/2))

            else:
                processed_image_list.append(int(0))
    else:
        # split colors into 4
        for i in gray_image:
            if i >= int(color_val*3/4):
                processed_image_list.append(int(255))# maybe append "base" and then have gcode writer and color preview read it with special instructions
                
            elif int(color_val/2) <= i < int(color_val*3/4):
                processed_image_list.append(int(color_val*2/3))

            elif int(color_val/4) <= i < int(color_val/2):
                processed_image_list.append(int(color_val/3))

            else:
                processed_image_list.append(int(0))

    # convert to array
    output_image = np.array(processed_image_list).T
    # reshape image
    output_image = output_image.reshape(shape)

    return output_image

def preview_colors(image, color1, color2, color3, base_color):
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


def write_Gcode(image):
    # calculate scaling factor (converts pixel index to mm of machine movement)
    scaling_factor = math.sqrt(PAINT_DROP_SIZE)
    # create an array of pixel coordinates and pixel colors [x, y, color]
    pixels = []
    for y in range(len(image)):
        pixel_row = []
        for x in range(len(image[y])):
            # light colors are painted last
            if image[y][x] >= 250:
                color = 3
            # darker colors are painted first
            elif image[y][x] <= 5:
                color = 1
            else:
                color = 2
            pixel_row.append([(scaling_factor*x)+scaling_factor, (scaling_factor*y)+scaling_factor, color])
        pixels.append(pixel_row)

    # generate Gcode
    string1 = ''
    string2 = ''
    string3 = ''
    z_pseudo_location = 0
    for y in range(len(pixels)):
        gcode = "G90 ; absolute distance mode\nG21 ; set millimeters\nG17 ; XY Plane\nG94 ; Units per Minute Feed Rate Mode\nG1 X0 Y0\nG92 Z0 ; zero the z axis\n\n"

        for x in range(len(pixels[y])):
            z_pseudo_location += FLOW_STEP

            if (y%2) != 0:
                x = len(pixels[y])- 1 - x
            if pixels[y][x][2] == 1:
                string1 += "F%s\n" % (FEED_RATE)
                string1 += "G0 X%s Y%s\n" % (pixels[y][x][0], pixels[y][x][1])
                string1 += "F%s\n" % (FLOW_RATE)
                for i in range(DROPLETS-1):
                    string1 += "G0 Z%s\n" % (z_pseudo_location)
                    string1 += "G4 P%s\n" % (DELAY)
                    z_pseudo_location += FLOW_STEP
                string1 += "G0 Z%s\n" % (z_pseudo_location)

            elif pixels[y][x][2] == 2:
                string2 += "F%s\n" % (FEED_RATE)
                string2 += "G0 X%s Y%s\n" % (pixels[y][x][0], pixels[y][x][1])
                string2 += "F%s\n" % (FLOW_RATE)
                for i in range(DROPLETS-1):
                    string2 += "G0 Z%s\n" % (z_pseudo_location)
                    string2 += "G4 P%s\n" % (DELAY)
                    z_pseudo_location += FLOW_STEP
                string2 += "G0 Z%s\n" % (z_pseudo_location)
            elif pixels[y][x][2] == 3:
                string3 += "F%s\n" % (FEED_RATE)
                string3 += "G0 X%s Y%s\n" % (pixels[y][x][0], pixels[y][x][1])
                string3 += "F%s\n" % (FLOW_RATE)
                for i in range(DROPLETS-1):
                    string3 += "G0 Z%s\n" % (z_pseudo_location)
                    string3 += "G4 P%s\n" % (DELAY)
                    z_pseudo_location += FLOW_STEP
                string3 += "G0 Z%s\n" % (z_pseudo_location)
        
        gcode += string1
        #M8 is coolant flood on
        gcode += string2
        #M3 is spindle on clockwise
        gcode += string3
    
    gcode += "M5\n" # spindle off
    gcode += "M09\n" # coolant off
    gcode += "M2"

    return gcode


def main():
    # read image
    input_image = cv2.imread(IMAGE)
    input_image = rotate(input_image)
    # convert to grayscale
    image = separate_colors_grayscale(input_image, (input_image.shape[0], input_image.shape[1]))
    print(image.shape)
    # crompress image
    image = compress_image(image)
    # crop image
    image = crop_image(image)
    print(image.shape)
    if WRITE == True:
        gcode = write_Gcode(image)
        output_file = open("test_gcode.gcode", 'w')
        output_file.write(gcode)
        output_file.close()
    # display image
    image = preview_colors(image, [0, 0, 0], [255, 0, 0], [0, 0, 255], BASE_COLOR_VALUES)
    image = cv2.resize(image, (400, 600))
    cv2.imshow("Processed Image", cv2.convertScaleAbs(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()