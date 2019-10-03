import json
import os
import threading
from functools import partial
from subprocess import Popen
from typing import Dict, List, Tuple, Union

from PIL import Image, ImageDraw, ImageFont
from pynput.keyboard import Controller, Key
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.ImageHelpers import PILHelper

FONTS_PATH = os.path.join(os.path.dirname(__file__), "fonts")
DEFAULT_FONT = os.path.join("roboto", "Roboto-Regular.ttf")
STATE_FILE = os.environ.get("STREAMDECK_UI_CONFIG", os.path.expanduser("~/.streamdeck_ui.json"))

keyboard = Controller()
decks: Dict[str, StreamDeck] = {}
state: Dict[str, Dict[str, Union[int, Dict[int, Dict[str, str]]]]] = {}
if os.path.isfile(STATE_FILE):
    with open(STATE_FILE) as state_file:
        for deck_id, deck in json.loads(state_file.read()).items():
            deck["buttons"] = {
                int(button_id): button for button_id, button in deck.get("buttons", {}).items()
            }
            state[deck_id] = deck


def _key_change_callback(deck_id: str, _deck: StreamDeck, key: int, state: bool) -> None:
    if state:
        command = get_button_command(deck_id, key)
        if command:
            Popen(command.split(" "))

        keys = get_button_keys(deck_id, key)
        if keys:
            keys = keys.strip().replace(" ", "")
            for sections in keys.split(","):
                for key in keys.split("+"):
                    keyboard.press(getattr(Key, key, key))
                for key in keys.split("+"):
                    keyboard.release(getattr(Key, key, key))

        write = get_button_write(deck_id, key)
        if write:
            keyboard.type(write)


def _save_state():
    with open(STATE_FILE, "w") as state_file:
        state_file.write(json.dumps(state))


def open_decks() -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    """Opens and then returns all known stream deck devices"""
    for deck in DeviceManager().enumerate():
        deck.open()
        deck.reset()
        deck_id = deck.get_serial_number()
        decks[deck_id] = deck
        deck.set_key_callback(partial(_key_change_callback, deck_id))

    return {
        deck_id: {"type": deck.deck_type(), "layout": deck.key_layout()}
        for deck_id, deck in decks.items()
    }


def _button_state(deck_id: str, button: int) -> dict:
    buttons_state = state.setdefault(deck_id, {}).setdefault("buttons", {})
    return buttons_state.setdefault(button, {})  # type: ignore


def set_button_text(deck_id: str, button: int, text: str) -> None:
    """Set the text associated with a button"""
    _button_state(deck_id, button)["text"] = text
    render()
    _save_state()


def get_button_text(deck_id: str, button: int) -> str:
    """Returns the text set for the specified button"""
    return _button_state(deck_id, button).get("text", "")


def set_button_icon(deck_id: str, button: int, icon: str) -> None:
    """Sets the icon associated with a button"""
    _button_state(deck_id, button)["icon"] = icon
    render()
    _save_state()


def get_button_icon(deck_id: str, button: int) -> str:
    """Returns the icon set for a particular button"""
    return _button_state(deck_id, button).get("icon", "")


def set_button_command(deck_id: str, button: int, command: str) -> None:
    """Sets the command associated with the button"""
    _button_state(deck_id, button)["command"] = command
    _save_state()


def get_button_command(deck_id: str, button: int) -> str:
    """Returns the command set for the specified button"""
    return _button_state(deck_id, button).get("command", "")


def set_button_keys(deck_id: str, button: int, keys: str) -> None:
    """Sets the keys associated with the button"""
    _button_state(deck_id, button)["keys"] = keys
    _save_state()


def get_button_keys(deck_id: str, button: int) -> str:
    """Returns the keys set for the specified button"""
    return _button_state(deck_id, button).get("keys", "")


def set_button_write(deck_id: str, button: int, write: str) -> None:
    """Sets the text meant to be written when button is pressed"""
    _button_state(deck_id, button)["write"] = write
    _save_state()


def get_button_write(deck_id: str, button: int) -> str:
    """Returns the text to be produced when the specified button is pressed"""
    return _button_state(deck_id, button).get("write", "")


def set_brightness(deck_id: str, brightness: int) -> None:
    decks[deck_id].set_brightness(brightness)
    state.setdefault(deck_id, {})["brightness"] = brightness
    _save_state()


def get_brightness(deck_id: str) -> int:
    return state.get(deck_id, {}).get("brightness", 100)  # type: ignore


def render() -> None:
    """renders all decks"""
    for deck_id, deck_state in state.items():
        deck = decks[deck_id]
        for button_id, button_settings in deck_state.get("buttons", {}).items():  # type: ignore
            if "text" in button_settings or "icon" in button_settings:
                image = _render_key_image(deck, **button_settings)
                deck.set_key_image(button_id, image)


def _render_key_image(deck, icon: str = "", text: str = "", font: str = DEFAULT_FONT, **kwargs):
    """Renders an individual key image"""
    image = PILHelper.create_image(deck)
    draw = ImageDraw.Draw(image)

    if icon:
        rgba_icon = Image.open(icon).convert("RGBA")
    else:
        rgba_icon = Image.new("RGBA", (300, 300))

    icon_width, icon_height = image.width, image.height
    if text:
        icon_height -= 20

    rgba_icon.thumbnail((icon_width, icon_height), Image.LANCZOS)
    icon_pos = ((image.width - rgba_icon.width) // 2, 0)
    image.paste(rgba_icon, icon_pos, rgba_icon)

    if text:
        true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)
        label_w, label_h = draw.textsize(text, font=true_font)
        label_pos = ((image.width - label_w) // 2, image.height - 20)
        draw.text(label_pos, text=text, font=true_font, fill="white")

    return PILHelper.to_native_format(deck, image)
