"""Defines shared configuration variables for the streamdeck_ui project"""
import json
import os
from typing import Dict

from streamdeck_ui.model import ButtonMultiState, ButtonState, DeckState, DeckStateV1

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_NAME = "StreamDeck UI"
APP_LOGO = os.path.join(PROJECT_PATH, "logo.png")
FONTS_PATH = os.path.join(PROJECT_PATH, "fonts", "roboto")
FONTS_FALLBACK_PATH = os.path.join(PROJECT_PATH, "fonts", "roboto")
DEFAULT_FONT = "Roboto-Regular.ttf"
DEFAULT_FONT_FALLBACK_PATH = os.path.join(FONTS_FALLBACK_PATH, DEFAULT_FONT)
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT_COLOR = "#ffffff"
DEFAULT_BACKGROUND_COLOR = "#000000"
STATE_FILE = os.environ.get("STREAMDECK_UI_CONFIG", os.path.expanduser("~/.streamdeck_ui.json"))
LOG_FILE = os.environ.get("STREAMDECK_UI_LOG_FILE", os.path.expanduser("~/.streamdeck_ui.log"))
STATE_FILE_BACKUP = os.path.expanduser("~/.streamdeck_ui.json_old")
CONFIG_FILE_VERSION = 2
CONFIG_FILE_PREVIOUS_VERSION = 1
CONFIG_FILE_SUPPORTED_VERSIONS = [CONFIG_FILE_VERSION, CONFIG_FILE_PREVIOUS_VERSION]
WARNING_ICON = os.path.join(PROJECT_PATH, "icons", "warning_icon_button.png")


def config_file_need_migration(config_file_path: str) -> bool:
    """Check if the config file need to be updated"""
    if not os.path.isfile(config_file_path):
        return False
    with open(config_file_path, "r") as config_file:
        config = json.load(config_file)
        file_version = config.get("streamdeck_ui_version", CONFIG_FILE_VERSION)
        return file_version != CONFIG_FILE_VERSION


def do_config_file_backup(config_file_path: str, backup_config_file_path: str) -> None:
    """Make a copy of the config file"""
    if os.path.isfile(config_file_path):
        os.replace(config_file_path, backup_config_file_path)


def do_config_file_migration() -> None:
    """Update the config file to the latest version"""
    state = read_state_from_config(STATE_FILE)
    do_config_file_backup(STATE_FILE, STATE_FILE_BACKUP)
    write_state_to_config(STATE_FILE, state)


def read_state_from_config(config_file_path: str) -> Dict[str, DeckState]:
    """Open the config file and return its content as a dict"""

    with open(config_file_path, "r") as config_file:
        config = json.load(config_file)
        file_version = config.get("streamdeck_ui_version", 0)
        if file_version not in CONFIG_FILE_SUPPORTED_VERSIONS:
            raise ValueError(
                f"Incompatible version of config file found: {file_version} does not match required version {CONFIG_FILE_VERSION}."
            )
        if file_version == CONFIG_FILE_PREVIOUS_VERSION:
            return _migrate_deck_state_from_previous_version(config["state"])
        return _to_deck_states(config["state"])


def write_state_to_config(config_file_path: str, state: Dict[str, DeckState]) -> None:
    """Write the state to the config file"""
    temp_file_path = config_file_path + ".tmp"
    try:
        with open(temp_file_path, "w") as config_file:
            config = {
                "state": _to_deck_config(state),
                "streamdeck_ui_version": CONFIG_FILE_VERSION,
            }
            json.dump(config, config_file, indent=4)
    except Exception as error:
        raise ValueError(f"The configuration file '{config_file_path}' was not updated. Error: {error}")
    else:
        os.replace(temp_file_path, os.path.realpath(config_file_path))


def _to_deck_states(state: dict) -> Dict[str, DeckState]:
    return {
        deck_id: DeckState(
            buttons={
                int(page_of_buttons_id): {
                    int(button_id): _to_button_multi_state(button)
                    for button_id, button in page_of_buttons_state.items()
                }
                for page_of_buttons_id, page_of_buttons_state in deck_state["buttons"].items()
            },
            display_timeout=deck_state["display_timeout"],
            brightness=deck_state["brightness"],
            brightness_dimmed=deck_state["brightness_dimmed"],
            rotation=deck_state["rotation"],
            page=deck_state["page"],
        )
        for deck_id, deck_state in state.items()
    }


