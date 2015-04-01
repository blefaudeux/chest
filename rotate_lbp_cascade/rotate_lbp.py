
import xml.etree.ElementTree as etree
import numpy as np
import re


def rotateLBPStage(inputTree):
    stages = inputTree.findall("cascade/stages/_/weakClassifiers")

    for inner_tree in stages:
        nodes = inner_tree.findall("_/internalNodes")
        for node in nodes:
            old_text = node.text

            # Rotate the node values
            text = re.split(' |\n', old_text)
            c = [item for item in text if (item != '' and item != '\n')]

            # Naive rotation, let's see whether this works..
            rotated_text = [c[0], c[1], c[2], c[5], c[6], c[7], c[8], c[9], c[10], c[3], c[4]]

            # Crush the values
            node.text = ""
            for n in c:		# rotated_text
                node.text += " " + str(n)


def rotateLBPFeature(inputTree):
    width = int(inputTree.find("cascade/width").text)
    height = int(inputTree.find("cascade/height").text)

    features = inputTree.findall("cascade/features/_/rect")

    for rect in features:
        old_text = rect.text
        text = re.split(' |\n', old_text)
        c = [item for item in text if (item != '' and item != '\n')]

        # The two first values are the rectangle initial coordinates, the two last its extend (width and height)
        rotated_text = [c[1], width-int(c[0])-int(c[2])-1, c[3], c[2]]

        # Crush the values
        rect.text = " "
        for n in rotated_text:
            rect.text += str(n) + " "


tree = etree.parse('lbpcascade_frontalface.xml')

# Rotate stages and features in place
rotateLBPStage(tree)
rotateLBPFeature(tree)

# Save the file (with the xml declaration)
tree.write('lbpcascade_frontalface_rotated.xml', xml_declaration=True, encoding="utf-8")

# FIXME: ET saves the declaration with single quotes instead of double quotes