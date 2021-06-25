"""Defines the Python API for interacting with the StreamDeck Configuration UI"""
import json
import os
import threading
from functools import partial
from io import BytesIO
from typing import Dict, Tuple, Union, cast
from warnings import warn

import cairosvg
from PIL import Image, ImageDraw, ImageFont
from PySide2.QtCore import QObject, Signal
from StreamDeck import DeviceManager
from StreamDeck.Devices import StreamDeck
from StreamDeck.ImageHelpers import PILHelper

from streamdeck_ui.config import CONFIG_FILE_VERSION, DEFAULT_FONT, FONTS_PATH, STATE_FILE

image_cache: Dict[str, memoryview] = {}
decks: Dict[str, StreamDeck.StreamDeck] = {}
state: Dict[str, Dict[str, Union[int, Dict[int, Dict[int, Dict[str, str]]]]]] = {}
streamdecks_lock = threading.Lock()
key_event_lock = threading.Lock()


class KeySignalEmitter(QObject):
    key_pressed = Signal(str, int, bool)


streamdesk_keys = KeySignalEmitter()


def _key_change_callback(deck_id: str, _deck: StreamDeck.StreamDeck, key: int, state: bool) -> None:
    """ Callback whenever a key is pressed. This is method runs the various actions defined
        for the key being pressed, sequentially. """
    # Stream Desk key events fire on a background thread. Emit a signal
    # to bring it back to UI thread, so we can use Qt objects for timers etc.
    # Since multiple keys could fire simultaniously, we need to protect
    # shared state with a lock
    with key_event_lock:
        streamdesk_keys.key_pressed.emit(deck_id, key, state)


def get_display_timeout(deck_id: str) -> int:
    """ Returns the amount of time in seconds before the display gets dimmed."""
    return cast(int, state.get(deck_id, {}).get("display_timeout", 0))


def set_display_timeout(deck_id: str, timeout: int) -> None:
    """ Sets the amount of time in seconds before the display gets dimmed."""
    state.setdefault(deck_id, {})["display_timeout"] = timeout
    _save_state()


def _save_state():
    export_config(STATE_FILE)


def _open_config(config_file: str):
    global state

    with open(config_file) as state_file:
        config = json.loads(state_file.read())
        file_version = config.get("streamdeck_ui_version", 0)
        if file_version != CONFIG_FILE_VERSION:
            raise ValueError(
                "Incompatible version of config file found: "
                f"{file_version} does not match required version "
                f"{CONFIG_FILE_VERSION}."
            )

        state = {}
        for deck_id, deck in config["state"].items():
            deck["buttons"] = {
                int(page_id): {int(button_id): button for button_id, button in buttons.items()}
                for page_id, buttons in deck.get("buttons", {}).items()
            }
            state[deck_id] = deck


def import_config(config_file: str) -> None:
    _open_config(config_file)
    render()
    _save_state()


def export_config(output_file: str) -> None:
    try:
        with open(output_file + ".tmp", "w") as state_file:
            state_file.write(
                json.dumps(
                    {"streamdeck_ui_version": CONFIG_FILE_VERSION, "state": state},
                    indent=4,
                    separators=(",", ": "),
                )
            )
    except Exception as error:
        print(f"The configuration file '{output_file}' was not updated. Error: {error}")
        raise
    else:
        os.replace(output_file + ".tmp", os.path.realpath(output_file))


def open_decks() -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    """Opens and then returns all known stream deck devices"""
    for deck in DeviceManager.DeviceManager().enumerate():
        deck.open()
        deck.reset()
        deck_id = deck.get_serial_number()
        decks[deck_id] = deck
        deck.set_key_callback(partial(_key_change_callback, deck_id))

    return {
        deck_id: {"type": deck.deck_type(), "layout": deck.key_layout()}
        for deck_id, deck in decks.items()
    }


def close_decks() -> None:
    """Closes open decks for input/ouput."""
    for _deck_serial, deck in decks.items():
        if deck.connected():
            deck.set_brightness(50)
            deck.reset()
            deck.close()


