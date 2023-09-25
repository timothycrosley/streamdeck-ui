"""Defines shared configuration variables for the streamdeck_ui project"""
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_NAME = "StreamDeck UI"
APP_LOGO = os.path.join(PROJECT_PATH, "logo.png")
FONTS_FALLBACK_PATH = os.path.join(PROJECT_PATH, "fonts", "roboto")
DEFAULT_FONT = "Roboto-Regular.ttf"
DEFAULT_FONT_FALLBACK_PATH = os.path.join(FONTS_FALLBACK_PATH, DEFAULT_FONT)
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT_COLOR = "white"
DEFAULT_BACKGROUND_COLOR = "#000000"
STATE_FILE = os.environ.get("STREAMDECK_UI_CONFIG", os.path.expanduser("~/.streamdeck_ui.json"))
CONFIG_FILE_VERSION = 1  # Update only if backward incompatible changes are made to the config file
