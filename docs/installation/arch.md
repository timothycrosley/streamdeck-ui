# Installing on Arch
This has been tested on Arch with XFCE, Manjaro in Feb 2023.

## Install hidapi
``` console
sudo pacman -S hidapi python-pip qt6-base
```
## Set path
You need to add `~/.local/bin` to your path. Be sure to add this to your `.bashrc` (or equivalent) file so it automatically sets it for you in future.
``` console
PATH=$PATH:$HOME/.local/bin
```

## Upgrade pip
You may need to upgrade pip, using pip. On Arch this is usually not required.
Setuptools is required but may not be installed on Arch.
```
python -m pip install --upgrade pip
python -m pip install setuptools
```
## Configure access to Elgato devices
The following will create a file called `/etc/udev/rules.d/70-streamdeck.rules` and add the following text to it: `SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"`. Creating this file adds a udev rule that provides your user with access to USB devices created by Elgato.
``` bash
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
```
For the rule to take immediate effect, run the following command:
``` bash
sudo udevadm trigger
```
If the software is having problems later to detect the Stream Deck, you can try unplugging/plugging it back in.

## Install Stream Deck UI
```
python -m pip install streamdeck-ui --user
```

Launch with
```
streamdeck
```
See [troubleshooting](../troubleshooting.md) for tips if you're stuck.
