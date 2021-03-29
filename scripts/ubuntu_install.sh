#!/bin/bash -xe
echo "Installing libraries"
sudo apt install python3-pip libhidapi-libusb0 qt5-default

echo "Adding udev rules and reloading"
sudo tee /etc/udev/rules.d/70-streamdeck.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"
EOF
sudo udevadm control --reload-rules

echo "Unplug and replug in device for the new udev rules to take effect"
echo "Installing streamdeck_ui"
pip3 install --user streamdeck_ui
echo "If the installation was successful, run 'streamdeck' to start."
