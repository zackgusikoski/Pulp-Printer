import cv2

def rotate(input_image, sheet_size):
    # if width is greater than length, rotate 90 degrees, otherwise, return input image as is
    if (input_image.shape[1] > input_image.shape[0]) and (int(sheet_size[-1])%2) == 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    elif (input_image.shape[0] > input_image.shape[1]) and (int(sheet_size[-1])%2) != 0:
        return cv2.rotate(input_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    else:
        return input_image

def reader(image, sheet_size):
    # read image
    input_image = cv2.imread(image)
    input_image = rotate(input_image, sheet_size)
    return input_image