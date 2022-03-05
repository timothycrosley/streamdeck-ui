from abc import ABC, abstractmethod
from PySide2.QtGui import QIcon
from typing import Callable
import os


class ActionSettings:
    def __init__(self, get_setting: Callable[[str], any], set_setting: Callable[[str], any]):
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

    @abstractmethod
    def execute(self):
        pass
