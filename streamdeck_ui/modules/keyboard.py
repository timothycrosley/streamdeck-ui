import time
from typing import List

from evdev import InputDevice, UInput
from evdev import ecodes as e
from evdev import list_devices
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QCompleter

_DEFAULT_KEY_PRESS_DELAY = 0.05
_DEFAULT_KEY_SECTION_DELAY = 0.5

# fmt: off
_SPECIAL_KEYS = {
    "plus": "+",
    "comma": ","
}
_OLD_NUMPAD_KEYS = {
    "numpad_0": e.KEY_KP0,
    "numpad_1": e.KEY_KP1,
    "numpad_2": e.KEY_KP2,
    "numpad_3": e.KEY_KP3,
    "numpad_4": e.KEY_KP4,
    "numpad_5": e.KEY_KP5,
    "numpad_6": e.KEY_KP6,
    "numpad_7": e.KEY_KP7,
    "numpad_8": e.KEY_KP8,
    "numpad_9": e.KEY_KP9,
    "numpad_enter": e.KEY_ENTER,
    "numpad_decimal": e.KEY_KPDOT,
    "numpad_divide": e.KEY_KPSLASH,
    "numpad_multiply": e.KEY_KPASTERISK,
    "numpad_subtract": e.KEY_KPMINUS,
    "numpad_add": e.KEY_KPPLUS,
}
_OLD_PYNPUT_KEYS = {
    "media_volume_mute": e.KEY_MUTE,
    "media_volume_down": e.KEY_VOLUMEDOWN,
    "media_volume_up": e.KEY_VOLUMEUP,
    "media_play_pause": e.KEY_PLAYPAUSE,
    "media_previous_track": e.KEY_PREVIOUSSONG,
    "media_previous": e.KEY_PREVIOUSSONG,
    "media_next_track": e.KEY_NEXTSONG,
    "media_next": e.KEY_NEXTSONG,
    "media_stop": e.KEY_STOPCD,
    "num_lock": e.KEY_NUMLOCK,
    "caps_lock": e.KEY_CAPSLOCK,
    "scroll_lock": e.KEY_SCROLLLOCK,
}
_MODIFIER_KEYS = {
    "ctrl": e.KEY_LEFTCTRL,
    "alt": e.KEY_LEFTALT,
    "alt_gr": e.KEY_RIGHTALT,
    "shift": e.KEY_LEFTSHIFT,
    "meta": e.KEY_LEFTMETA,
    "super": e.KEY_LEFTMETA,
    "win": e.KEY_LEFTMETA,
}

