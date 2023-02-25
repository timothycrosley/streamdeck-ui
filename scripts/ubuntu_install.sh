#!/bin/bash -xe
echo "Installing libraries"
sudo apt install python3-pip libhidapi-libusb0 libxcb-xinerama0

echo "Adding udev rules and reloading"
sudo tee /etc/udev/rules.d/70-streamdeck.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
EOF
sudo udevadm trigger

pip3 install --user streamdeck_ui
echo "If the installation was successful, run 'streamdeck' to start."
