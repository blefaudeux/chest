#!/bin/bash

# Query the current state, and flip it
STATUS=$(glxinfo | grep "OpenGL vendor" | cut -d: -f2)
echo "Current status : using ${STATUS}"

echo "Do you want to switch cards ?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) break;;
        No ) echo "Not switching" exit;;
    esac
done


function switch_nvidia {
    echo "Setting up SDDM..."
    sudo cp /usr/share/sddm/scripts/Xsetup.nvidia /usr/share/sddm/scripts/XSetup
    echo "Done"

    # Install the nvidia libs
    echo "Setting up GL libs.."
    yaourt -Sy nvidia-libgl lib32-nvidia-libgl
    echo "Done"

    # Install the Xorg config
    echo "Setting up Xorg"
    sudo cp /etc/X11/xorg.conf.nvidia /etc/X11/xorg.conf
    echo "Done"
}

function switch_intel {
    echo "Setting up SDDM.."
    sudo cp /usr/share/sddm/scripts/Xsetup.intel /usr/share/sddm/scripts/XSetup
    echo "Done"
    
    echo "Setting up GL libs.."
    yaourt -Sy mesa-libgl lib32-mesa-libgl
    echo "Done"

    # Install the Xorg config
    echo "Setting up Xorg"
    sudo cp --backup=t /etc/X11/xorg.conf /etc/X11/ 
    echo "Done"
}

# Explain which card will be used from now on, and apply
IS_INTEL=$(echo ${STATUS} | grep "Intel")
if [ -n "${IS_INTEL}" ]; 
    then
        echo "Switching to NVIDIA card"
        switch_nvidia
    
    else
        echo "Switching to INTEL card"
        switch_intel
fi
