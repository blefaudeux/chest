#!/usr/bin/python3

import xml.etree.ElementTree as etree
import numpy as np
import re


# Ref : http://w3facility.org/question/understanding-opencv-lbp-implementation/
def rotateLBPStage(inputTree, direction='left'):
    stages = inputTree.findall("cascade/stages/_/weakClassifiers")

    for inner_tree in stages:
        nodes = inner_tree.findall("_/internalNodes")
        for node in nodes:
            old_text = node.text

            # Rotate the node values
            parsedValues = re.split(' |\n', old_text)
            c = [item for item in parsedValues if (item != '' and item != '\n')]

            weights = [128, 64, 32, 16, 8, 4, 2, 1]

            d = []  # We could check that the weight match here, we should have ints
            d.append(int(c[5]) / weights[2] * weights[0])
            d.append(int(c[6]) / weights[3] * weights[1])
            d.append(int(c[7]) / weights[4] * weights[2])
            d.append(int(c[8]) / weights[5] * weights[3])
            d.append(int(c[9]) / weights[6] * weights[4])
            d.append(int(c[10]) / weights[7]* weights[5])
            d.append(int(c[3]) / weights[0] * weights[6])
            d.append(int(c[4]) / weights[1] * weights[7])

            d = [int(item) for item in d]

            rotated_text = []
            if direction == 'left':
                rotated_text = [c[0], c[1], c[2], str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(d[4]), str(d[5]), str(d[6]), str(d[7])]
                
            elif direction == 'right':
                # to be fixed
                rotated_text = [c[0], c[1], c[2], str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(d[4]), str(d[5]), str(d[6]), str(d[7])]
                
            elif direction == 'bottom_up':
                # to be fixed
                rotated_text = [c[0], c[1], c[2], str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(d[4]), str(d[5]), str(d[6]), str(d[7])]
                
            else :
                print("This direction is not supported")


            # Crush the values
            node.text = ""
            for n in rotated_text:
                node.text += " " + str(n)


def rotateLBPFeature(inputTree, direction = 'left'):
    width = int(inputTree.find("cascade/width").text)
    height = int(inputTree.find("cascade/height").text)

    features = inputTree.findall("cascade/features/_/rect")

    # Change the LUT values
    for rect in features:
        old_text = rect.text
        parsedValues = re.split(' |\n', old_text)
        c = [item for item in parsedValues if (item != '' and item != '\n')]

        # The two first values are the rectangle initial coordinates, the two last its extend (width and height)
        rotated_text = []
        if direction == 'left':
            rotated_text = [c[1], width-int(c[0])-3*int(c[2]), c[3], c[2]]

        elif direction == 'right':
            rotated_text = [c[1], width-int(c[0])-3*int(c[2]), c[3], c[2]]

        elif direction == 'bottom_up':
            rotated_text = [c[1], width-int(c[0])-3*int(c[2]), c[3], c[2]]

        else:
            print("This direction is not supported")

        # Crush the values
        rect.text = " "
        for n in rotated_text:
            rect.text += str(n) + " "

    # Flip width and height values
    width_ref = inputTree.findall("cascade/width")     # Get the handle first
    width_ref[0].text = str(height)

    height_ref = inputTree.findall("cascade/height")
    height_ref[0].text = str(width)


# Load the original xml file
tree = etree.parse('lbpcascade_frontalface.xml')

# Rotate stages and features in place
directions = ['left', 'right', 'bottom_up']
for direction in directions :
    print("Rotating cascade to the " + direction)
    rotateLBPStage(tree, direction)
    rotateLBPFeature(tree, direction)
    filename = 'rotated_cascade_' + direction + '.xml'
    tree.write(filename, xml_declaration=True, encoding="utf-8")

    # Fix an annoying ET bug : replace single quotes by double quotes in the saved file
    f = open(filename, 'r')
    text = f.read()
    f.close()

    f_fixed = open(filename, 'w')
    text = re.sub("\'", '"', text)
    f_fixed.write(text)
    f_fixed.close()
    
    print(".." + filename + " saved\n")
    
