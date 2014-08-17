#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import numpy as np

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

    placemarkList = list(tree.findall(".//{http://earth.google.com/kml/2.2}Placemark"))

    coordlist = []

    for placemark in placemarkList:
        records = placemark.findall(".//{http://earth.google.com/kml/2.2}coordinates")

        for coord in records:
            #coordline = coord.text.split(' ').split(',') re.findall(r"[\w']+", DATA)

            n_coords = int(len(coordline) / 3)
            new_batch = np.zeros((n_coords, 3))

            for i in range(n_coords):
                new_batch[3*i  ,0] = float(coordline[3*i])
                new_batch[3*i+1,1] = float(coordline[3*i+1])
                new_batch[3*i+2,2] = float(coordline[3*i+2])

            coordlist.append(new_batch)

        print("Placemark found")

    return coordlist

filename = "/home/benjamin/Documents/Randos/Alpes/2014-07-31_10-04-11.kml"
records = parse_kml(filename)
