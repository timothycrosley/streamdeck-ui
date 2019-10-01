import os
import sys

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QSizePolicy

from streamdeck_ui import api

STREAMDECK_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.ui")


selected_button = None


def button_clicked(clicked_button, buttons):
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)


def start():
    app = QApplication(sys.argv)

    window = QUiLoader().load(STREAMDECK_TEMPLATE)
    window.show()

    for deck_id, deck in api.decks().items():
        window.device_list.addItem(f"{deck['type']} - {deck_id}", userData=deck_id)

        tab = window.cards.currentWidget()
        row_layout = QtWidgets.QVBoxLayout()
        tab.children()[0].addLayout(row_layout, 0, 0)

        buttons = []
        index = 0
        for row in range(deck["layout"][0]):
            column_layout = QtWidgets.QHBoxLayout()
            row_layout.addLayout(column_layout)

            for column in range(deck["layout"][1]):
                index += 1
                button = QtWidgets.QPushButton()
                button.setCheckable(True)
                button.index = index
                button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                button.setStyleSheet(
                    """QPushButton{background-color:black;}
                                        QPushButton:checked{background-color:darkGray;}
                                        QPushButton:focus{border:none; }
                                     """
                )
                buttons.append(button)
                column_layout.addWidget(button)

        for button in buttons:
            button.clicked.connect(
                lambda button=button, buttons=buttons: button_clicked(button, buttons)
            )

        buttons[0].click()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(start())
