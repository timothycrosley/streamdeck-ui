#!/bin/sh
#########################################################################################################
# Shell-based (POSIX) plugin for streamdeck-ui by Sawy7															#
# Switching between two pipewire audio devices; change these settings:											#
#########################################################################################################

# TIP: To get this sink's name type 'wpctl status' into terminal and look for 'Audio->Sinks' section
devone_name=""
# Device picture path - can be relative to this script or absolute
devone_image="assets/speakers.png"

# TIP: To get this sink's name type 'wpctl status' into terminal and look for 'Audio->Sinks' section
devtwo_name=""
# Device picture path - can be relative to this script or absolute
devtwo_image="assets/headphones.png"

#########################################################################################################
# Don't change anything past this line unless you know what you're doing.								#
#########################################################################################################

script_path=$(dirname "$0")
if [ "$(echo $devone_image | cut -c1-1)" != "/" ]; then
	devone_image="$script_path/$devone_image"
fi
if [ "$(echo $devtwo_image | cut -c1-1)" != "/" ]; then
	devtwo_image="$script_path/$devtwo_image"
fi

if [ "$devone_name" = "" ] || [ "$devtwo_name" = "" ]; then
	echo "{\"streamdeck-plugin\":{\"tasks\":[{\"function\":\"set_button_icon\",\"data\":\"$script_path/assets/noconf.png\"}]}}"
	exit
fi

devone_id=$(wpctl status | grep "$devone_name" | grep "\d+" -Po | head -n 1)
devtwo_id=$(wpctl status | grep "$devtwo_name" | grep "\d+" -Po | head -n 1)

unused_devices=$(wpctl status | sed -n '/Sink endpoints/q;p' | sed -n '/Sinks/,/ ├/p' | grep '[0-9]' | grep -v '\*' | sed -r 's/.* ([0-9]+)\. .*/\1/')

for device in $unused_devices
do
    if [ "$device" = "$devone_id" ] || [ "$device" = "$devtwo_id" ]; then
		second_device=$device
	fi
done

if [ "$second_device" = "$devone_id" ]; then
	new_image=$devone_image
else
	new_image=$devtwo_image
fi

echo "{\"streamdeck-plugin\":{\"tasks\":[{\"function\":\"set_button_icon\",\"data\":\"$new_image\"}]}}"

wpctl set-default "$second_device"
