'''
Author: Monirul Hasan
Date: November 8, 2016

Dependencies
Install miniconda with Python 3+
To install OpenCV3 run:
$conda install -c menpo opencv3=3.1.0
'''

from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np


def open_file():
    # change the initial directory to whatever is needed
    name = askopenfilename(initialdir="~/PyCharmProjects/bangla-ocr",
                           filetypes=(("Image files", "*.jpg"), ("All Files", "*.*")),
                           title="Choose a file."
                           )
    return name


def scan_line(image, image_to_change):
    rows = []
    height, width = image.shape
    for row in range(1, height):
        sum_pixels = 0
        for col in range(1, width):
            if image.item(row, col) > 0:
                sum_pixels += 1
        if sum_pixels < width * .05:
            rows.append(row)

    for row in rows:
        cv2.line(image_to_change, (0, row), (width, row), (0, 0, 0), 1)


# file_name = open_file()
# print(file_name)

file_name = 'test_images/bangla_gan_rotated.png'

original_image = cv2.imread(file_name)
height, width, channel = original_image.shape
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
blur_image = cv2.blur(gray_image, (3, 3))
#edges = cv2.Canny(blur_image, 50, 150, apertureSize=3)

th1 = cv2.adaptiveThreshold(blur_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# return value: a set of rho, theta values
# parameter 1: input image -- the thresholded one
# parameter 2: value for rho in pixels
# parameter 3: value for theta
# parameters 2 and 3 are used to get the votes in discrete intervals
# parameter 4: the minimum number of pixels you need on a line to consider it a line
# -- here I'm saying we need at least 0.5 (or 50%) pixels to be on the line
hough_lines = cv2.HoughLines(th1, 1, np.pi / 180.0, int(width * 0.5))

cv2.imshow('Original Image', original_image)
cv2.imshow('Thresholded Image', th1)

# we run through each lines and plot them on the original image
for i in range(len(hough_lines)):
    for rho, theta in hough_lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        print(rho, theta, x1, y1, x2, y2)
        cv2.line(original_image, (x1, y1), (x2, y2), (0, 0, 255), 1)

cv2.imshow('Hough Transform Lines', original_image)

while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        sys.exit(0)
