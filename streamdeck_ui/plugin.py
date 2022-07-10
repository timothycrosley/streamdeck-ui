import json

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.ui_main import Ui_MainWindow
import streamdeck_ui.gui as gui

class PluginManager:
    def __init__(self, api: StreamDeckServer, ui: Ui_MainWindow):
        self.api = api
        self.ui = ui

    def get_plugin_data(self, command_stdout: str, button: int) -> None:
        try:
            json_data = json.loads(command_stdout)
        except:
            return # Not JSON -> probably not a plugin
        if not self.validate_data(json_data):
            return # JSON doesn't have "streamdeck-plugin" key -> probably not a plugin
        try:
            self.parse_function(json_data, button)
        except:
            print("This plugin's format is incorrect...")

    def validate_data(self, json_data: dict) -> bool:
        return "streamdeck-plugin" in json_data

    def parse_function(self, json_data: dict, button: int) -> None:
        for task in json_data["streamdeck-plugin"]["tasks"]:
            plugin_function = task["function"]
            plugin_data = task["data"]

            deck_id = gui._deck_id(self.ui)
            page = gui._page(self.ui)
            if plugin_function == "set_button_icon":
                self.api.set_button_icon(deck_id, page, button, plugin_data)
            elif plugin_function == "set_button_text":
                self.api.set_button_text(deck_id, page, button, plugin_data)
            elif plugin_function == "set_button_command":
                self.api.set_button_command(deck_id, page, button, plugin_data)

            gui.redraw_buttons(self.ui)