def ensure_decks_connected() -> None:
    """Reconnects to any decks that lost connection. If they did, re-renders them."""
    for deck_serial, deck in decks.copy().items():
        if not deck.connected():
            for new_deck in DeviceManager.DeviceManager().enumerate():
                try:
                    new_deck.open()
                    new_deck_serial = new_deck.get_serial_number()
                except Exception as error:
                    warn(f"A {error} error occurred when trying to reconnect to {deck_serial}")
                    new_deck_serial = None

                if new_deck_serial == deck_serial:
                    deck.close()
                    new_deck.reset()
                    new_deck.set_key_callback(partial(_key_change_callback, new_deck_serial))
                    decks[new_deck_serial] = new_deck
                    render()


def get_deck(deck_id: str) -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    return {"type": decks[deck_id].deck_type(), "layout": decks[deck_id].key_layout()}


def _button_state(deck_id: str, page: int, button: int) -> dict:
    buttons = state.setdefault(deck_id, {}).setdefault("buttons", {})
    buttons_state = buttons.setdefault(page, {})  # type: ignore
    return buttons_state.setdefault(button, {})  # type: ignore


def swap_buttons(deck_id: str, page: int, source_button: int, target_button: int) -> None:
    """Swaps the properties of the source and target buttons"""
    temp = cast(dict, state[deck_id]["buttons"])[page][source_button]
    cast(dict, state[deck_id]["buttons"])[page][source_button] = cast(
        dict, state[deck_id]["buttons"]
    )[page][target_button]
    cast(dict, state[deck_id]["buttons"])[page][target_button] = temp

    # Clear the cache so images will be recreated on render
    image_cache.pop(f"{deck_id}.{page}.{source_button}", None)
    image_cache.pop(f"{deck_id}.{page}.{target_button}", None)

    _save_state()
    render()


def set_button_text(deck_id: str, page: int, button: int, text: str) -> None:
    """Set the text associated with a button"""
    if get_button_text(deck_id, page, button) != text:
        _button_state(deck_id, page, button)["text"] = text
        image_cache.pop(f"{deck_id}.{page}.{button}", None)
        render()
        _save_state()


def get_button_text(deck_id: str, page: int, button: int) -> str:
    """Returns the text set for the specified button"""
    return _button_state(deck_id, page, button).get("text", "")


def set_button_icon(deck_id: str, page: int, button: int, icon: str) -> None:
    """Sets the icon associated with a button"""
    if get_button_icon(deck_id, page, button) != icon:
        _button_state(deck_id, page, button)["icon"] = icon
        image_cache.pop(f"{deck_id}.{page}.{button}", None)
        render()
        _save_state()


def get_button_icon(deck_id: str, page: int, button: int) -> str:
    """Returns the icon set for a particular button"""
    return _button_state(deck_id, page, button).get("icon", "")


def set_button_change_brightness(deck_id: str, page: int, button: int, amount: int) -> None:
    """Sets the brightness changing associated with a button"""
    if get_button_change_brightness(deck_id, page, button) != amount:
        _button_state(deck_id, page, button)["brightness_change"] = amount
        render()
        _save_state()


def get_button_change_brightness(deck_id: str, page: int, button: int) -> int:
    """Returns the brightness change set for a particular button"""
    return _button_state(deck_id, page, button).get("brightness_change", 0)


def set_button_command(deck_id: str, page: int, button: int, command: str) -> None:
    """Sets the command associated with the button"""
    if get_button_command(deck_id, page, button) != command:
        _button_state(deck_id, page, button)["command"] = command
        _save_state()


def get_button_command(deck_id: str, page: int, button: int) -> str:
    """Returns the command set for the specified button"""
    return _button_state(deck_id, page, button).get("command", "")


def set_button_switch_page(deck_id: str, page: int, button: int, switch_page: int) -> None:
    """Sets the page switch associated with the button"""
    if get_button_switch_page(deck_id, page, button) != switch_page:
        _button_state(deck_id, page, button)["switch_page"] = switch_page
        _save_state()


def get_button_switch_page(deck_id: str, page: int, button: int) -> int:
    """Returns the page switch set for the specified button. 0 implies no page switch."""
    return _button_state(deck_id, page, button).get("switch_page", 0)


