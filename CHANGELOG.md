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
## 1.0.3 - TBD
- Wait for Stream Deck to be attached on startup.
- Drag and drop support for rearranging buttons around in UI.
- Supports `plus` in the Key Press action to output `+`.
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
