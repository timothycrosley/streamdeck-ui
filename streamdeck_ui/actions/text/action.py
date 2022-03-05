from PySide2.QtWidgets import QWidget
from streamdeck_ui.actions.text.ui_text import Ui_TextWidget
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Type text", "Keyboard", __file__)

    def get_ui(self, parent):
        return TextWidget(parent, self.settings)

    def get_summary(self) -> str:
        return self.settings.get_setting("text")

    def execute(self):
        pass


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

    def text_changed(self, text: str) -> None:
        self.settings.set_setting("text", self.ui.textEdit.toPlainText())
