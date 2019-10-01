import os
import sys
from functools import partial

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QSizePolicy

from streamdeck_ui import api

STREAMDECK_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.ui")

selected_button = None


def update_button_text(window, text):
    deck_id = window.device_list.itemData(0)
    api.set_button_text(deck_id, selected_button.index, text)


def update_button_command(window, command):
    deck_id = window.device_list.itemData(0)
    api.set_button_command(deck_id, selected_button.index, command)


def button_clicked(window, clicked_button, buttons):
    global selected_button
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)

    deck_id = window.device_list.itemData(0)
    button_id = selected_button.index
    window.text.setText(api.get_button_text(deck_id, button_id))
    window.command.setText(api.get_button_command(deck_id, button_id))


def start():
    app = QApplication(sys.argv)
    window = QUiLoader().load(STREAMDECK_TEMPLATE)
    window.show()

    window.text.textChanged.connect(partial(update_button_text, window))
    window.command.textChanged.connect(partial(update_button_command, window))
    for deck_id, deck in api.open_decks().items():
        window.device_list.addItem(f"{deck['type']} - {deck_id}", userData=deck_id)

        tab = window.cards.currentWidget()
        row_layout = QtWidgets.QVBoxLayout()
        tab.children()[0].addLayout(row_layout, 0, 0)

        buttons = []
        index = 0
        for _row in range(deck["layout"][0]):
            column_layout = QtWidgets.QHBoxLayout()
            row_layout.addLayout(column_layout)

            for _column in range(deck["layout"][1]):
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
                index += 1

        for button in buttons:
            button.clicked.connect(
                lambda button=button, buttons=buttons: button_clicked(window, button, buttons)
            )

        buttons[0].click()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(start())
