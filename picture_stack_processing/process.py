#!/usr/bin/env python
import os

path, _ = os.path.split(os.path.abspath(__file__))

print path

# Just go through and list files
for _, dirnames, _ in os.walk(path):
    print "Found directories : {}\n".format(dirnames)

    for directory in dirnames:
        print "Appropriate files in {}".format(directory)

        for _, _, records in os.walk(directory):
            file_list = []

            # Find the relevant files in this folder
            for record in records:
                if record.split(".")[-1] == "tiff":
                    print "Registering {}".format(record)
                    file_list.append(record)

            # Process all the files
            # TODO: Ben