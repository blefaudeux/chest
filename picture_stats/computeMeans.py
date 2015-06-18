#!/bin/python   

from PIL import Image

import glob, os
import numpy as np

report = []

# Compute stats on all the pictures
for infile in glob.glob("*.bmp"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    median = int(np.median(im))
    mean = np.round(np.mean(im), 1)

    print("Picture " + infile + " processed :\n mean " + str(mean) + " | median " + str(median) + "\n")

    report.append((infile, mean, median))
    im.close()

# Write a text file, just in case
file = open("report.txt", "w")
for item in report:
    file.write("Picture " + item[0] + " : mean " + str(item[1]) + ", median " + str(item[2]) + "\n")
file.close()


