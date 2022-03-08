from subprocess import Popen
from PySide2.QtWidgets import QWidget
from streamdeck_ui.actions.obs.obs import Ui_ObsWidget
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction
import shlex


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Switch Scene", "Obs", __file__)

    def get_ui(self, parent):
        return ObsWidget(parent, self.settings)

    def execute(self):
        command = self.settings.get_setting("scene")
        if command:
            try:
                pass
            except Exception as error:
                print(f"The command '{command}' failed: {error}")

    def get_summary(self) -> str:
        return self.settings.get_setting("command")


class ObsWidget(QWidget):
    def __init__(self, parent, settings: ActionSettings):
        super().__init__(parent)
        self.ui = Ui_ObsWidget()
        self.ui.setupUi(self)
        self.ui.scene.setText(settings.get_setting("scene"))
        self.ui.scene.textChanged.connect(self.text_changed)
        self.settings = settings
        self.show()

    def text_changed(self, text: str) -> None:
        self.settings.set_setting("scene", text)
