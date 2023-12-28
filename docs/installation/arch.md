# Installing on Arch

This has been tested on:

* Arch with Plasma (July 2023)
* Arch with Cinnamon (October 2023)
* Arch with Gnome (Per every release, thanks to dhtseany)

## Install Dependencies

```bash
sudo pacman -S hidapi qt6-base
```

## Set path

You need to add `~/.local/bin` to your path. Be sure to add this to your `.bashrc` (or equivalent) file, so it automatically sets it for you in the future.

```ini
PATH=$PATH:$HOME/.local/bin
```

## Configure access to Elgato devices

The following will create a file called `/etc/udev/rules.d/70-streamdeck.rules` and add the following text to it: `SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"`. Creating this file adds a udev rule that provides your user with access to USB devices created by Elgato.

```bash
sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0fd9\", TAG+=\"uaccess\"" > /etc/udev/rules.d/70-streamdeck.rules'
sudo sh -c 'echo "KERNEL==\"uinput\", SUBSYSTE==\misc\, TAG+=\"uaccess\"" >> /etc/udev/rules.d/70-streamdeck.rules'
```

For the rule to take immediate effect, run the following command:

```bash
sudo udevadm trigger
```

If the software is having problems later to detect the Stream Deck, you can try unplugging/plugging it back in.

## Install Streamdeck

### From Pypi with pipx

```bash
sudo pacman -S python-pipx
```

```console
pipx install  streamdeck-linux-gui
```

### From Source

Please make sure you have followed [Install dependencies](#install-dependencies) and [Configure access to Elgato devices](#configure-access-to-elgato-devices) before continuing.

The steps to install from source can be found [here](source.md)

### Install with the AUR

The AUR currently has an [easy install script](https://aur.archlinux.org/packages/streamdeck-ui) that is being maintained by dhtseany.
> Additional packages may be required before the script will finish, once those have been installed the script will finish installing.

``` bash
cd Downloads
git clone https://aur.archlinux.org/streamdeck-ui.git
cd streamdeck-ui
makepkg
sudo pacman -U streamdeck-ui-3.1.0-1-any.pkg.tar.zst
```

### Install with yay

[yay is a Pacman wrapper and AUR helper](https://aur.archlinux.org/packages/yay) that will download and install all of the prerequisites for you, along with the StreamDeck UI app itself.

``` bash
yay -S streamdeck-ui
```

> For both yay and the AUR you can also install the [Development branch](https://aur.archlinux.org/packages/streamdeck-ui-develop) if you want to stay on the bleeding edge or help with testing.

## Launch the Streamdeck UI

Launch with

```bash
streamdeck
```

See [troubleshooting](../troubleshooting.md) for tips if you're stuck.
