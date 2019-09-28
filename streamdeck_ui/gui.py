import os
import sys

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from streamdeck_ui import api

STREAMDECK_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.ui")


def start():
    app = QApplication(sys.argv)

    window = QUiLoader().load(STREAMDECK_TEMPLATE)
    window.show()

    for deck_id, deck_type in api.decks().items():
        window.device_list.addItem(f"{deck_type} - {deck_id}", userData=deck_id)

    return app.exec_()


if __name__ == "__main__":
    sys.exit(start())
