# Installing on Fedora
This has been tested on Fedora 36, 37.

## Install hidapi
``` bash
sudo dnf install python3-pip python3-devel hidapi
```

## Upgrade pip
You need to upgrade pip, using pip. In my experience, old versions of pip may fail to properly install some of the required Python dependencies.
```
python -m pip install --upgrade pip
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
See [system tray](../troubleshooting.md#no-system-tray-indicator) installation.

Launch with
```
streamdeck
```
See [troubleshooting](../troubleshooting.md) for tips if you're stuck.
