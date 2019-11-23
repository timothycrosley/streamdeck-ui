[![streamdeck_ui - Linux compatible UI for the Elgato Stream Deck](https://raw.githubusercontent.com/timothycrosley/streamdeck-ui/master/art/logo_large.png)](https://timothycrosley.github.io/streamdeck-ui/)
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

![Streamdeck UI Usage Example](https://raw.github.com/timothycrosley/streamdeck-ui/master/art/example.gif)

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

To use streamdeck_ui on Linux, you will need first to install some pre-requisite system libraries and give your user access to the Stream Deck devices.

[Here](https://github.com/timothycrosley/streamdeck-ui/blob/master/scripts/ubuntu_install.sh) is a simple script for doing that on Ubuntu:

```bash
#!/bin/bash -xe

sudo apt install libhidapi-hidraw0 libudev-dev libusb-1.0-0-dev

sudo usermod -a -G plugdev `whoami`

sudo tee /etc/udev/rules.d/99-streamdeck.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", MODE:="666", GROUP="plugdev"
EOF

sudo udevadm control --reload-rules

echo "Unplug and replug in device for the new udev rules to take effect"
```

As mentioned in the echo in the last line, make sure you unplug and replug your device before continuing.
Once complete, you should be able to install streamdeck_ui:

```bash
sudo pip3 install streamdeck_ui
```

You can then launch `streamdeck` to start configuring your device.

```bash
streamdeck
```

It's recommended that you include `streamdeck` in your windowing environment's list of applications to auto-start.

## Generic Quick Start

On other Operating Systems, or if you already have the required libraries and permissions, you should be able to install and run streamdeck_ui:

```bash
pip3 install streamdeck_ui --user
streamdeck
```
