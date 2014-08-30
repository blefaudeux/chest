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


# Compute the distance in between two angular coordinates on a sphere
def distOnSphere(point1, point2, radius):
    angularDist = np.sqrt(np.power(point1[0] - point2[0], 2) + np.power(point1[1] - point2[1], 2))

    return angularDist * radius

def parse_kml(file):
    tree = ET.parse(file).getroot()

    nameRaw = tree.tag

    rootName = nameRaw[1:-4]  # "http://earth.google.com/kml/2.2"
    placemarkList = list(tree.findall(".//{"+rootName+"}Placemark"))

    # if len(placemarkList) == 0:  # Use a while loop here
    #     rootName = "http://www.opengis.net/kml/2.2"
    #     placemarkList = list(tree.findall(".//{"+rootName+"}Placemark"))

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


def prettyPlot(data, title):
    # Thanks Rutger Kassies for the nice drawing method !

    # Quick failsafe : remove null entries from the files
    alt = data[:, 2]
    lat = data[:, 0]
    lon = data[:, 1]

    alt = alt[alt.nonzero()]
    lat = lat[alt.nonzero()]
    lon = lon[alt.nonzero()]

    # Compute flat distance
    linearDist = np.zeros(np.size(alt))

    for i in range(np.size(alt)):
        if i == 0:
            linearDist[i] = 0

        else:
            linearDist[i] = distOnSphere((lat[i], lon[i]), (lat[i-1],lon[i-1]), 6.4*10e3)
            linearDist[i] += linearDist[i-1]

    # Actual drawings.. complicated by the blue shading
    fig, ax = pl.subplots()
    poly, = ax.fill(linearDist, alt, facecolor='none')
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # create a dummy image
    img_data = np.arange(ymin, ymax, (ymax-ymin)/100.)
    img_data = img_data.reshape(img_data.size, 1)

    # plot and clip the image
    im = ax.imshow(img_data, aspect='auto', origin='lower', cmap=pl.cm.Blues_r, extent=[xmin, xmax, ymin, ymax], vmin=alt.min(), vmax=alt.max())
    im.set_clip_path(poly)
    fig.suptitle(title)
    ax.set_xticks(np.arange(xmin, xmax, 200))
    ax.set_yticks(np.arange(ymin, ymax, 50))
    pl.grid()
    pl.show()

# Process one file
def Pipeline(filename):
    records = parse_kml(filename)

    if np.size(records) > 0:
        title = filename.split('/')
        prettyPlot(records, title[-1])

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

