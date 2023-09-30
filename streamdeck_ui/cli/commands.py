import typing as tp

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.ui_main import Ui_MainWindow


class Command(tp.Protocol):
    def execute(self, api: StreamDeckServer, ui: tp.Any) -> None:
        ...


class SetPageCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if api.get_page(deck_id) == self.page_index:
            return
        api.set_page(deck_id, self.page_index)
        ui.pages.setCurrentIndex(self.page_index)


class SetButtonStateCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_state_index = cfg["state"]

    def execute(self, api: StreamDeckServer, ui: Ui_MainWindow):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        page_id = api.get_page(deck_id) if self.page_index is None else self.page_index
        if api.get_button_state(deck_id, page_id, self.button_index) == self.button_state_index:
            return
        api.set_button_state(deck_id, page_id, self.button_index, self.button_state_index)
        ui.button_states.setCurrentIndex(self.button_state_index)
        ui.redraw_button(self.button_index)  # type: ignore [attr-defined]


class SetBrightnessCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.brightness = cfg["value"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        api.set_brightness(deck_id, self.brightness)


class SetButtonTextCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_text = cfg["text"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_text(deck_id, self.page_index, self.button_index, self.button_text)


class SetButtonTextAlignmentCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_text_alignment = cfg["alignment"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_text_vertical_align(deck_id, self.page_index, self.button_index, self.button_text_alignment)


class SetButtonWriteCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_write = cfg["write"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_write(deck_id, self.page_index, self.button_index, self.button_write)


class SetButtonCmdCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_cmd = cfg["button_cmd"]

    def execute(self, api: StreamDeckServer, ui):
        print(self.button_cmd)
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_command(deck_id, self.page_index, self.button_index, self.button_cmd)


class SetButtonKeysCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.button_keys = cfg["button_keys"]

    def execute(self, api: StreamDeckServer, ui):
        print(self.button_keys)
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_keys(deck_id, self.page_index, self.button_index, self.button_keys)


class SetButtonIconCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]
        self.icon_path = cfg["icon"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_icon(deck_id, self.page_index, self.button_index, self.icon_path)


class ClearButtonIconCommand:
    def __init__(self, cfg):
        self.deck_index = cfg["deck"]
        self.page_index = cfg["page"]
        self.button_index = cfg["button"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex()) if self.deck_index is None else self.deck_index
        if self.page_index is None:
            self.page_index = api.get_page(deck_id)
        api.set_button_icon(deck_id, self.page_index, self.button_index, "")


def create_command(cfg: dict) -> Command | None:
    if cfg["command"] == "set_page":
        return SetPageCommand(cfg)
    elif cfg["command"] == "set_brightness":
        return SetBrightnessCommand(cfg)
    elif cfg["command"] == "set_text":
        return SetButtonTextCommand(cfg)
    elif cfg["command"] == "set_alignment":
        return SetButtonTextAlignmentCommand(cfg)
    elif cfg["command"] == "set_write":
        return SetButtonWriteCommand(cfg)
    elif cfg["command"] == "set_cmd":
        return SetButtonCmdCommand(cfg)
    elif cfg["command"] == "set_keys":
        return SetButtonKeysCommand(cfg)
    elif cfg["command"] == "set_icon":
        return SetButtonIconCommand(cfg)
    elif cfg["command"] == "clear_icon":
        return ClearButtonIconCommand(cfg)
    elif cfg["command"] == "set_state":
        return SetButtonStateCommand(cfg)
    return None
