# Installing on Ubuntu
This has been tested on Ubuntu 2004, 2204, Linux Mint 20.

## Install hidapi
``` console
sudo apt install libhidapi-libusb0 python3-pip
```

> Note that for version `2.0.6` and below, you also need to install `libxcb-xinerama0` (include it with apt in the line above). 
## Set path
You need to add `~/.local/bin` to your path. Be sure to add this to your `.bashrc` (or equivalent) file so it automatically sets it for you in future.
``` console
PATH=$PATH:$HOME/.local/bin
```
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

### From Pypi with pip
```bash
python3 -m pip install streamdeck-ui --user
```

### From Surce 
Please make sure you have followed the steps below untill the **Install Stream Deck UI section** before continuing.


The steps to install from source can be found [here](source.md)


### Launch the Streamdeck UI
Launch with
```bash
streamdeck
```

See [troubleshooting](../troubleshooting.md) for tips if you're stuck.
