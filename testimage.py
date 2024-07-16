#!/usr/bin/python3

# Create test images with specific patterns to test leds

import numpy as np

from binimage import LedFanBinImage
from random import randint

T_MAX = 3072
R_MAX = 112

ARRAY = np.zeros((1, T_MAX, R_MAX, 3)) # movie of 1 frame, 3072x224 image size, 3 colors
binimage = LedFanBinImage('G224-42')

# Add some patterns to the array

#    color_r, color_g, color_b = (255,255,255) #( randint(0, 255), randint(0, 255), randint(0, 255) )
for j in range(0, R_MAX-3, 3):
    for i in range(0, T_MAX, 1):
        ARRAY[0, i, j+0, 0] = 255
        ARRAY[0, i, j+0, 1] = 0
        ARRAY[0, i, j+0, 2] = 0
        ARRAY[0, i, j+1, 0] = 0
        ARRAY[0, i, j+1, 1] = 255
        ARRAY[0, i, j+1, 2] = 0
        ARRAY[0, i, j+2, 0] = 0
        ARRAY[0, i, j+2, 1] = 0
        ARRAY[0, i, j+2, 2] = 255

binimage.import_numpy_movie(ARRAY)
binimage.encode_movie()
binimage.export_bin_movie("test3.BIN")

