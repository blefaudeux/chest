#!/bin/bash

# This script converts 16-bits pictures into 8 bits, 
# applying levelling in the meantime, and then fuses 
# all pictures in a given subfolder to color channels

EXT=tiff

for d in *; do
	cd $d
	for file in *; do
		# Ask for the levels
		echo "Reading file $file" 
		read -p "What should the black level be ? " black_lvl
		read -p "What should the white level be ? " white_lvl
		
		if [ $black_lvl -gt $white_lvl ]; then
			echo "Switching black and white level, didn't look right"
			temp=black_lvl
			black_lvl=white_lvl
			white_lvl=temp
		fi
	
		# Create the appropriate macro here
		echo "open($file)\n level($black_lvl, $white_lvl)\n save(newPict)" > LevelMacro.ijm
		# TODO : Ben

		# Process the picture using ImageJ
#		imagej --headless LevelMacro.ijm
	done
done



