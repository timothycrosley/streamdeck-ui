from subprocess import Popen

from obswebsocket import obsws, requests
from PySide2.QtWidgets import QWidget

from streamdeck_ui.actions.obs.ui_obs import Ui_ObsWidget
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Switch Scene", "Obs", __file__)

    def get_ui(self, parent):
        return ObsWidget(parent, self.settings)

    def execute(self):
        scene = self.settings.get_setting("scene")
        if scene:
            try:
                ws = obsws("localhost", 4444, "12345")
                ws.connect()
                ws.call(requests.SetCurrentScene(scene))
                ws.disconnect()
            except Exception as error:
                print(f"Could not switch to scene '{scene}' failed: {error}")

    def get_summary(self) -> str:
        return self.settings.get_setting("scene")


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
