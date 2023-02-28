Install the latest
===================

To install the latest version of streamdeck_ui simply run:

`pip3 install streamdeck_ui`

OR

`poetry add streamdeck_ui`

OR

`pipenv install streamdeck_ui`


Change log
==========
## 2.0.13 - 27 Feb 2023
### Fixes
- Requirement for Python < 3.11 removed.
- Switched to pyside6.
### Features
- Added support for a new sub-variant of the StreamDeck XL.
- Allow Stream Deck UI to start, even if virtual keyboard won't work.
- Improved troubleshooting messages.
- Updated documentation and installation guides.
## 2.0.6 - 23 Sep 2022
### Fixes
- Image drag/drop from external applications.
- Dimmer not working properly.
## 2.0.5 - 18 Sep 2022
### Features
- Support for new Stream Deck Mini.
### Fixes
- Fix install under Fedora 36 (pillow dependency version bump).
## 2.0.4 - 29 Apr 2022
### Features
- Recover from a suspend/resume cycle.

### Fixes
- Button icon stuck in pushed state when changing from page 1.
- Remove python3-xlib dependency.

## 2.0.3 - 6 Mar 2022

### Features
- UI starts up even if no Stream Deck attached.
- SVG file type support.
- Keys widget now has examples built in.
- Help menu with links to websites.
- About dialog shows application version and primary dependency versions.
- Support hex key codes in Key Press. For example, 0x74.
- Support vertical text alignment.
- New display system:
    - User interface shows same image as Stream Deck.
    - Text overlay on top of image, with automatic font outline.
    - Buttons image change when pressed (visual feedback).
    - Animated GIF support.
    - CPU indicator for display processing.

### Fixes
- Tray context menu not interrupted by window activation.
## 1.1.3 - 2 Feb 2022

### Features
- Support for Stream Deck MK.2 added.
- Remember previous image selection directory.
- Auto dim to a configurable percentage.
- Drag and drop icons onto buttons from file browser.
- Follow the settings file location if symbolic link.

### Fixes
- Works with Python 3.10 (resolves Fedora 35 install).
## 1.1.2 - April 30, 2021
### Fixes
- Regression with multi-character keys.
## 1.1.1 - April 29, 2021
### Features
- Open main window from tray with Configure... menu item.
- Dim the display from tray.
- Supports variable delay duration in Key press action.
### Fixes
- On exit, reset the display to 50% brightness.
- Documentation for Ubuntu 18.04 added.

## 1.1.0 - April 20, 2021
### Features
- Automatically dim the display after a configurable amount of time.

## 1.0.7 - April 6, 2021
### Features
- Drag and drop support for rearranging buttons around in UI.
- Launches minimized with `-n` or `--no-ui`.
- Window title has been updated to `Stream Deck UI`.
- A remove image button has been added. Cancelling during image selection no longer removes image.
- Image selection button defaults to previous image path, if there is one.
- Reset to the standby image after exiting. This makes it easy to see if streamdeck-ui is running or not.
- Supports `delay` in Key Press action to add a 0.5 second delay.
- Supports `plus` and `comma` in the Key Press action to output `+` and `,` respectively.
- Separator added between Exit and other menu items.
- Avoid unnecessary writes to settings file.
- Improved parsing of command line arguments for launching programs.
### Fixes
- Missing button image error handling added.
- Avoid losing configuration if there is an exception while writing file.
- Updated to streamdeck 0.8.4 to improve stability.
- Updated to Pillow 8.2 to improve stability and fixes jpeg artifacts.
- Fixed race condition where streamdeck buttons get scrambled.
- Fixed `core dumped` error when exiting.
- Improved error handling for invalid command or key press actions.
- Fixed black on black color issue on UI buttons.
- Removed requirement for plugdev group.
- Waits for Stream Deck to be attached on start up.

## 1.0.2 - November 25, 2019
- Updated driver requirement to enable full compatibility with XL.

## 1.0.1 - October 8, 2019
- Initial API stable release.
