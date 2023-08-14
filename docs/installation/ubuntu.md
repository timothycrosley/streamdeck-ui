# Installing on Debian and ubuntu derivatives

This has been tested on Debian 12

## Install hidapi and pipx

```bash
sudo apt install libhidapi-libusb0 pipx
```

> Note that for version `2.0.6` and below, you also need to install `libxcb-xinerama0` (include it with apt in the line above).
>
## Set path

You need to add `~/.local/bin` to your path. Be sure to add this to your `.bashrc` (or equivalent) file so it automatically sets it for you in future.

```ini
PATH=$PATH:$HOME/.local/bin
```

## Configure access to Elgato devices

The following will create a file called `/etc/udev/rules.d/70-streamdeck.rules` and add the following text to it: `SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"`. Creating this file adds a udev rule that provides your user with access to USB devices created by Elgato.

```bash
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
```

For the rule to take immediate effect, run the following command:

```bash
sudo udevadm trigger
```

If the software is having problems later to detect the Stream Deck, you can try unplugging/plugging it back in.

## Install Stream Deck UI

### From Pypi with pipx

```bash
python3 -m pipx install streamdeck-linux-gui
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