_BAD_ECODES = ['KEY_MAX', 'KEY_CNT']
_KEY_MAPPING = {
    'a': e.KEY_A,
    'b': e.KEY_B,
    'c': e.KEY_C,
    'd': e.KEY_D,
    'e': e.KEY_E,
    'f': e.KEY_F,
    'g': e.KEY_G,
    'h': e.KEY_H,
    'i': e.KEY_I,
    'j': e.KEY_J,
    'k': e.KEY_K,
    'l': e.KEY_L,
    'm': e.KEY_M,
    'n': e.KEY_N,
    'o': e.KEY_O,
    'p': e.KEY_P,
    'q': e.KEY_Q,
    'r': e.KEY_R,
    's': e.KEY_S,
    't': e.KEY_T,
    'u': e.KEY_U,
    'v': e.KEY_V,
    'w': e.KEY_W,
    'x': e.KEY_X,
    'y': e.KEY_Y,
    'z': e.KEY_Z,
    'A': e.KEY_A,
    'B': e.KEY_B,
    'C': e.KEY_C,
    'D': e.KEY_D,
    'E': e.KEY_E,
    'F': e.KEY_F,
    'G': e.KEY_G,
    'H': e.KEY_H,
    'I': e.KEY_I,
    'J': e.KEY_J,
    'K': e.KEY_K,
    'L': e.KEY_L,
    'M': e.KEY_M,
    'N': e.KEY_N,
    'O': e.KEY_O,
    'P': e.KEY_P,
    'Q': e.KEY_Q,
    'R': e.KEY_R,
    'S': e.KEY_S,
    'T': e.KEY_T,
    'U': e.KEY_U,
    'V': e.KEY_V,
    'W': e.KEY_W,
    'X': e.KEY_X,
    'Y': e.KEY_Y,
    'Z': e.KEY_Z,
    '1': e.KEY_1,
    '2': e.KEY_2,
    '3': e.KEY_3,
    '4': e.KEY_4,
    '5': e.KEY_5,
    '6': e.KEY_6,
    '7': e.KEY_7,
    '8': e.KEY_8,
    '9': e.KEY_9,
    '0': e.KEY_0,
    '-': e.KEY_MINUS,
    '=': e.KEY_EQUAL,
    '[': e.KEY_LEFTBRACE,
    ']': e.KEY_RIGHTBRACE,
    '\\': e.KEY_BACKSLASH,
    ';': e.KEY_SEMICOLON,
    "'": e.KEY_APOSTROPHE,
    ',': e.KEY_COMMA,
    '.': e.KEY_DOT,
    '/': e.KEY_SLASH,
    ' ': e.KEY_SPACE,
    '\n': e.KEY_ENTER,
    '\t': e.KEY_TAB,
    '`': e.KEY_GRAVE,
    '!': e.KEY_1,
    '@': e.KEY_2,
    '#': e.KEY_3,
    '$': e.KEY_4,
    '%': e.KEY_5,
    '^': e.KEY_6,
    '&': e.KEY_7,
    '*': e.KEY_8,
    '(': e.KEY_9,
    ')': e.KEY_0,
    '_': e.KEY_MINUS,
    '+': e.KEY_EQUAL,
    '{': e.KEY_LEFTBRACE,
    '}': e.KEY_RIGHTBRACE,
    '|': e.KEY_BACKSLASH,
    ':': e.KEY_SEMICOLON,
    '"': e.KEY_APOSTROPHE,
    '<': e.KEY_COMMA,
    '>': e.KEY_DOT,
    '?': e.KEY_SLASH,
    '~': e.KEY_GRAVE,
}
_SHIFT_KEY_MAPPING = {
    '!': e.KEY_1,
    '@': e.KEY_2,
    '#': e.KEY_3,
    '$': e.KEY_4,
    '%': e.KEY_5,
    '^': e.KEY_6,
    '&': e.KEY_7,
    '*': e.KEY_8,
    '(': e.KEY_9,
    ')': e.KEY_0,
    '_': e.KEY_MINUS,
    '+': e.KEY_EQUAL,
    '{': e.KEY_LEFTBRACE,
    '}': e.KEY_RIGHTBRACE,
    '|': e.KEY_BACKSLASH,
    ':': e.KEY_SEMICOLON,
    '"': e.KEY_APOSTROPHE,
    '<': e.KEY_COMMA,
    '>': e.KEY_DOT,
    '?': e.KEY_SLASH,
    '~': e.KEY_GRAVE,
    'A': e.KEY_A,
    'B': e.KEY_B,
    'C': e.KEY_C,
    'D': e.KEY_D,
    'E': e.KEY_E,
    'F': e.KEY_F,
    'G': e.KEY_G,
    'H': e.KEY_H,
    'I': e.KEY_I,
    'J': e.KEY_J,
    'K': e.KEY_K,
    'L': e.KEY_L,
    'M': e.KEY_M,
    'N': e.KEY_N,
    'O': e.KEY_O,
    'P': e.KEY_P,
    'Q': e.KEY_Q,
    'R': e.KEY_R,
    'S': e.KEY_S,
    'T': e.KEY_T,
    'U': e.KEY_U,
    'V': e.KEY_V,
    'W': e.KEY_W,
    'X': e.KEY_X,
    'Y': e.KEY_Y,
    'Z': e.KEY_Z,
}
# we remove KEY_ from the key names to make it easier to type
_SUPPORTED_KEYS = [key.replace("KEY_", "").lower() for key in dir(e) if key.startswith("KEY_") and key not in _BAD_ECODES]
# fmt: on


def _initialize_uinput():
    return UInput({e.EV_KEY: _SUPPORTED_KEYS})


