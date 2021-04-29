[![streamdeck_ui - Linux compatible UI for the Elgato Stream Deck](art/logo_large.png)](https://timothycrosley.github.io/streamdeck-ui/)
_________________

[![PyPI version](https://badge.fury.io/py/streamdeck-ui.svg)](http://badge.fury.io/py/streamdeck-ui)
[![Test Status](https://github.com/timothycrosley/streamdeck-ui/workflows/Test/badge.svg?branch=master)](https://github.com/timothycrosley/streamdeck-ui/actions?query=workflow%3ATest)
[![codecov](https://codecov.io/gh/timothycrosley/streamdeck-ui/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/streamdeck-ui)
[![Join the chat at https://gitter.im/timothycrosley/streamdeck-ui](https://badges.gitter.im/timothycrosley/streamdeck-ui.svg)](https://gitter.im/timothycrosley/streamdeck-ui?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/streamdeck-ui/)
[![Downloads](https://pepy.tech/badge/streamdeck-ui)](https://pepy.tech/project/streamdeck-ui)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
 
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
**Python 3.8** is required. You can check which version you have installed with `python3 --version`.
### Precooked Scripts
There are scripts for setting up streamdeck_ui on [Debian/Ubuntu](scripts/ubuntu_install.sh) and [Fedora](scripts/fedora_install.sh).
### Manual installation
To use streamdeck_ui on Linux, you will need first to install some prerequisite system libraries.
The name of those libraries will differ depending on your Operating System.  
Debian / Ubuntu:
``` console
sudo apt install python3-pip libhidapi-libusb0 libxcb-xinerama0
```
Fedora:
``` console
sudo dnf install python3-pip python3-devel hidapi
```
If you're using GNOME shell, you might need to manually install an extension that adds [KStatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/) to make the tray icon show up.

To use streamdeck_ui without root permissions, you have to give your user full access to the device.

Add the udev rules using your text editor:
``` console
sudoedit /etc/udev/rules.d/70-streamdeck.rules
# If that doesn't work, try:
sudo nano /etc/udev/rules.d/70-streamdeck.rules
```
Paste the following lines:
``` console
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"
```
Reload the rules:
``` console
sudo udevadm control --reload-rules
```
Make sure you unplug and replug your device before continuing.
Once complete, you should be able to install streamdeck_ui.
Installing the application itself is done via pip:
``` console
pip3 install streamdeck-ui --user
```
Make sure to include `$HOME/.local/bin` to your PATH.  
If you haven't already, add
``` console
PATH=$PATH:$HOME/.local/bin
```
to the bottom your shell config file (most likely .bashrc in your home directory)

You can then launch `streamdeck` to start configuring your device.

``` console
streamdeck
```

It's recommended that you include `streamdeck` in your windowing environment's list of applications to auto-start.

## Generic Quick Start

On other Operating Systems, you'll need to install the required [dependencies](https://github.com/abcminiuser/python-elgato-streamdeck#package-dependencies) of the library.
After that, use pip to install the app:

``` console
pip3 install streamdeck-ui --user
streamdeck
```

See the guide for
* [CentOS 7](docs/centos.md)
* [Ubuntu 18.04](docs/ubuntu1804.md)

## Help
### Command
Enter a value in the command field to execute a command. For example, `gnome-terminal` will launch a new terminal on Ubuntu/Fedora or `obs` will launch OBS.

#### Some examples (Ubuntu)
You can use a tool like `xdotool` to interact with other applications.

Find the window with a title starting with `Meet - ` and bring it to focus. This helps if you have a Google Meet session on a tab somewhere but you lost it behind another window. 
``` console
xdotool search --name '^Meet - .+$' windowactivate 
```
> The meeting tab must be active one if you have multiple tabs open, since the window title is set by the currently active tab.

Find the window with a title starting with `Meet - ` and then send `ctrl+d` to it. This has the effect of toggling the mute button in Google Meet.
``` console
xdotool search --name '^Meet - .+$' windowactivate --sync key ctrl+d
```

Change the system volume up (or down) by a certain percentage. Assumes you're using PulseAudio/Alsa Mixer.
``` console
amixer -D pulse sset Master 20%+
```
### Press Keys
Simulates key press combinations (hot keys). The basic format is a group of keys, separated by a `+` sign to press simultaneously. Separate key combination groups with a `,` if additional key combinations are needed. For example, `alt+F4,f` means press and hold `alt`, followed by `F4` and then release both. Next, press and release `f`. 

> Use `comma` or `plus` if you want to actually *output* `,` or `+` respectively.
> 
> Use `delay <n>` to add a delay, where `<n>` is the number (float or integer) of seconds to delay. If `<n>` is not specified, 0.5 second default is used. If `<n>` fails to parse as a valid number, it will result in no delay.
> 

#### Examples
- `F11` - Press F11. If you have focus on a browser, this will toggle full screen.
- `alt+F4` - Closes the current window.
- `ctrl+w` - Closes the current browser tab.
- `cmd+left` - View split on left. Note `cmd` is the **super** key (equivalent of the Windows key).
- `alt+plus` - Presses the alt and the `+` key at the same time.
- `alt+delay+F4` - Press alt, then wait 0.5 seconds, then press F4. Release both.
- `1,delay,delay,2,delay,delay,3` - Type 123 with a 1-second delay between key presses (using default delay).
- `1,delay 1,2,delay 1,3` - Type 123 with a 1-second delay between key presses (using custom delay).


The standard list of keys can be found [at the source](https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key).

## Known issues
Confirm you are running the latest release with `pip3 show streamdeck-ui`. Compare it to: [![PyPI version](https://badge.fury.io/py/streamdeck-ui.svg)](http://badge.fury.io/py/streamdeck-ui)

- Streamdeck uses [pynput](https://github.com/moses-palmer/pynput) for simulating **Key Presses** but it lacks proper [support for Wayland](https://github.com/moses-palmer/pynput/issues/189). Generally your results will be good when using X (Ubuntu/Linux Mint). [This thread](https://github.com/timothycrosley/streamdeck-ui/issues/47) may be useful.
- **Key Press** or **Write Text** does not work on Fedora (outside of the streamdeck itself), which is not particularly useful. However, still do a lot with the **Command** feature.
- On Ubuntu, the **Key Press** `ctrl+alt+t` [doesn't work](https://github.com/moses-palmer/pynput/issues/333
). However using the **Command** `gnome-terminal` achieves the same result.
- Version [1.0.2](https://pypi.org/project/streamdeck-ui/) lacks error handling when executing **Command** and **Key Press** actions. As a result, you have to be careful - an invalid command or key press makes everything else also stop working.  Please upgrade to the latest version.
- Some users have reported that the Stream Deck device does not work on all on specific USB ports, as it draws quite a bit of power and/or has [strict bandwidth requirements](https://github.com/timothycrosley/streamdeck-ui/issues/69#issuecomment-715887397). Try a different port.
