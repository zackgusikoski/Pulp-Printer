import cv2
import numpy as np
from tools import get_sheet_dimensions
from PIL import Image

def rotate(input_image, sheet_size):
    # if width is greater than length, rotate 90 degrees, otherwise, return input image as is
    if (input_image.shape[1] > input_image.shape[0]) and (int(sheet_size[-1])%2) == 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    elif (input_image.shape[0] > input_image.shape[1]) and (int(sheet_size[-1])%2) != 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    else:
        return input_image


def compress_image_standard(image, sheet_size, paint_drop_size):
    # get sheet dimensions
    x, y = get_sheet_dimensions(sheet_size)

    # get number of pixels in x and y
    #x_pixels = int(x/math.sqrt(paint_drop_size))
    #y_pixels = int(y/math.sqrt(paint_drop_size))
    x_pixels = int(x/paint_drop_size)
    y_pixels = int(y/paint_drop_size)
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

def compress_image_cv2(image, sheet_size, paint_drop_size, interpolation):

    x, y = get_sheet_dimensions(sheet_size)
    print(image.shape, y/paint_drop_size, x/paint_drop_size)

    image = cv2.resize(image, (int(x/paint_drop_size), int(y/paint_drop_size)), interpolation=interpolation)
    print(len(image), len(image[0]))

    return image

def crop_image(image, sheet_size, paint_drop_size):
    # get sheet dimensions
    x, y = get_sheet_dimensions(sheet_size)

    # get number of pixels in x and y
    #x_pixels = int(x/math.sqrt(paint_drop_size))
    #y_pixels = int(y/math.sqrt(paint_drop_size))
    x_pixels = int(x/paint_drop_size)
    y_pixels = int(y/paint_drop_size)

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

def separate_colors_grayscale(image, shape, base_color):
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
    
    if base_color == "NA":
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
                processed_image_list.append(int(255))
                
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

def processor(input_image, base_color, sheet_size: str, paint_drop_size: int, compression_type: str):
    #NOTE Standard will not be in the dropdown
    if compression_type == "Standard":
        image = separate_colors_grayscale(input_image, (input_image.shape[0], input_image.shape[1]), base_color)
        # crompress image
        image = compress_image_standard(image, sheet_size, paint_drop_size)
        # crop image
        image = crop_image(image, sheet_size, paint_drop_size)

    elif compression_type == "Linear":
        image = compress_image_cv2(input_image, sheet_size, paint_drop_size, cv2.INTER_LINEAR)
        # convert to grayscale
        image = separate_colors_grayscale(image, (image.shape[0], image.shape[1]), base_color)
    
    elif compression_type == "Cubic":
        image = compress_image_cv2(input_image, sheet_size, paint_drop_size, cv2.INTER_CUBIC)
        # convert to grayscale
        image = separate_colors_grayscale(image, (image.shape[0], image.shape[1]), base_color)
    
    elif compression_type == "Nearest":
        image = compress_image_cv2(input_image, sheet_size, paint_drop_size, cv2.INTER_NEAREST)
        # convert to grayscale
        image = separate_colors_grayscale(image, (image.shape[0], image.shape[1]), base_color)
    
    elif compression_type == "Area":
        image = compress_image_cv2(input_image, sheet_size, paint_drop_size, cv2.INTER_AREA)
        # convert to grayscale
        image = separate_colors_grayscale(image, (image.shape[0], image.shape[1]), base_color)
    
    elif compression_type == "Lanczos":
        image = compress_image_cv2(input_image, sheet_size, paint_drop_size, cv2.INTER_LANCZOS4)
        # convert to grayscale
        image = separate_colors_grayscale(image, (image.shape[0], image.shape[1]), base_color)
    
    return image