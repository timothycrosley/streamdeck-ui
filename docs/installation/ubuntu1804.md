# Installing on Ubuntu
This has been tested on Ubuntu 1804.

## Install hidapi
``` console
sudo apt install python3.8 python3.8-dev libhidapi-libusb0
```

> Note that for version `2.0.6` and below, you also need to install `libxcb-xinerama0` (include it with apt in the line above). 

## Upgrade pip
You need to upgrade pip, using pip. In my experience, old versions of pip may fail to properly install some of the required Python dependencies.
```
python3 -m pip install --upgrade pip
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
pip install streamdeck-ui --user
```
You need to add `~/.local/bin` to your path before you can launch. Be sure to add this to your `.bashrc` file so it automatically sets it for you in future.
``` console
PATH=$PATH:$HOME/.local/bin
```
Launch with
```
streamdeck
```
See [troubleshooting](../troubleshooting.md) for tips if you're stuck.






Installing on Ubuntu 18.04
==========================

The following guide was tested on Ubuntu 18.04.

This version of Ubuntu comes with Python 3.6 and we have to install Python 3.8 and then make sure we can also run pip.
Please see this [post](https://stackoverflow.com/a/63207387/) for more details.

``` console
sudo apt install python3.8 python3.8-dev libhidapi-libusb0 libxcb-xinerama0
```
> **Explanation**
>
> * python3.8 - Does a side by side install of python 3.8. Run with `python3.8`. Your python 3.6 can be run with `python3` as per usual.
> * python3.8-dev - Some dependencies need to be built during the install. You'll need this package for that to work.
> * libhidapi-libusb0 - The USB library to communicate to the Stream Deck hardware.
> * libxcb-xinerama0 - Required by pyside2 (the Qt based UI library).

This will install pip for python3.6
``` console
sudo apt install python3-pip
```

Next, we will use the pip module installed in the previous step, to install pip for python 3.8. Yea I know, it's weird, installing pip with pip.
``` console
python3.8 -m pip install pip
```

Before we can run pip3.8, we need to set
``` console
PATH=$PATH:$HOME/.local/bin
```
You should also add this to your .bashrc file.

Confirm you are able to run pip3.8 as follows:
``` console
$ pip3.8 --version
pip 21.0.1 from /home/user/.local/lib/python3.8/site-packages/pip (python 3.8)
```

Install streamdeck-ui
``` console
pip3.8 install streamdeck-ui --user
```

We need configure the USB device to be accessible by the currently logged in user, when it is attached:
``` console
sudo nano /etc/udev/rules.d/70-streamdeck.rules
```
Paste the following line:
``` console
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
```
Reload the rules:
``` console
sudo udevadm control --reload-rules
```
Remove and plug your Stream Deck in.
``` console
streamdeck
```
