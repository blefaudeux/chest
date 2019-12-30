#!/usr/bin/env python3

import argparse
from pathlib import Path
import functools
import operator

RAW_FILEFORMATS = ["CR2", "RW2", "NEF"]
JPG_FILEFORMATS = ["JPG", "jpg"]


def run(args):
    folderpath = Path(args.folderpath)

    # List all RAW files
    if args.raw_format == "":
        list_raws = list(
            map(lambda x: list(folderpath.glob("**/*."+x)), RAW_FILEFORMATS))

    else:
        list_raws = list(folderpath.glob(
            "**/*." + args.raw_format.replace(".", "")))

    # Flatten lists
    list_raws = functools.reduce(operator.concat, list_raws)

    # List all JPG files
    list_jpgs = list(folderpath.glob("**/*.jpg")) + \
        list(folderpath.glob("**/*.JPG"))

    # Find duplicated files
    remove_jpg = not args.remove_raw
    for filepath in list_raws:
        # Check whether the same file is in the jpgs list
        candidate = Path(filepath.parent / (filepath.stem + ".JPG"))
        if candidate in list_jpgs:
            index = list_jpgs.index(candidate)
            print("{} and {} are duplicates".format(
                filepath, list_jpgs[index]))

            if remove_jpg:
                list_jpgs[index].unlink()
            else:
                filepath.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove RAW/Jpg duplicates')

    parser.add_argument(
        'folderpath', help="path of the folder you would like to process", type=str)

    parser.add_argument(
        '--raw_format', help="raw file format to consider --else defaults--", default="", type=str)

    parser.add_argument("--remove_raw", default=False, type=bool)

    args = parser.parse_args()
    run(args)
