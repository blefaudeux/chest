
import xml.etree.ElementTree as etree
import numpy as np
import re


def rotateLBPStage(inputTree, direction='left'):
    stages = inputTree.findall("cascade/stages/_/weakClassifiers")

    for inner_tree in stages:
        nodes = inner_tree.findall("_/internalNodes")
        for node in nodes:
            old_text = node.text

            # Rotate the node values
            text = re.split(' |\n', old_text)
            c = [item for item in text if (item != '' and item != '\n')]

            rotated_text = []
            if direction == 'left':
                rotated_text = [c[0], c[1], c[2], c[5], c[7], c[10], c[4], c[9], c[3], c[6], c[8]]
                
            elif direction == 'right':
                # to be fixed
                rotated_text = [c[0], c[1], c[2], c[5], c[7], c[10], c[4], c[9], c[3], c[6], c[8]]
                
            elif direction == 'bottom_up':
                # to be fixed
                rotated_text = [c[0], c[1], c[2], c[5], c[7], c[10], c[4], c[9], c[3], c[6], c[8]]
            
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

    for rect in features:
        old_text = rect.text
        text = re.split(' |\n', old_text)
        c = [item for item in text if (item != '' and item != '\n')]

        # The two first values are the rectangle initial coordinates, the two last its extend (width and height)
        rotated_text = []
        if direction == 'left':
            rotated_text = [c[1], width-int(c[0])-int(c[2]), c[3], c[2]]

        elif direction == 'right':
            rotated_text = [c[1], width-int(c[0])-int(c[2]), c[3], c[2]]

        elif direction == 'bottom_up':
            rotated_text = [c[1], width-int(c[0])-int(c[2]), c[3], c[2]]

        else:
            print("This direction is not supported")

        # Crush the values
        rect.text = " "
        for n in rotated_text:
            rect.text += str(n) + " "


# Load the original xml file
tree = etree.parse('lbpcascade_frontalface.xml')

# Rotate stages and features in place
directions = ['left', 'right', 'bottom_up']
for direction in directions :
    print("Rotating cascade to the " + direction)
    rotateLBPStage(tree, direction)
    rotateLBPFeature(tree, direction)
    filename = 'rotated_cascade_' + direction + '.xml'
    tree.write(filename)
    print(".." + filename + " saved\n")
    