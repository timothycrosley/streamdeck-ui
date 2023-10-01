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

## Install with the AUR
The AUR currently has an [easy install script](https://aur.archlinux.org/packages/streamdeck-ui) that is being maintained by dhtseany. 
There may be more packages that need to be installed before the script will run, after you install those you should be able to finish installing. 
``` bash
cd Downloads 
git clone https://aur.archlinux.org/streamdeck-ui.git
cd streamdeck-ui
makepkg
sudo pacman -U streamdeck-ui-3.1.0-1-any.pkg.tar.zst
```
You can also install the [Development branch](https://aur.archlinux.org/packages/streamdeck-ui-develop) if you want to stay up to date with improvements.
Both of these will install an icon in your programs list. 

## Install with yay
[yay is a Pacman wrapper and AUR helper](https://aur.archlinux.org/packages/yay) that will download and install all of the prerequisites for you, along with the StreamDeck UI app itself. 
``` bash
yay -S streamdeck-ui
```
To open you can use the new icon that is added to your programs list. 
