[![streamdeck_ui - Linux compatible UI for the Elgato Stream Deck](art/logo_large.png)](https://timothycrosley.github.io/streamdeck-ui/)
_________________

[![PyPI version](https://badge.fury.io/py/streamdeck-ui.svg)](http://badge.fury.io/py/streamdeck-ui)
[![Build Status](https://travis-ci.org/timothycrosley/streamdeck-ui.svg?branch=master)](https://travis-ci.org/timothycrosley/streamdeck-ui)
[![codecov](https://codecov.io/gh/timothycrosley/streamdeck-ui/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/streamdeck-ui)
[![Join the chat at https://gitter.im/timothycrosley/streamdeck-ui](https://badges.gitter.im/timothycrosley/streamdeck-ui.svg)](https://gitter.im/timothycrosley/streamdeck-ui?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/streamdeck-ui/)
[![Downloads](https://pepy.tech/badge/streamdeck-ui)](https://pepy.tech/project/streamdeck-ui)
_________________

[Read Latest Documentation](https://timothycrosley.github.io/streamdeck-ui/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/streamdeck-ui/)
_________________

**streamdeck_ui** A Linux compatible UI for the Elgato Stream Deck.

![Streamdeck UI Usage Example](art/example.gif)

## Key Features

* **Linux Compatible**: Enables usage of all Stream Deck devices on Linux without needing to code.
* **Multi-device**: Enables connecting and configuring multiple Stream Deck devices on one computer.
* **Brightness Control**: Supports controlling the brightness from both the configuration UI and buttons on the device itself.
* **Configurable Button Display**: Icons + Text, Icon Only, and Text Only configurable per button on the Stream Deck.
* **Multi-Action Support**: Run commands, write text and press hotkey combinations at the press of a single button on your Stream Deck.
* **Button Pages**: streamdeck_ui supports multiple pages of buttons and dynamically setting up buttons to switch between those pages.
* **Auto Reconnect**: Automatically and gracefully reconnects, in the case the device is unplugged and replugged in.
* **Import/Export**: Supports saving and restoring Stream Deck configuration.

Communication with the Streamdeck is powered by the [Python Elgato Stream Deck Library](https://github.com/abcminiuser/python-elgato-streamdeck#python-elgato-stream-deck-library).

## Linux Quick Start
### Precooked Scripts
There are scripts for setting up streamdeck_ui on [Debian/Ubuntu](scripts/ubuntu_install.sh) and [Fedora](scripts/fedora_install.sh).
### Manual installation
To use streamdeck_ui on Linux, you will need first to install some pre-requisite system libraries.
The name of those libraries will differ depending on your Operating System.  
Debian / Ubuntu:
```bash
sudo apt-get install libhidapi-hidraw0 libudev-dev libusb-1.0-0-dev
```
Fedora:
```bash
sudo dnf install python3-devel libusb-devel
```
If you're using GNOME shell, you might need to manually install an extension that adds [KStatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/) to make the tray icon show up.

To use streamdeck_ui without root permissions, you have to give your user full access to the device.

Add your user to the 'plugdev' group:
```bash
sudo usermod -a -G plugdev `whoami`
```
Add the udev rules using your favorite text editor:
```bash
sudo nano /etc/udev/rules.d/99-streamdeck.rules
```
Paste the following lines:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", MODE:="666", GROUP="plugdev"
```
Reload the rules:
```
sudo udevadm control --reload-rules
```
Make sure you unplug and replug your device before continuing.
Once complete, you should be able to install streamdeck_ui.
Installing the application itself is done via pip: To install the app system-wide, run:
```bash
pip3 install --user streamdeck_ui
```
You can then launch `streamdeck` to start configuring your device.

```bash
streamdeck
```

It's recommended that you include `streamdeck` in your windowing environment's list of applications to auto-start.

## Generic Quick Start

On other Operating Systems, you'll need to install the required [dependencies](https://github.com/abcminiuser/python-elgato-streamdeck#package-dependencies) of the library.
After that, use pip to install the app:

```bash
pip3 install streamdeck_ui --user
streamdeck
```
