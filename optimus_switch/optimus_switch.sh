#!/bin/sh

# Query the current state, and flip it
# TODO: Ben

# Change the SDDM status
echo "Setting up SDDM..."
sudo mv /usr/share/sddm/scripts/Xsetup.nvidia 
/usr/share/sddm/scripts/XSetup
echo "Done"

# Install the nvidia libs
echo "Setting up GL libs.."
yaourt -Sy nvidia-libgl lib32-nvidia-libgl

# Install the mesa libs
#yaourt -Sy mesa-libgl lib32-mesa-libgl
echo "Done"

# Install the Xorg config
echo "Setting up Xorg"
sudo mv /etc/X11/xorg.conf.nvidia /etc/X11/xorg.conf

echo "Done"
