import typing as tp

from streamdeck_ui.api import StreamDeckServer

class Command(tp.Protocol):
    def execute(self, api: StreamDeckServer, ui: tp.Any) -> None:
        ...

class PageChangeCommand:
    def __init__(self, cfg):
        self.page_index = cfg["page"]

    def execute(self, api: StreamDeckServer, ui):
        deck_id = ui.device_list.itemData(ui.device_list.currentIndex())
        if api.get_page(deck_id) == self.page_index:
            return
        api.set_page(deck_id, self.page_index)
        ui.pages.setCurrentIndex(self.page_index)


def create_command(cfg: dict) -> Command:
    if(cfg["command"] == "page_change"):
        return PageChangeCommand(cfg)
    return None