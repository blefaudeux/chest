#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import numpy as np
import pylab as pl


#
# from fastkml import kml
#
# parser = kml.KML()
# file = open(filename)
# parser.fromstring(file.read())
#
# features = list(parser.features())
#
# data = list(features[0].features())
# placemark = data[1]

def parse_kml(file):
    tree = ET.parse(file).getroot()

    rootName = "http://earth.google.com/kml/2.2"
    placemarkList = list(tree.findall(".//{"+rootName+"}Placemark"))

    if len(placemarkList) == 0:  # Use a while loop here
        rootName = "http://www.opengis.net/kml/2.2"
        placemarkList = list(tree.findall(".//{"+rootName+"}Placemark"))

    coordlist = np.zeros((1, 3))

    for placemark in placemarkList:
        records = placemark.findall(".//{"+rootName+"}coordinates")

        for coord in records:
            coordline = (coord.text.replace(",", " ")).split(' ')

            n_coords = int(len(coordline) / 3)
            new_batch = np.zeros((n_coords, 3))

            # Save lat/long/alt triplets
            for i in range(n_coords):
                new_batch[i, 0] = float(coordline[3*i])      # Lat
                new_batch[i, 1] = float(coordline[3*i+1])    # Long
                new_batch[i, 2] = float(coordline[3*i+2])    # Altitude

            coordlist = np.vstack((coordlist, new_batch))

    return coordlist[1:, :]  # Skip the first line


def prettyPlot(data):
    # Thanks Rutger Kassies for the nice method..

    x = np.linspace(0, 1, len(data[:,1]))
    alt = data[:,2]

    fig, ax = pl.subplots()

    # plot only the outline of the polygon, and capture the result
    poly, = ax.fill(x, alt, facecolor='none')

    # get the extent of the axes
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # create a dummy image
    img_data = np.arange(ymin, ymax, (ymax-ymin)/100.)
    img_data = img_data.reshape(img_data.size, 1)

    # plot and clip the image
    im = ax.imshow(img_data, aspect='auto', origin='lower', cmap=pl.cm.Blues_r, extent=[xmin, xmax, ymin, ymax], vmin=alt.min(), vmax=alt.max())
    im.set_clip_path(poly)

    # display (and save eventually ?)
    pl.show()

# Get all the files in the given folder
# TODO: Ben

# Get the data from the file
filename = "/home/benjamin/Documents/Randos/Alpes/Grand Area.kml"
records = parse_kml(filename)

# Plot the altitude profile
prettyPlot(records)