def set_button_keys(deck_id: str, page: int, button: int, keys: str) -> None:
    """Sets the keys associated with the button"""
    if get_button_keys(deck_id, page, button) != keys:
        _button_state(deck_id, page, button)["keys"] = keys
        _save_state()


def get_button_keys(deck_id: str, page: int, button: int) -> str:
    """Returns the keys set for the specified button"""
    return _button_state(deck_id, page, button).get("keys", "")


def set_button_write(deck_id: str, page: int, button: int, write: str) -> None:
    """Sets the text meant to be written when button is pressed"""
    if get_button_write(deck_id, page, button) != write:
        _button_state(deck_id, page, button)["write"] = write
        _save_state()


def get_button_write(deck_id: str, page: int, button: int) -> str:
    """Returns the text to be produced when the specified button is pressed"""
    return _button_state(deck_id, page, button).get("write", "")


def set_brightness(deck_id: str, brightness: int) -> None:
    """Sets the brightness for every button on the deck"""
    if get_brightness(deck_id) != brightness:
        decks[deck_id].set_brightness(brightness)
        state.setdefault(deck_id, {})["brightness"] = brightness
        _save_state()


def get_brightness(deck_id: str) -> int:
    """Gets the brightness that is set for the specified stream deck"""
    return state.get(deck_id, {}).get("brightness", 100)  # type: ignore


def get_brightness_dimmed(deck_id: str) -> int:
    """Gets the percentage value of the full brightness that is used when dimming the specified
    stream deck"""
    return state.get(deck_id, {}).get("brightness_dimmed", 0)  # type: ignore


def set_brightness_dimmed(deck_id: str, brightness_dimmed: int) -> None:
    """Sets the percentage value that will be used for dimming the full brightness"""
    state.setdefault(deck_id, {})["brightness_dimmed"] = brightness_dimmed
    _save_state()


def change_brightness(deck_id: str, amount: int = 1) -> None:
    """Change the brightness of the deck by the specified amount"""
    set_brightness(deck_id, max(min(get_brightness(deck_id) + amount, 100), 0))


def get_page(deck_id: str) -> int:
    """Gets the current page shown on the stream deck"""
    return state.get(deck_id, {}).get("page", 0)  # type: ignore


def set_page(deck_id: str, page: int) -> None:
    """Sets the current page shown on the stream deck"""
    if get_page(deck_id) != page:
        state.setdefault(deck_id, {})["page"] = page
        render()
        _save_state()


def render() -> None:
    """renders all decks"""
    for deck_id, deck_state in state.items():
        deck = decks.get(deck_id, None)
        if not deck:
            warn(f"{deck_id} has settings specified but is not seen. Likely unplugged!")
            continue

        page = get_page(deck_id)
        for button_id, button_settings in (
            deck_state.get("buttons", {}).get(page, {}).items()  # type: ignore
        ):
            key = f"{deck_id}.{page}.{button_id}"
            if key in image_cache:
                image = image_cache[key]
            else:
                image = _render_key_image(deck, **button_settings)
                image_cache[key] = image

            with streamdecks_lock:
                deck.set_key_image(button_id, image)


def _render_key_image(deck, icon: str = "", text: str = "", font: str = DEFAULT_FONT, **kwargs):
    """Renders an individual key image"""
    image = PILHelper.create_image(deck)
    draw = ImageDraw.Draw(image)

    if icon:
        try:
            rgba_icon = Image.open(icon).convert("RGBA")
        except (OSError, IOError) as icon_error:
            print(f"Unable to load icon {icon} with error {icon_error}")
            svg_code = open(icon).read()
            png = cairosvg.svg2png(svg_code, output_height=72, output_width=72)
            image_file = BytesIO(png)
            rgba_icon = Image.open(image_file)
        except (OSError, IOError) as icon_error:
            print(f"Unable to load icon {icon} with error {icon_error}")
            rgba_icon = Image.new("RGBA", (300, 300))
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
        if icon:
            label_pos = ((image.width - label_w) // 2, image.height - 20)
        else:
            label_pos = ((image.width - label_w) // 2, (image.height // 2) - 7)
        draw.text(label_pos, text=text, font=true_font, fill="white")

    return PILHelper.to_native_format(deck, image)


if os.path.isfile(STATE_FILE):
    _open_config(STATE_FILE)
