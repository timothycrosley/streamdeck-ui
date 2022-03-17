from pynput import keyboard
from PySide2.QtWidgets import QWidget

from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction
from streamdeck_ui.actions.text.ui_text import Ui_TextWidget


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Type text", "Keyboard", __file__)

    def get_ui(self, parent):
        return TextWidget(parent, self.settings)

    def get_summary(self) -> str:
        text = self.settings.get_setting("text")
        if text:
            return text.replace("\n", " ")
        else:
            return "<empty>"

    def execute(self):
        write = self.settings.get_setting("text")
        if write:
            kb = keyboard.Controller()
            try:
                kb.type(write)
            except Exception as error:
                print(f"Could not complete the write command: {error}")


class TextWidget(QWidget):
    def __init__(self, parent, settings: ActionSettings):
        super().__init__(parent)
        self.ui = Ui_TextWidget()
        self.ui.setupUi(self)
        self.settings = settings
        self.ui.textEdit.setPlainText(self.settings.get_setting("text"))
        self.ui.textEdit.textChanged.connect(self.text_changed)
        self.settings = settings
        self.show()

    def text_changed(self) -> None:
        self.settings.set_setting("text", self.ui.textEdit.toPlainText())
