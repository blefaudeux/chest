#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
#import pylab as mp
import matplotlib.pyplot as mp
import glob
from scipy.stats import gaussian_kde
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Settings:
    xStart = 0
    xStop = 1.0
    nBins = 30
    bandwidth = 0.05

    def __init__(self):
        pass

# Parse the XML file
def ParseCellXML(file):
    tree = ET.parse(file).getroot()

    records = []

    for type in tree.findall('Marker_Data/Marker_Type'):
        mark = []

        for marker in type.findall('Marker'):
            x = int(marker.find('MarkerX').text)
            y = int(marker.find('MarkerY').text)
            z = int(marker.find('MarkerZ').text)
            mark.append([x, y, z])

        records.append(mark)

    return records

# Get the coordinates for the crypt and the vilosity
def ComputeMainAxis(records):
    vilosity = np.array(records[2])
    crypt_bottom = np.array(records[0])
    crypt_top = np.array(records[1])
    main_axis = vilosity - crypt_bottom    
    return main_axis

# Compute the cell repartition with respect to the chosen referential, and show statistics
def ComputeCellCoordinates(records, main_axis, start, normalized = True):
    coord = np.array([0,0])

    length = np.sqrt( float(main_axis[0] * main_axis[0] + main_axis[1] * main_axis[1] + main_axis[2] * main_axis[2]) )

    for item in records[3]:
        pose = [item[0] - start[0], item[1] - start[1], item[2] - start[2]]
        coord_raw = pose[0] * main_axis[0] + pose[1] * main_axis[1] + pose[2] * main_axis[2]
        coord_raw = max(coord_raw/length, 0)
                
        if normalized:
            coord_normalized = coord_raw / length
            coord = np.append( coord, coord_normalized)
        else:
            coord = np.append( coord, coord_raw)
            
    return coord

# Plot an histogram
def PlotHisto(coords):
    histNBin = 30
    bins = np.linspace(start = 0, stop = 1, num = histNBin)
    histRange = [0, 1.0]
    mp.figure()
    mp.hist(coords, bins, range = histRange)
    mp.xlim(xmax = 1.0)
    mp.show()

# Compute Probability density through KDE

def ComputeKDE(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1), **kwargs)
    return kde.evaluate(x_grid)

# Pipeline for one file
def Pipeline(file, normalized = True):
    records = ParseCellXML(file)
    if len(records) > 0:
        main_axis = ComputeMainAxis(records)
        # records[0][0] : bas de la crypte, records[1][0] haut de la crypte
        res = ComputeCellCoordinates(records, main_axis[0], records[0][0],normalized)
        return res

    else:
        return []

# Get all the XML files in this folder and plot
def FolderPipeline(folder, params):
    coord_ovrl = np.array([])

    files = glob.glob(folder + "/*.xml")

    file_exist = False

    for file in files:
        print "Reading "+file
        res = Pipeline(file, params.normalized)

        if len(res) > 0:
            file_exist = True
            coord_ovrl = np.append(coord_ovrl, res)

    if file_exist:
        # Compute the probability density
        xBins = np.linspace( start=params.xStart, stop=params.xStop, num=params.nBins )
        pdf = ComputeKDE(coord_ovrl, xBins, params.bandwidth)

        # Plot PDF and histogram
        mp.figure()
        
        if params.normalized:
            mp.hist(coord_ovrl, xBins, normed=True)
            mp.xlim([params.xStart, params.xStop])
        else:
            mp.hist(coord_ovrl, params.nBins, normed=True)
        
        mp.plot(xBins, pdf, color='blue', alpha=0.5, lw=3)
        title = folder.split('/')
        mp.title(title[-1])
        mp.savefig(folder + '/histogram.png', bbox_inches='tight')
        mp.show()

        return [pdf, title[-1]]

    else:
        return []

# Get all the subfolders and plot
dirList = os.listdir(os.path.dirname(os.path.realpath(__file__))) # current directory

# Define all the settings
paramsNorm = Settings()
paramsNorm.bandwidth = 0.01 # PDF smoothness
paramsNorm.nBins = 30
paramsNorm.xStart = 0
paramsNorm.xStop = 1
paramsNorm.normalized = True

paramsRaw = Settings()
paramsRaw.bandwidth = 40 # PDF smoothness
paramsRaw.nBins = 30
paramsRaw.xStart = 0
paramsRaw.xStop = 1500
paramsRaw.normalized = False

params = paramsRaw

curves = []
titles = []

for dir in dirList:
    folder = os.path.dirname(os.path.realpath(__file__)) + '/' + dir

    if os.path.isdir(folder):
            [pdf, title] = FolderPipeline(folder, params)
            if len(pdf) > 0:
                curves.append(pdf)
                titles.append(title)

# Plot all the curves on one figure
mp.figure()
xBins = np.linspace(start=params.xStart, stop=params.xStop, num=params.nBins)
for curve in curves:
    mp.plot(xBins, curve, alpha=0.5, lw=3)
    
mp.legend(titles)
mp.show()