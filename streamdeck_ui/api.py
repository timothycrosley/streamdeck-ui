"""Defines the Python API for interacting with the StreamDeck Configuration UI"""
import itertools
import json
import os
import threading
import time
from functools import partial
from typing import Dict, Tuple, Union, cast
from warnings import warn

from fractions import Fraction
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from PySide2.QtCore import QObject, Signal
from StreamDeck import DeviceManager
from StreamDeck.Devices import StreamDeck
from StreamDeck.ImageHelpers import PILHelper
from StreamDeck.Transport.Transport import TransportError

from streamdeck_ui.config import CONFIG_FILE_VERSION, DEFAULT_FONT, FONTS_PATH, STATE_FILE, ICON_DIR

image_cache: Dict[str, memoryview] = {}
decks: Dict[str, StreamDeck.StreamDeck] = {}
state: Dict[str, Dict[str, Union[int, Dict[int, Dict[int, Dict[str, str]]]]]] = {}
streamdecks_lock = threading.Lock()
key_event_lock = threading.Lock()
animation_buttons = dict()


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


def export_icon(deck_id: str, page: int, button_id: int, icon_frames_to_save: list) -> None:
    """export rendered icon"""
    if not os.path.isdir(ICON_DIR):
        os.mkdir(ICON_DIR)
    key = f"{deck_id}.{page}.{button_id}"
    try:
        gif = icon_frames_to_save
        if gif.__len__() > 1:
            gif[0].save(
                ICON_DIR + key + ".gif",
                save_all=True,
                append_images=gif[1:],
                optimize=False,
                loop=0,
                duration=40  # 40ms (25 fps)
            )
        else:
            gif[0].save(ICON_DIR + key + ".gif")
    except Exception as error:
        print(f"The icon file '{key}'.gif was not updated. Error: {error}")
        raise


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
    os.remove(ICON_DIR + f"{deck_id}.{page}.{source_button}" + ".gif")
    os.remove(ICON_DIR + f"{deck_id}.{page}.{target_button}" + ".gif")

    _save_state()
    render()


def set_button_text(deck_id: str, page: int, button: int, text: str) -> None:
    """Set the text associated with a button"""
    if get_button_text(deck_id, page, button) != text:
        _button_state(deck_id, page, button)["text"] = text
        image_cache.pop(f"{deck_id}.{page}.{button}", None)
        os.remove(ICON_DIR + f"{deck_id}.{page}.{button}" + ".gif")
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
        os.remove(ICON_DIR + f"{deck_id}.{page}.{button}" + ".gif")
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


def change_brightness(deck_id: str, amount: int = 1) -> None:
    """Change the brightness of the deck by the specified amount"""
    set_brightness(deck_id, max(min(get_brightness(deck_id) + amount, 100), 0))


def get_page(deck_id: str) -> int:
    """Gets the current page shown on the stream deck"""
    return state.get(deck_id, {}).get("page", 0)  # type: ignore


def set_page(deck_id: str, page: int) -> None:
    """Sets the current page shown on the stream deck"""
    if get_page(deck_id) != page:
        stop_animation()
        state.setdefault(deck_id, {})["page"] = page
        render()
        _save_state()
        start_animation()


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
            key_image = False
            if key in image_cache:
                image = image_cache[key]
            elif os.path.isfile(ICON_DIR + key + ".gif"):
                image = _load_key_image(deck, key)
                key_image = True
            else:
                image = _render_key_image(deck, key, **button_settings)
                key_image = True

            if key_image:
                image_cache[key] = image[0]

                global animation_buttons
                if deck_id not in animation_buttons: animation_buttons[deck_id] = {}
                if page not in animation_buttons[deck_id]: animation_buttons[deck_id][page] = {}
                animation_buttons[deck_id][page][button_id] = itertools.cycle(image)

                image = image_cache[key]

            with streamdecks_lock:
                deck.set_key_image(button_id, image)