def parse_keys_as_keycodes(keys: str) -> List[List[str]]:
    stripped = keys.strip().replace(" ", "").lower()
    if not stripped:
        return []
    # split by , for sections
    sections = stripped.split(",")
    parsed_keys = []
    for section in sections:
        # split by + for individual keys
        individual = section.split("+")
        # filter empty strings
        individual = list(filter(None, individual))
        # replace any string with e.KEY_<string>
        individual = [getattr(e, f"KEY_{key.upper()}", key) for key in individual]
        # replace special keys
        individual = [_SPECIAL_KEYS.get(key, key) for key in individual]
        # replace old numpad keys
        individual = [_OLD_NUMPAD_KEYS.get(key, key) for key in individual]
        # replace old media keys
        individual = [_OLD_PYNPUT_KEYS.get(key, key) for key in individual]
        # replace modifier keys
        individual = [_MODIFIER_KEYS.get(key, key) for key in individual]
        # replace key names with key codes
        individual = [_KEY_MAPPING.get(key, key) for key in individual]

        # if any value is not an int, raise an error
        if not all(isinstance(key, int) for key in individual):
            invalid_keys = [key for key in individual if not isinstance(key, int)]
            raise ValueError(f"Invalid keys: {invalid_keys}")

        if len(individual) > 0:
            parsed_keys.append(individual)

    return parsed_keys


def keyboard_write(string: str):
    _ui = _initialize_uinput()
    caps_lock_is_on = check_caps_lock()
    for char in string:
        if char in _KEY_MAPPING:
            keycode = _KEY_MAPPING[char]
            need_shift = False

            if char in _SHIFT_KEY_MAPPING:
                need_shift = True

            if char.isalpha() and caps_lock_is_on:
                need_shift = not need_shift

            if need_shift:
                _ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)

            _ui.write(e.EV_KEY, keycode, 1)
            _ui.syn()
            _ui.write(e.EV_KEY, keycode, 0)
            _ui.syn()

            if need_shift:
                _ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
                _ui.syn()

            time.sleep(_DEFAULT_KEY_PRESS_DELAY)
        else:
            print(f"Unsupported character: {char}")


def keyboard_press_keys(keys: str):
    _ui = _initialize_uinput()
    sections = parse_keys_as_keycodes(keys)
    for section_of_keycodes in sections:
        for keycode in section_of_keycodes:
            _ui.write(e.EV_KEY, keycode, 1)
            _ui.syn()

        time.sleep(_DEFAULT_KEY_PRESS_DELAY)

        for keycode in reversed(section_of_keycodes):
            _ui.write(e.EV_KEY, keycode, 0)
            _ui.syn()

        # add some delay between sections, only if there are more than one
        if len(section_of_keycodes) > 1:
            time.sleep(_DEFAULT_KEY_SECTION_DELAY)


def get_valid_key_names() -> List[str]:
    """Returns a list of valid key names."""
    key_names = [key for key in _SUPPORTED_KEYS]
    key_names.extend(_SPECIAL_KEYS.keys())
    key_names.extend(_OLD_NUMPAD_KEYS.keys())
    key_names.extend(_OLD_PYNPUT_KEYS.keys())
    key_names.extend(_MODIFIER_KEYS.keys())
    return sorted(key_names)


def check_caps_lock() -> bool:
    """Returns True if Caps Lock is on, False if it is off, and False if it cannot be determined."""
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.capabilities().get(e.EV_LED):
            return e.LED_CAPSL in device.leds()
    return False


class KeyPressAutoComplete(QCompleter):
    special_keys = _SPECIAL_KEYS.values()
    allowed_keys = get_valid_key_names()

    def __init__(self, parent=None):
        super(KeyPressAutoComplete, self).__init__(parent)
        model = QStringListModel()
        model.setStringList(self.allowed_keys)
        self.setModel(model)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

    def update_prefix(self, text: str):
        """Update the prefix for the autocompletion."""
        # space " " is considered a special key in case user types, for example, "ctrl + "
        # we still can autocomplete after the space
        last_special_index = max(text.rfind(","), text.rfind("+"), text.rfind(" "))
        # if there is a special key, update model to allow autocomplete for further keys
        if last_special_index != -1:
            prefix = text[: last_special_index + 1]
            allowed_keys = [prefix + key for key in self.allowed_keys]
            self.model().setStringList(allowed_keys)  # type: ignore [attr-defined]
        # otherwise, reset model to allow autocomplete for all keys
        else:
            self.model().setStringList(self.allowed_keys)  # type: ignore [attr-defined]
        self.complete()
