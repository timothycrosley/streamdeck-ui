import time

pynput_supported: bool = True

try:
    from pynput.keyboard import Controller, Key, KeyCode
except ImportError as pynput_error:
    # the following are dummy classes to allow the program to run without pynput
    class Controller:  # type: ignore[no-redef]
        pass

    class Key:  # type: ignore[no-redef]
        enter = None
        tab = None

    class KeyCode(int):  # type: ignore[no-redef]
        pass

    pynput_supported = False
    print("---------------")
    print("*** Warning ***")
    print("---------------")
    print("Virtual keyboard functionality has been disabled.")
    print("You can still run Stream Deck UI, however you will not be able to emulate key presses or text typing.")
    print("The most likely reason you are seeing this message is because you don't have an X server running")
    print("and your operating system uses Wayland.")
    print("")
    print(f"For troubleshooting purposes, the actual error is: \n{pynput_error}")


class Keyboard:
    pynput_supported: bool
    keyboard: Controller

    # fmt: off
    _CONTROL_CODES = {
        '\n': Key.enter,
        '\r': Key.enter,
        '\t': Key.tab
    }

    _SPECIAL_COMMANDS = {
        'plus': '+',
        'comma': ','
    }
    _NUMPAD_CODES = {
        'numpad_0': int(0xFFB0),
        'numpad_1': int(0xFFB1),
        'numpad_2': int(0xFFB2),
        'numpad_3': int(0xFFB3),
        'numpad_4': int(0xFFB4),
        'numpad_5': int(0xFFB5),
        'numpad_6': int(0xFFB6),
        'numpad_7': int(0xFFB7),
        'numpad_8': int(0xFFB8),
        'numpad_9': int(0xFFB9),
        'numpad_enter': int(0xFF8D),
        'numpad_decimal': int(0xFFAE),
        'numpad_divide': int(0xFFAF),
        'numpad_multiply': int(0xFFAA),
        'numpad_subtract': int(0xFFAD),
        'numpad_add': int(0xFFAB),
        'numpad_equal': int(0xFFBD),
    }
    # fmt: on

    _DEFAULT_WRITE_DELAY = 0.015
    _DEFAULT_KEY_DELAY = 0.5

    def __init__(self, controller=None):
        self.keyboard = controller if controller else Controller()
        self.pynput_supported = pynput_supported

    def _replace_special_keys(self, key):
        """Replaces special keywords the user can use with their character equivalent."""
        if key in self._SPECIAL_COMMANDS:
            return self._SPECIAL_COMMANDS[key]
        if key in self._NUMPAD_CODES:
            return f"0x{self._NUMPAD_CODES[key]:02x}"
        if key.startswith("delay"):
            return key
        return key

    def write(self, string: str):
        """Types a string.

        This method will send all key presses and releases necessary to type
        all characters in the string.

        :param str string: The string to type.

        :raises InvalidCharacterException: if a non-typable character is encountered
        """
        if not self.pynput_supported:
            raise Exception("Virtual keyboard functionality is not supported on this system.")

        for i, character in enumerate(string):
            key = self._CONTROL_CODES.get(character, character)
            try:
                self.keyboard.press(key)
                self.keyboard.release(key)
                time.sleep(self._DEFAULT_WRITE_DELAY)

            except (ValueError, Controller.InvalidKeyException):
                raise Controller.InvalidCharacterException(i, character)

    def keys(self, string: str):
        """
        Presses and releases a series of keys.

        This method will send all key presses and releases necessary to type
        a combination of keys. including modifiers.
        """
        if not self.pynput_supported:
            raise Exception("Virtual keyboard functionality is not supported on this system.")

        sections = string.strip().replace(" ", "").lower().split(",")

        for section in sections:
            # Since + and , are used to delimit our section and keys to press,
            # they need to be substituted with keywords.
            section_keys = [self._replace_special_keys(key_name) for key_name in section.split("+")]

            # Translate string to enum, or just the string itself if not found
            section_keys = [getattr(Key, key_name, key_name) for key_name in section_keys]

            for key_name in section_keys:
                if isinstance(key_name, str) and key_name.startswith("delay"):
                    sleep_time_arg = key_name.split("delay", 1)[1]
                    if sleep_time_arg:
                        try:
                            sleep_time = float(sleep_time_arg)
                        except Exception:
                            print(f"Could not convert sleep time to float '{sleep_time_arg}'")
                            sleep_time = 0
                    else:
                        sleep_time = self._DEFAULT_KEY_DELAY

                    if sleep_time:
                        try:
                            time.sleep(sleep_time)
                        except Exception:
                            print(f"Could not sleep with provided sleep time '{sleep_time}'")
                else:
                    try:
                        if isinstance(key_name, str) and key_name.startswith("0x"):
                            self.keyboard.press(KeyCode(int(key_name, 16)))
                        else:
                            self.keyboard.press(key_name)

                    except Exception:
                        print(f"Could not press key '{key_name}'")

            for key_name in section_keys:
                if not (isinstance(key_name, str) and key_name.startswith("delay")):
                    try:
                        if isinstance(key_name, str) and key_name.startswith("0x"):
                            self.keyboard.release(KeyCode(int(key_name, 16)))
                        else:
                            self.keyboard.release(key_name)
                    except Exception:
                        print(f"Could not release key '{key_name}'")