def _migrate_deck_state_from_previous_version(state: dict) -> Dict[str, DeckState]:
    deck_state = _to_deck_states_v1(state)
    return {
        deck_id: DeckState(
            buttons={
                page_of_buttons_id: {
                    button_id: _migrate_button_state_to_multi_state(button)
                    for button_id, button in page_of_buttons_state.items()
                }
                for page_of_buttons_id, page_of_buttons_state in deck_state.buttons.items()
            },
            display_timeout=deck_state.display_timeout,
            brightness=deck_state.brightness,
            brightness_dimmed=deck_state.brightness_dimmed,
            rotation=deck_state.rotation,
            page=deck_state.page,
        )
        for deck_id, deck_state in deck_state.items()
    }


def _migrate_button_state_to_multi_state(button: ButtonState) -> ButtonMultiState:
    return ButtonMultiState(
        state=0,
        states={
            0: button,
        },
    )


def _to_deck_states_v1(state: dict) -> Dict[str, DeckStateV1]:
    """Convert a dict to a DeckStateV1 object"""
    return {
        deck_id: DeckStateV1(
            buttons={
                int(page_of_buttons_id): {
                    int(button_id): _to_button_state(button) for button_id, button in page_of_buttons_state.items()
                }
                for page_of_buttons_id, page_of_buttons_state in deck_state.get("buttons", {}).items()
            },
            display_timeout=deck_state.get("display_timeout", 0),
            brightness=deck_state.get("brightness", 0),
            brightness_dimmed=deck_state.get("brightness_dimmed", 0),
            rotation=deck_state.get("rotation", 0),
            page=deck_state.get("page", 0),
        )
        for deck_id, deck_state in state.items()
    }


def _to_button_state(button: dict) -> ButtonState:
    """Convert a dict to a ButtonState object"""
    return ButtonState(
        text=button.get("text", ""),
        icon=button.get("icon", ""),
        keys=button.get("keys", ""),
        write=button.get("write", ""),
        command=button.get("command", ""),
        switch_page=button.get("switch_page", 0),
        switch_state=button.get("switch_state", 0),
        brightness_change=button.get("brightness_change", 0),
        text_vertical_align=button.get("text_vertical_align", ""),
        text_horizontal_align=button.get("text_horizontal_align", ""),
        font=button.get("font", ""),
        font_color=button.get("font_color", ""),
        font_size=button.get("font_size", 0),
        background_color=button.get("background_color", ""),
    )


def _to_button_multi_state(button: dict) -> ButtonMultiState:
    return ButtonMultiState(
        state=button.get("state", 0),
        states={int(state_id): _to_button_state(state) for state_id, state in button.get("states", {}).items()},
    )


def _to_deck_config(state: Dict[str, DeckState]) -> dict:
    return {
        deck_id: {
            "buttons": {
                page_of_buttons_id: {
                    button_id: _to_multi_state_button_config(button)
                    for button_id, button in page_of_buttons_state.items()
                }
                for page_of_buttons_id, page_of_buttons_state in deck_state.buttons.items()
            },
            "display_timeout": deck_state.display_timeout,
            "brightness": deck_state.brightness,
            "brightness_dimmed": deck_state.brightness_dimmed,
            "rotation": deck_state.rotation,
            "page": deck_state.page,
        }
        for deck_id, deck_state in state.items()
    }


def _to_button_config(button: ButtonState) -> dict:
    """Convert a ButtonState object to a dict"""
    return {
        "text": button.text,
        "icon": button.icon,
        "keys": button.keys,
        "write": button.write,
        "command": button.command,
        "brightness_change": button.brightness_change,
        "switch_page": button.switch_page,
        "switch_state": button.switch_state,
        "text_vertical_align": button.text_vertical_align,
        "text_horizontal_align": button.text_horizontal_align,
        "font": button.font,
        "font_color": button.font_color,
        "font_size": button.font_size,
        "background_color": button.background_color,
    }


def _to_multi_state_button_config(button: ButtonMultiState) -> dict:
    return {
        "state": button.state,
        "states": {state_id: _to_button_config(state) for state_id, state in button.states.items()},
    }
