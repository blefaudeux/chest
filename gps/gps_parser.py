#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import numpy as np
import pylab as pl

import glob
import os

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
        # Only use the records if the attribut contain 'GPS'
        attrib = placemark.attrib
        id = attrib.get('id')

        if id and id.find('GPS') >= 0:
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
    # Thanks Rutger Kassies for the nice drawing method !

    alt = data[:, 2]
    alt = alt[alt.nonzero()]
    alt = np.append(alt.min(), alt)
    x = np.linspace(0, 1, len(alt))
    alt_bottom = np.ones((len(alt)))
    alt_bottom *= alt.min()

    fig, ax = pl.subplots()

    # plot only the outline of the polygon, and capture the result
    poly, = ax.fill(x, alt, facecolor='none')
    #poly = ax.fill_between(x, alt, alt.min(), facecolor='none')

    # get the extent of the axes
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # create a dummy image
    img_data = np.arange(ymin, ymax, (ymax-ymin)/100.)
    img_data = img_data.reshape(img_data.size, 1)

    # plot and clip the image
    im = ax.imshow(img_data, aspect='auto', origin='lower', cmap=pl.cm.Blues_r, extent=[xmin, xmax, ymin, ymax], vmin=alt.min(), vmax=alt.max())
    im.set_clip_path(poly)
    #im.set_clip_path(poly.get_clip_path())

    # display (and save eventually ?)
    pl.show()

# Process one file
def Pipeline(filename):
    records = parse_kml(filename)
    prettyPlot(records)
    # Save the file ?

# Get all the KML files in this folder and plot
def FolderPipeline(folder):
    coord_ovrl = np.array([])

    files = glob.glob(folder + "/*.kml")
    file_exist = False

    for file in files:
        print("Reading {}".format(file))
        Pipeline(file)

# Run for all files in folder :)
folder = "/home/benjamin/Documents/Randos/Alpes"
FolderPipeline(folder)

