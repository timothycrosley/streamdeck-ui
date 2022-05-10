import os
from abc import ABC, abstractmethod
from typing import Any, Callable

from PySide2.QtGui import QIcon


class StreamDeckAPI(ABC):
    """An API provided to StreamDeckAction instances that allow them to interact with
    the Stream Deck.
    """

    @abstractmethod
    def change_brightness(self, amount: int) -> None:
        """Changes the brightness of the Stream Deck by the given amount.

        :param amount: The amount the change the brightness by. Positive values make the buttons
        appear brighter, negative values darker.
        :type amount: int
        """
        pass

    @abstractmethod
    def set_page(self, page: int) -> None:
        """Sets the current page shown on the Stream Deck.

        :param page: The page number to change to.
        :type page: int
        """


class ActionSettings:
    def __init__(self, get_setting: Callable[[str], Any], set_setting: Callable[[str], Any]):
        self.get_setting = get_setting
        self.set_setting = set_setting


class StreamDeckAction(ABC):
    def __init__(self, name: str, category: str, file_path: str):
        self.name = name
        self.category = category
        self.file_path = file_path

    def initialize(self, settings: ActionSettings, api: StreamDeckAPI):
        self.settings = settings
        self.api = api

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_icon(self) -> QIcon:
        path = os.path.dirname(os.path.abspath(self.file_path))
        return QIcon(os.path.join(path, "icon.png"))

    def id(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    @abstractmethod
    def get_ui(self, parent):
        pass

    @abstractmethod
    def get_summary(self) -> str:
        """Returns a text summary of this action. This will be displayed to the user in a list
        of various actions. Will typically include configuration or other key behaviour.
        """
        pass

    # REVIEW: What would be a good way to allow for execution flow control?
    # It could return True or False. False stops futher execution, true lets it continue
    # It could return a numeric result.
    # It could return return an arbitrary result and we pass it on the the next
    # execute.
    # We could have a "conditional" action - all it does, is decides what to do next
    @abstractmethod
    def execute(self):
        pass
