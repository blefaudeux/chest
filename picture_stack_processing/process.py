#!/usr/bin/env python
import os
from subprocess import call

path, _ = os.path.split(os.path.abspath(__file__))

print path


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Just go through and list files
for _, dirnames, _ in os.walk(path):
    print "Found directories : {}\n".format(dirnames)

    for directory in dirnames:
        print "\nAppropriate files in {}".format(directory)

        for _, _, records in os.walk(directory):
            file_list = []

            # Find the relevant files in this folder
            for record in records:
                if record.split(".")[-1] == "tif":
                    print "Registering {}".format(record)
                    file_list.append(record)

            # Process all the files
            # - Ask for the desired levels
            keep_going = True
            black_lvl = -1
            white_lvl = -1

            while keep_going:
                black_lvl = raw_input("Desired black level :")
                keep_going = not(is_number(black_lvl))

            keep_going = True
            while keep_going:
                white_lvl = raw_input("Desired white level :")
                keep_going = not(is_number(white_lvl) and white_lvl > black_lvl)

            print("Registered ({},{})".format(black_lvl, white_lvl))

            # - Write the macro file
            os.makedirs(path + "/" + directory + "/8bits")
            macro = open(path + "/" + directory + "/" + "macro_8bits.ijm", 'w')
            macro.write("run(\"Window/Level...\");\n")
            min_max = "setMinAndMax({}, {});\n".format(int(black_lvl), int(white_lvl))
            macro.write(min_max)
            macro.write("run(\"8-bit\");\n")
            macro.write("path = getInfo(\"image.directory\")"
                             "+File.separator+\"8bits\"+File.separator+getInfo(\"image.filename\");\n")
            macro.write("saveAs(\"Tiff\", path);\n")
            macro.write("close();\n")
            macro.close()

            # - Run imageJ with the macro file
            for filename in file_list:
                call(["imagej", path + "/" + directory + "/" + filename, "-e macro_8bits.ijm"])

