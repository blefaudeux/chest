#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
from matplotlib import pyplot as plt
import os

from VertSlider import *

# List all files in the folder
f = []
for (dirpath, dirnames, filenames) in os.walk("."):
    f.extend(filenames)
    break

for file in f:
    if file[-3:] == 'png':
        break

img = cv2.imread(file)

# Settings
# - Non-local means:
nl_strength = 3
nl_templateWindowSize = 7
nl_searchWindowSize = 21

# - Bilateral filter
bi_diameter = 5             # Real time.. bigger slows things down
bi_sigma_colour = 100       # The bigger, the more cartoonish
bi_sigma_space = 100        # The bigger, the more cartoonish

# - Median blur
med_ksize = 5   # Even number !


# Dedicated processing
def nlm(pict):
    global nl_strength, nl_templateWindowSize, nl_searchWindowSize
    return cv2.fastNlMeansDenoising(pict, None, nl_strength, nl_templateWindowSize, nl_searchWindowSize)


def bilateral(pict):
    global bi_diameter, bi_sigma_colour, bi_sigma_space
    return cv2.bilateralFilter(pict, bi_diameter, bi_sigma_colour, bi_sigma_space)


def median(pict):
    global med_ksize
    return cv2.medianBlur(pict, med_ksize)

img_nlm = nlm(img)
img_bi = bilateral(img)
img_med = median(img)

# Multi plots & slider callbacks
f, ax = plt.subplots()
plt.subplots_adjust(left=0.1, right=0.87)

ax_nl_strength = plt.axes([0.88, 0.5, 0.01, 0.4], axisbg='lightgoldenrodyellow')  # left, bottom, width, height
ax_nl_templ = plt.axes([0.925, 0.5, 0.01, 0.4], axisbg='lightgoldenrodyellow')
ax_nl_sws = plt.axes([0.97, 0.5, 0.01, 0.4], axisbg='lightgoldenrodyellow')

ax_bi_diam = plt.axes([0.02, 0.05, 0.01, 0.4], axisbg='lightgoldenrodyellow')  # left, bottom, width, height
ax_bi_sigma_c = plt.axes([0.05, 0.05, 0.01, 0.4], axisbg='lightgoldenrodyellow')
ax_bi_sigma_s = plt.axes([0.08, 0.05, 0.01, 0.4], axisbg='lightgoldenrodyellow')

ax_med_k = plt.axes([0.925, 0.05, 0.01, 0.4], axisbg='lightgoldenrodyellow')

s_nl_strength = VertSlider(ax_nl_strength, 'NLStrength', 0.1, 30.0, valinit=nl_strength)
s_nl_templ = VertSlider(ax_nl_templ, 'NLTemplateSize', 1, 10, valinit=nl_templateWindowSize)
s_nl_search = VertSlider(ax_nl_sws, 'NLSearchSize', 1, 10, valinit=nl_searchWindowSize)
s_bi_diam = VertSlider(ax_bi_diam, 'BilDiam', 1, 20, valinit=bi_diameter)
s_bi_sigma_c = VertSlider(ax_bi_sigma_c, 'BilSigmaC', 1, 200, valinit=bi_sigma_colour)
s_bi_sigma_s = VertSlider(ax_bi_sigma_s, 'BilSigmaS', 1, 200, valinit=bi_sigma_space)
s_med_k = VertSlider(ax_med_k, 'MedSize', 1, 10, valinit=med_ksize)


def update(val):   # Global callback
    global img_nlm, img_med, img_bi
    global nl_strength, nl_templateWindowSize, nl_searchWindowSize
    global bi_diameter, bi_sigma_colour, bi_sigma_space
    global med_ksize

    # Non local means
    nl_strength = int(s_nl_strength.val)
    nl_templateWindowSize = int(s_nl_templ.val)
    nl_searchWindowSize = int(s_nl_search.val)
    img_nlm = nlm(img)

    # Billateral filter:
    bi_diameter = int(s_bi_diam.val)
    bi_sigma_colour = int(s_bi_sigma_c.val)
    bi_sigma_space = int(s_bi_sigma_s.val)
    img_bi = bilateral(img)

    # Median blur
    med_ksize = int(s_med_k.val)
    med_ksize += (med_ksize + 1) % 2    # Make it an even number
    img_med = median(img)

    # Plots
    plt.subplot(221)
    plt.imshow(img)
    plt.title("RAW")

    fig_nlm = plt.subplot(222)
    plt.imshow(img_nlm)
    plt.title("Non local means")

    fig_bi = plt.subplot(223)
    plt.imshow(img_bi)
    plt.title("Billateral")

    fig_median = plt.subplot(224)
    plt.imshow(img_med)
    plt.title("Median blur")

    f.canvas.draw_idle()

# Connect the signals and callbacks
s_nl_strength.on_changed(update)
s_nl_templ.on_changed(update)
s_nl_search.on_changed(update)
s_bi_diam.on_changed(update)
s_bi_sigma_c.on_changed(update)
s_bi_sigma_s.on_changed(update)
s_med_k.on_changed(update)

update(None)

plt.show()
