from abc import ABC, abstractmethod
from PySide2.QtGui import QIcon
from typing import Callable, Any
import os


class ActionSettings:
    def __init__(self, get_setting: Callable[[str], Any], set_setting: Callable[[str], Any]):
        self.get_setting = get_setting
        self.set_setting = set_setting


class StreamDeckAction(ABC):
    def __init__(self, name: str, category: str, file_path: str):
        self.name = name
        self.category = category
        self.file_path = file_path

    def initialize(self, settings : ActionSettings):
        self.settings = settings

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
