Install the latest
===================

To install the latest version of streamdeck_ui simply run:

`pip3 install streamdeck_ui`

OR

`poetry add streamdeck_ui`

OR

`pipenv install streamdeck_ui`


Changelog
=========
## 1.0.6 (test.pypi.org)
- Require Pillow 8.2.
- Fix button image rendering on startup.
- Fix command line args not working.
## 1.0.5 (test.pypi.org)
- Fix race condition where streamdeck buttons get scrambled.
- Avoid uncessary writes to settings file.
- Fix missing remove image button.
## 1.0.4 (test.pypi.org)
- Separator added between Exit and other menu items.
- Image button defaults to previous image path, if there is one.
- Remove image button added. Cancelling image selection no longer removes image.
## 1.0.3 (test.pypi.org)
- Missing icon error handling added.
- Supports `delay` in Key Press action to add a 0.5 second delay.
- Avoid losing config if exception during write.
- Wait for Stream Deck to be attached on startup.
- Drag and drop support for rearranging buttons around in UI.
- Supports `plus` and `comma` in the Key Press action to output `+` and `,` respectively.
- Fixed `core dumped` error when closing.
- Improved error handling for invalid command or key press actions.
- Window title updated to `Stream Deck UI`.
- Launch minimized with `-n` or `--no-ui`.
- Fixed black on black color issue on UI buttons.
- Fixed low quality jpeg artifacts on Stream Deck buttons.
- Removed requirement for plugdev group.
- Improved parsing of command line args for launching programs.

## 1.0.2 - November 25th 2019
- Updated driver requirement to enable full compatiblity with XL.

## 1.0.1 - October 8th 2019
- Initial API stable release.
