from PySide2.QtWidgets import QWidget
from streamdeck_ui.actions.command.ui_commandwidget import Ui_CommandWidget
from streamdeck_ui.actions.stream_deck_action import StreamDeckAction


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Run_command", "Keyboard", __file__)

    def get_ui(self, parent, settings):
        return CommandWidget(parent, settings)


class CommandWidget(QWidget):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.ui.command.setText(settings.get("command"))
        self.ui.command.textChanged.connect(self.text_changed)
        self.settings = settings
        self.show()

    def text_changed(self, text: str) -> None:
        self.settings.set("command", text)
