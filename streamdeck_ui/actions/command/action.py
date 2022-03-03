from PySide2.QtWidgets import QWidget
from streamdeck_ui.actions.command.ui_commandwidget import Ui_CommandWidget
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Run Command", "System", __file__)

    def get_ui(self, parent):
        return CommandWidget(parent, self.settings)

    def execute(self):
        pass


class CommandWidget(QWidget):
    def __init__(self, parent, settings: ActionSettings):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.ui.command.setText(settings.get_setting("command"))
        self.ui.command.textChanged.connect(self.text_changed)
        self.settings = settings
        self.show()

    def text_changed(self, text: str) -> None:
        self.settings.set_setting("command", text)
