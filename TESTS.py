from image_processors import separate_colors_splitter
from image_readers import reader
import cv2
import numpy as np

image = "test_image40.jpg"
base_color = [255, 255, 255]

image = reader(image, "A2")
cv2.imshow("TEST", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
shape = image.shape
image = separate_colors_splitter(image, "NA")
print(image)
cv2.imshow("TEST", image)
cv2.waitKey(0)
cv2.destroyAllWindows()