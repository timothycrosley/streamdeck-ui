from subprocess import Popen  # nosec - Need to allow users to specify arbitrary commands

from PySide2.QtWidgets import QWidget

from streamdeck_ui.actions.brightness.ui_brightness import Ui_Brightness
from streamdeck_ui.actions.stream_deck_action import ActionSettings, StreamDeckAction


class Action(StreamDeckAction):
    def __init__(self):
        super().__init__("Change Brightness", "System", __file__)

    def get_ui(self, parent):
        return BrightnessWidget(parent, self.settings)

    def execute(self):
        brightness_change = self.settings.get_setting("brightness_change")
        if brightness_change:
            self.api.change_brightness(int(brightness_change))

    def get_summary(self) -> str:
        return str(self.settings.get_setting("brightness_change"))


class BrightnessWidget(QWidget):
    def __init__(self, parent, settings: ActionSettings):
        super().__init__(parent)
        self.ui = Ui_Brightness()
        self.ui.setupUi(self)
        brightness_change = settings.get_setting("brightness_change")
        if brightness_change:
            self.ui.dial.setValue(settings.get_setting("brightness_change"))
            self.ui.amount.setText(str(brightness_change))
        self.ui.dial.valueChanged.connect(self.value_changed)
        self.settings = settings
        self.show()

    def value_changed(self, text: int) -> None:
        self.settings.set_setting("brightness_change", text)
        self.ui.amount.setText(str(text))
