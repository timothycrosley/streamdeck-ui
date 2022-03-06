from PySide2.QtWidgets import QWidget
from streamdeck_ui.actions.command.ui_commandwidget import Ui_CommandWidget
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction
from pynput import keyboard
import time


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Press key(s)", "Keyboard", __file__)

    def get_ui(self, parent):
        return CommandWidget(parent, self.settings)

    def _replace_special_keys(self, key):
        """Replaces special keywords the user can use with their character equivalent."""
        if key.lower() == "plus":
            return "+"
        if key.lower() == "comma":
            return ","
        if key.lower().startswith("delay"):
            return key.lower()
        return key

    def execute(self):
        kb = keyboard.Controller()
        keys = self.settings.get_setting("keys")
        if keys:
            keys = keys.strip().replace(" ", "")
            for section in keys.split(","):
                # Since + and , are used to delimit our section and keys to press,
                # they need to be substituted with keywords.
                section_keys = [self._replace_special_keys(key_name) for key_name in section.split("+")]

                # Translate string to enum, or just the string itself if not found
                section_keys = [getattr(Key, key_name.lower(), key_name) for key_name in section_keys]

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
                            # default if not specified
                            sleep_time = 0.5

                        if sleep_time:
                            try:
                                time.sleep(sleep_time)
                            except Exception:
                                print(f"Could not sleep with provided sleep time '{sleep_time}'")
                    else:
                        try:
                            if isinstance(key_name, str) and key_name.lower().startswith("0x"):
                                kb.press(keyboard.KeyCode(int(key_name, 16)))
                            else:
                                kb.press(key_name)

                        except Exception:
                            print(f"Could not press key '{key_name}'")

                for key_name in section_keys:
                    if not (isinstance(key_name, str) and key_name.startswith("delay")):
                        try:
                            if isinstance(key_name, str) and key_name.lower().startswith("0x"):
                                kb.release(keyboard.KeyCode(int(key_name, 16)))
                            else:
                                kb.release(key_name)
                        except Exception:
                            print(f"Could not release key '{key_name}'")

    def get_summary(self) -> str:
        return self.settings.get_setting("keys")


class CommandWidget(QWidget):
    def __init__(self, parent, settings: ActionSettings):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.ui.command.setText(settings.get_setting("keys"))
        self.ui.command.textChanged.connect(self.text_changed)
        self.settings = settings
        self.show()

    def text_changed(self, text: str) -> None:
        self.settings.set_setting("keys", text)
