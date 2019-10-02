import json
import os
import threading
from functools import partial
from subprocess import Popen
from typing import Dict, List, Tuple, Union

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.ImageHelpers import PILHelper

FONTS_PATH = os.path.join(os.path.dirname(__file__), "fonts")
DEFAULT_FONT = os.path.join("roboto", "Roboto-Regular.ttf")
STATE_FILE = os.environ.get("STREAMDECK_UI_CONFIG", os.path.expanduser("~/.streamdeck_ui.json"))

decks: Dict[str, StreamDeck] = {deck.id().decode(): deck for deck in DeviceManager().enumerate()}
state: Dict[str, Dict[int, Dict[str, str]]] = {}
if os.path.isfile(STATE_FILE):
    with open(STATE_FILE) as state_file:
        for deck, buttons in json.loads(state_file.read()).items():
            state[deck] = {int(button_id): button for button_id, button in buttons.items()}


def _key_change_callback(deck_id: str, _deck: StreamDeck, key: int, state: bool) -> None:
    if state:
        command = get_button_command(deck_id, key)
        if command:
            Popen(command.split(" "))


def _save_state():
    with open(STATE_FILE, "w") as state_file:
        state_file.write(json.dumps(state))


def open_decks() -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    """Opens and then returns all known stream deck devices"""
    for deck_id, deck in decks.items():
        deck.open()
        deck.reset()
        deck.set_key_callback(partial(_key_change_callback, deck_id))

    return {
        deck_id: {"type": deck.deck_type(), "layout": deck.key_layout()}
        for deck_id, deck in decks.items()
    }


def set_button_text(deck_id: str, button: int, text: str) -> None:
    """Set the text associated with a button"""
    state.setdefault(deck_id, {}).setdefault(button, {})["text"] = text
    render()
    _save_state()


def get_button_text(deck_id: str, button: int) -> str:
    """Returns the text set for the specified button"""
    return state.get(deck_id, {}).get(button, {}).get("text", "")


def set_button_icon(deck_id: str, button: int, icon: str) -> None:
    """Sets the icon associated with a button"""
    state.setdefault(deck_id, {}).setdefault(button, {})["icon"] = icon
    render()
    _save_state()


def get_button_icon(deck_id: str, button: int) -> str:
    """Returns the icon set for a particular button"""
    return state.get(deck_id, {}).get(button, {}).get("icon", "")


def set_button_command(deck_id: str, button: int, command: str) -> None:
    """Sets the command associated with the button"""
    state.setdefault(deck_id, {}).setdefault(button, {})["command"] = command
    _save_state()


def get_button_command(deck_id: str, button: int) -> str:
    """Returns the command set for the specified button"""
    return state.get(deck_id, {}).get(button, {}).get("command", "")


def render() -> None:
    """renders all decks"""
    for deck_id, buttons in state.items():
        deck = decks[deck_id]
        for button_id, button_settings in buttons.items():
            if "text" in button_settings or "icon" in button_settings:
                image = render_key_image(deck, **button_settings)
                deck.set_key_image(button_id, image)


def render_key_image(deck, icon: str = "", text: str = "", font: str = DEFAULT_FONT, **kwargs):
    # Create new key image of the correct dimensions, black background
    image = PILHelper.create_image(deck)
    draw = ImageDraw.Draw(image)

    # Add image overlay, rescaling the image asset if it is too large to fit
    # the requested dimensions via a high quality Lanczos scaling algorithm
    if icon:
        rgba_icon = Image.open(icon).convert("RGBA")
    else:
        rgba_icon = Image.new("RGBA", (300, 300))
    rgba_icon.thumbnail((image.width, image.height - 20), Image.LANCZOS)
    icon_pos = ((image.width - rgba_icon.width) // 2, 0)
    image.paste(rgba_icon, icon_pos, rgba_icon)

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image
    true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)
    label_w, label_h = draw.textsize(text, font=true_font)
    label_pos = ((image.width - label_w) // 2, image.height - 20)
    draw.text(label_pos, text=text, font=true_font, fill="white")

    return PILHelper.to_native_format(deck, image)
