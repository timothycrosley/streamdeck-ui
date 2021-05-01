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
## 1.1.2 - April 30, 2021
### Fixes
- Regression with multi-character keys
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
