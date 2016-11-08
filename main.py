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


file_name = open_file()
print(file_name)

original_image = cv2.imread(file_name)
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
blur_image = cv2.blur(gray_image, (3, 3))
edges = cv2.Canny(blur_image, 50, 150, apertureSize=3)
th1 = cv2.adaptiveThreshold(blur_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

scan_line(edges, blur_image)
# cv2.imshow('Original Image', original_image)
# cv2.imshow('Grayscale Image', gray_image)
cv2.imshow('Scan line', blur_image)
# cv2.imshow('Threshold', th1)

while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        sys.exit(0)
