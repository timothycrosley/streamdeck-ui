"""Defines shared configuration variables for the streamdeck_ui project"""
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(PROJECT_PATH, "logo.png")
FONTS_PATH = os.path.join(PROJECT_PATH, "fonts")
DEFAULT_FONT = os.path.join("roboto", "Roboto-Regular.ttf")
STATE_FILE = os.environ.get("STREAMDECK_UI_CONFIG", os.path.expanduser("~/.streamdeck_ui.json"))
CONFIG_FILE_VERSION = 1  # Update only if backward incompatible changes are made to the config file
