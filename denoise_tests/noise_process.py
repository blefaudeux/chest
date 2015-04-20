# Author : blefaudeux@github

from __future__ import division
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
bi_diameter = 5
bi_sigma = 100

# - Median blur
med_ksize = 5   # Even number !


def nlm(pict):  # Dedicated processing
    global nl_strength, nl_templateWindowSize, nl_searchWindowSize
    return cv2.fastNlMeansDenoising(pict, None, nl_strength, nl_templateWindowSize, nl_searchWindowSize)


def bilateral(pict):
    global bi_diameter, bi_sigma
    return cv2.bilateralFilter(pict, bi_diameter, bi_sigma, bi_sigma)


def median(pict):
    global med_ksize
    return cv2.medianBlur(pict, med_ksize)

img_nlm = nlm(img)
img_bi = bilateral(img)
img_med = median(img)

# Multi plots & slider callbacks
f, ax = plt.subplots()
plt.subplots_adjust(left=0.2)

ax_nl_strength = plt.axes([0.03, 0.5, 0.02, 0.4], axisbg='lightgoldenrodyellow')  # left, bottom, width, height
ax_nl_templ = plt.axes([0.06, 0.5, 0.02, 0.4], axisbg='lightgoldenrodyellow')
ax_nl_sws = plt.axes([0.09, 0.5, 0.02, 0.4], axisbg='lightgoldenrodyellow')
ax_bi_diam = plt.axes([0.03, 0.05, 0.02, 0.4], axisbg='lightgoldenrodyellow')  # left, bottom, width, height
ax_bi_sigma = plt.axes([0.06, 0.05, 0.02, 0.4], axisbg='lightgoldenrodyellow')
ax_med_k = plt.axes([0.09, 0.05, 0.02, 0.4], axisbg='lightgoldenrodyellow')

s_nl_strength = VertSlider(ax_nl_strength, 'NLStrength', 0.1, 30.0, valinit=nl_strength)
s_nl_templ = VertSlider(ax_nl_templ, 'NLTemplateSize', 1, 10, valinit=nl_templateWindowSize)
s_nl_search = VertSlider(ax_nl_sws, 'NLSearchSize', 1, 10, valinit=nl_searchWindowSize)
s_bi_diam = VertSlider(ax_bi_diam, 'BilDiam', 1, 20, valinit=bi_diameter)
s_bi_sigma = VertSlider(ax_bi_sigma, 'BilSigma', 1, 200, valinit=bi_sigma)
s_med_k = VertSlider(ax_med_k, 'MedSize', 1, 10, valinit=med_ksize)


def update(val):   # Global callback
    global img_nlm, img_med, img_bi

    # Non local means
    global nl_strength, nl_templateWindowSize, nl_searchWindowSize, bi_diameter, bi_sigma, med_ksize
    nl_strength = int(s_nl_strength.val)
    nl_templateWindowSize = int(s_nl_templ.val)
    nl_searchWindowSize = int(s_nl_search.val)
    img_nlm = nlm(img)

    # Billateral filter:
    bi_diameter = int(s_bi_diam.val)
    bi_sigma = int(s_bi_sigma.val)
    img_bi = bilateral(img)

    # Median blur
    med_ksize = int(s_med_k.val)
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

s_nl_strength.on_changed(update)
s_nl_templ.on_changed(update)
s_nl_search.on_changed(update)
s_bi_diam.on_changed(update)
s_bi_sigma.on_changed(update)
s_med_k.on_changed(update)

update(None)

plt.show()
