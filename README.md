[![streamdeck_ui - Linux compatible UI for the Elgato Stream Deck](docs/art/logo_large.png)](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui)
_________________

[![PyPI version](https://badge.fury.io/py/streamdeck-linux-gui.svg)](https://pypi.org/project/streamdeck-linux-gui/)
[![Build Status](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/actions/workflows/test.yaml/badge.svg)](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/actions/workflows/test.yaml?query=branch%3Amain)
[![Docs Status](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/actions/workflows/docs.yml/badge.svg)](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/streamdeck-linux-gui/streamdeck-linux-gui/branch/main/graph/badge.svg?token=I4WC0MVVZ3)](https://codecov.io/gh/streamdeck-linux-gui/streamdeck-linux-gui)
[![Join Discord](https://img.shields.io/badge/Join%20Discord-Discord-green?labelColor=Blue&style=flat&logo=discord&link=https://discord.gg/ZCZesnEj4)](https://discord.gg/ZCZesnEj4)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)

_________________

**streamdeck-linux-gui** A Linux compatible UI for the Elgato Stream Deck.

This project is a fork and drop-in replacement for [streamdeck_ui](https://github.com/timothycrosley/streamdeck-ui), which is no longer maintained.
This still keeps the original code and intends to pick up where the original left off.

All credit to the orignal authors, and the many contributors to the project.


![Streamdeck UI Usage Example](docs/art/example.gif)

## Key Features

* **Linux Compatible**: Enables usage of Stream Deck devices (Original, MK2, Mini and XL) on Linux.
* **Multi-device**: Enables connecting and configuring multiple Stream Decks on one computer.
* **Brightness Control**: Supports controlling the brightness from both the configuration UI and buttons on the device itself.
* **Configurable Button Display**: Icons + Text, Icon Only, and Text Only configurable per button on the Stream Deck.
* **Multi-Action Support**: Run commands, write text and press hotkey combinations at the press of a single button on your Stream Deck.
* **Button Pages**: streamdeck_ui supports multiple pages of buttons and dynamically setting up buttons to switch between those pages.
* **Auto Reconnect**: Automatically and gracefully reconnects, in the case the device is unplugged and replugged in.
* **Import/Export**: Supports saving and restoring Stream Deck configuration.
* **Drag/Drop**: Move buttons by simply drag and drop.
* **Drag/Drop Image**: Configure a button image by dragging it from your file manager onto the button.
* **Auto Dim**: Configure the Stream Deck to automatically dim the display after a period of time. A button press wakes it up again.
* **Animated icons**: Use an animated gif to liven things up a bit.
* **Runs under systemd**: Run automatically in the background as a systemd --user service.
* **Stream Deck Pedal**: Supports actions when pressing pedals.

# Documentation

Communication with the Stream Deck is powered by the [Python Elgato Stream Deck Library](https://github.com/abcminiuser/python-elgato-streamdeck#python-elgato-stream-deck-library).

Documentation is available at [https://streamdeck-linux-gui.github.io/streamdeck-linux-gui/](https://streamdeck-linux-gui.github.io/streamdeck-linux-gui/)

## Installation Guides
* [Arch/Manjaro](docs/installation/arch.md)
* [CentOS](docs/installation/centos.md)
* [Fedora](docs/installation/fedora.md)
* [openSUSE](docs/installation/opensuse.md)
* [Ubuntu/Mint](docs/installation/ubuntu.md)

Once you're up and running, consider installing a [systemd service](docs/installation/systemd.md).

> Use the [troubleshooting](docs/troubleshooting.md) guide or [search](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/issues?q=is%3Aissue) the issues for guidance. If you cannot find on the issue on this repository please try searching on the original at [streamdeck_ui](https://githib.com/timothycrosley/streamdeck_ui/issues?q=is%Aissue).

### Precooked Scripts
There are scripts for setting up streamdeck_ui on [Debian/Ubuntu](scripts/ubuntu_install.sh) and [Fedora](scripts/fedora_install.sh).

## Updating Documentation

Documentation is powered by mkdocs-material, and its on the [docs](docs/) folder. Install it with `pip install mkdocs-material` and run `mkdocs serve` to see the changes locally, before submitting a PR.


## Development & Contributions

Contributuions encouraged and very welcome, however some rules and guidelines must be followed! 

### General Guidelines

- The project is versioned according to [Semantic Versioning](https://semver.org/).
- When writing your commit messages, please follow the [Angular commit message](https://gist.github.com/brianclements/841ea7bffdb01346392c).
- Pull requests should be made against the `develop` branch, so please make sure you check out the `develop` branch.
- Pull requests should include tests and documentation as appropriate.
- When opening a pull request, if possible, attach a screenshot or GIF of the changes.
- Please read the [contributing guide](https://www.notion.so/cfcolaco/docs/contributing.md) for more information and instructions on how to get started.

## Known issues

- pip package is not yet available for the current state of the project. Please install from source, currently trying to find a better way to provide the package.
- Streamdeck uses [pynput](https://github.com/moses-palmer/pynput) for simulating **Key Presses** but it lacks proper [support for Wayland](https://github.com/moses-palmer/pynput/issues/189). Generally your results will be good when using X (Ubuntu/Linux Mint). [This thread](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/issues/47) may be useful.
- **Key Press** or **Write Text** does not work on Fedora (outside of the streamdeck itself), which is not particularly useful. However, still do a lot with the **Command** feature.
- Some users have reported that the Stream Deck device does not work on all on specific USB ports, as it draws quite a bit of power and/or has [strict bandwidth requirements](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/issues/69#issuecomment-715887397). Try a different port.
- If you are executing a shell script from the Command feature - remember to add the shebang at the top of your file, for the language in question. `#!/bin/bash` or `#!/usr/bin/python3` etc. The streamdeck may appear to lock up if you don't under some distros.
