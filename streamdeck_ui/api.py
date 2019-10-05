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

from streamdeck_ui.config import DEFAULT_FONT, FONTS_PATH, STATE_FILE

keyboard = Controller()
decks: Dict[str, StreamDeck] = {}
state: Dict[str, Dict[str, Union[int, Dict[int, Dict[int, Dict[str, str]]]]]] = {}
if os.path.isfile(STATE_FILE):
    with open(STATE_FILE) as state_file:
        for deck_id, deck in json.loads(state_file.read()).items():
            deck["buttons"] = {
                int(page_id): {int(button_id): button for button_id, button in buttons.items()}
                for page_id, buttons in deck.get("buttons", {}).items()
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
            for section in keys.split(","):
                for key_name in section.split("+"):
                    keyboard.press(getattr(Key, key_name, key_name))
                for key_name in section.split("+"):
                    keyboard.release(getattr(Key, key_name, key_name))

        write = get_button_write(deck_id, key)
        if write:
            keyboard.type(write)

        brightness_change = get_button_change_brightness(deck_id, key)
        if brightness_change:
            change_brightness(deck_id, brightness_change)


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


def get_deck(deck_id: str) -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    return {"type": decks[deck_id].deck_type(), "layout": decks[deck_id].key_layout()}


def _button_state(deck_id: str, page: int, button: int) -> dict:
    buttons_state = state.setdefault(deck_id, {}).setdefault("buttons", {}).setdefault(page, {})
    return buttons_state.setdefault(button, {})  # type: ignore


def set_button_text(deck_id: str, page: int, button: int, text: str) -> None:
    """Set the text associated with a button"""
    _button_state(deck_id, page, button)["text"] = text
    render()
    _save_state()


def get_button_text(deck_id: str, page: int, button: int) -> str:
    """Returns the text set for the specified button"""
    return _button_state(deck_id, page, button).get("text", "")


def set_button_icon(deck_id: str, page: int, button: int, icon: str) -> None:
    """Sets the icon associated with a button"""
    _button_state(deck_id, page, button)["icon"] = icon
    render()
    _save_state()


def get_button_icon(deck_id: str, page: int, button: int) -> str:
    """Returns the icon set for a particular button"""
    return _button_state(deck_id, page, button).get("icon", "")


def set_button_change_brightness(deck_id: str, page: int, button: int, amount: int) -> None:
    """Sets the brightness changing associated with a button"""
    _button_state(deck_id, page, button)["brightness_change"] = amount
    render()
    _save_state()


def get_button_change_brightness(deck_id: str, page: int, button: int) -> int:
    """Returns the brightness change set for a particular button"""
    return _button_state(deck_id, page, button).get("brightness_change", 0)


def set_button_command(deck_id: str, page: int, button: int, command: str) -> None:
    """Sets the command associated with the button"""
    _button_state(deck_id, page, button)["command"] = command
    _save_state()


def get_button_command(deck_id: str, page: int, button: int) -> str:
    """Returns the command set for the specified button"""
    return _button_state(deck_id, page, button).get("command", "")


def set_button_keys(deck_id: str, page: int, button: int, keys: str) -> None:
    """Sets the keys associated with the button"""
    _button_state(deck_id, page, button)["keys"] = keys
    _save_state()


def get_button_keys(deck_id: str, page: int, button: int) -> str:
    """Returns the keys set for the specified button"""
    return _button_state(deck_id, page, button).get("keys", "")


def set_button_write(deck_id: str, page: int, button: int, write: str) -> None:
    """Sets the text meant to be written when button is pressed"""
    _button_state(deck_id, page, button)["write"] = write
    _save_state()


def get_button_write(deck_id: str, page: int, button: int) -> str:
    """Returns the text to be produced when the specified button is pressed"""
    return _button_state(deck_id, page, button).get("write", "")


def set_brightness(deck_id: str, brightness: int) -> None:
    """Sets the brightness for every button on the deck"""
    decks[deck_id].set_brightness(brightness)
    state.setdefault(deck_id, {})["brightness"] = brightness
    _save_state()


def get_brightness(deck_id: str) -> int:
    """Gets the brightness that is set for the specified stream deck"""
    return state.get(deck_id, {}).get("brightness", 100)  # type: ignore


def change_brightness(deck_id: str, amount: int = 1) -> None:
    """Change the brightness of the deck by the specified amount"""
    set_brightness(deck_id, max(min(get_brightness(deck_id) + amount, 100), 0))


def render() -> None:
    """renders all decks"""
    for deck_id, deck_state in state.items():
        deck = decks[deck_id]
        page = deck_state.get("current_page", 0)
        for button_id, button_settings in (
            deck_state.get("buttons", {}).get(page, {}).items()
        ):  # type: ignore
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
