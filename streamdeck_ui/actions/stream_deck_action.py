from abc import ABC, abstractmethod
from PySide2.QtGui import QIcon
import os


class StreamDeckAction(ABC):
    def __init__(self, name, category, file_path):
        self.name = name
        self.category = category
        self.file_path = file_path

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_icon(self) -> QIcon:
        path = os.path.dirname(os.path.abspath(self.file_path))
        return QIcon(os.path.join(path, "icon.png"))

    @abstractmethod
    def get_ui(self, parent, settings):
        pass