def _load_key_image(deck, key: str):
    """load an individual rendered key image"""
    if os.path.isfile(ICON_DIR + key + ".gif"):
        try:
            rgba_icon = Image.open(ICON_DIR + key + ".gif")
        except (OSError, IOError) as icon_error:
            print(f"Unable to load icon {key}.gif with error {icon_error}")
            rgba_icon = Image.new("RGBA", (300, 300))
    else:
        rgba_icon = Image.new("RGBA", (300, 300))

    icon_frames = list()
    frame_durations = list()
    frame_timestamp = [0]

    rgba_icon.seek(0)
    frames_n = 1
    while True:
        try:
            frame_durations.append(rgba_icon.info['duration'])
            frame_timestamp.append(frame_timestamp[-1]+rgba_icon.info['duration'])
            rgba_icon.seek(rgba_icon.tell() + 1)
            frames_n += 1
        except EOFError:  # end of gif
            break
        except KeyError:  # no gif
            break
    frames = ImageSequence.Iterator(rgba_icon)
    del frame_timestamp[0]

    frame_ms = 0
    for frame_index in range(frames_n):
        if bool(frame_timestamp) and frame_ms > frame_timestamp[frame_index]:
            continue
        frame = frames[frame_index].convert("RGBA")
        frame_image = PILHelper.create_image(deck)
        icon_width, icon_height = frame_image.width, frame_image.height

        frame.thumbnail((icon_width, icon_height), Image.LANCZOS)
        icon_pos = ((frame_image.width - frame.width) // 2, 0)
        frame_image.paste(frame, icon_pos, frame)

        native_frame_image = PILHelper.to_native_format(deck, frame_image)

        if bool(frame_timestamp):
            while frame_ms < frame_timestamp[frame_index]:
                frame_ms += 40  # 40ms/frame (25 fps)
                icon_frames.append(native_frame_image)
        else:
            icon_frames.append(native_frame_image)

    return icon_frames


def _render_key_image(deck, key: str, icon: str = "", text: str = "", font: str = DEFAULT_FONT, **kwargs):
    """Renders an individual key image"""

    if icon:
        try:
            rgba_icon = Image.open(icon)
        except (OSError, IOError) as icon_error:
            print(f"Unable to load icon {icon} with error {icon_error}")
            rgba_icon = Image.new("RGBA", (300, 300))
    else:
        rgba_icon = Image.new("RGBA", (300, 300))

    icon_frames = list()
    icon_frames_to_save = list()
    frame_durations = list()
    frame_timestamp = [0]

    rgba_icon.seek(0)
    frames_n = 1
    while True:
        try:
            frame_durations.append(rgba_icon.info['duration'])
            frame_timestamp.append(frame_timestamp[-1]+rgba_icon.info['duration'])
            rgba_icon.seek(rgba_icon.tell() + 1)
            frames_n += 1
        except EOFError:  # end of gif
            break
        except KeyError:  # no gif
            break
    frames = ImageSequence.Iterator(rgba_icon)
    del frame_timestamp[0]

    frame_ms = 0
    for frame_index in range(frames_n):
        if bool(frame_timestamp) and frame_ms > frame_timestamp[frame_index]:
            continue
        frame = frames[frame_index].convert("RGBA")
        frame_image = PILHelper.create_image(deck)
        draw = ImageDraw.Draw(frame_image)
        icon_width, icon_height = frame_image.width, frame_image.height
        if text:
            icon_height -= 20

        frame.thumbnail((icon_width, icon_height), Image.LANCZOS)
        icon_pos = ((frame_image.width - frame.width) // 2, 0)
        frame_image.paste(frame, icon_pos, frame)

        if text:
            true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)
            label_w, label_h = draw.textsize(text, font=true_font)
            if icon:
                label_pos = ((frame_image.width - label_w) // 2, frame_image.height - 20)
            else:
                label_pos = ((frame_image.width - label_w) // 2, (frame_image.height // 2) - 7)
            draw.text(label_pos, text=text, font=true_font, fill="white")

        native_frame_image = PILHelper.to_native_format(deck, frame_image)

        if bool(frame_timestamp):
            while frame_ms < frame_timestamp[frame_index]:
                frame_ms += 40  # 40ms/frame (25 fps)
                icon_frames.append(native_frame_image)
                icon_frames_to_save.append(frame_image)
        else:
            icon_frames.append(native_frame_image)
            icon_frames_to_save.append(frame_image)

    deck_id, page, button_id = key.split(".")
    export_icon(deck_id, page, button_id, icon_frames_to_save)

    return icon_frames


def start_animation() -> None:
    global animation
    animation = threading.Thread(target=animate)
    animation.start()
    stop_event.clear()


def stop_animation() -> None:
    stop_event.set()
    animation.join()


def animate() -> None:
    frame_time = Fraction(1, 25)
    next_frame = Fraction(time.monotonic())

    # while not stop_event.is_set():
    while True:
        for deck_id, deck_state in state.items():
            deck = decks.get(deck_id, None)
            page = get_page(deck_id)
            if not deck:
                warn(f"{deck_id} has settings specified but is not seen. Likely unplugged!")
                continue

            try:
                with deck:
                    for key, frames in animation_buttons[deck_id][page].items():
                        deck.set_key_image(key, next(frames))
            except TransportError as err:
                print("TransportError: {0}".format(err))
                break

            if stop_event.is_set():
                return

            next_frame += frame_time

            sleep_interval = float(next_frame) - time.monotonic()

            if sleep_interval >= 0:
                time.sleep(sleep_interval)


animation = threading.Thread(target=animate)
stop_event = threading.Event()


if os.path.isfile(STATE_FILE):
    _open_config(STATE_FILE)
