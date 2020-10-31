"""Defines the QT powered interface for configuring Stream Decks"""
import os
import sys
from functools import partial

from PySide2 import QtWidgets
from PySide2.QtCore import QSize, Qt, QTimer
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QSystemTrayIcon,
)

from streamdeck_ui import api
from streamdeck_ui.config import LOGO, PROJECT_PATH
from streamdeck_ui.ui_main import Ui_MainWindow

BUTTON_SYTLE = """
    QToolButton{background-color:black;}
    QToolButton:checked{background-color:darkGray;}
    QToolButton:focus{border:none; }
"""

selected_button: QtWidgets.QToolButton
text_timer = None


def _deck_id(ui) -> str:
    return ui.device_list.itemData(ui.device_list.currentIndex())


def _page(ui) -> int:
    return ui.pages.currentIndex()


def update_button_text(ui, text: str) -> None:
    deck_id = _deck_id(ui)
    api.set_button_text(deck_id, _page(ui), selected_button.index, text)
    redraw_buttons(ui)


def update_button_command(ui, command: str) -> None:
    deck_id = _deck_id(ui)
    api.set_button_command(deck_id, _page(ui), selected_button.index, command)


def update_button_keys(ui, keys: str) -> None:
    deck_id = _deck_id(ui)
    api.set_button_keys(deck_id, _page(ui), selected_button.index, keys)


def update_button_write(ui) -> None:
    deck_id = _deck_id(ui)
    api.set_button_write(deck_id, _page(ui), selected_button.index, ui.write.toPlainText())


def update_change_brightness(ui, amount: int) -> None:
    deck_id = _deck_id(ui)
    api.set_button_change_brightness(deck_id, _page(ui), selected_button.index, amount)


def update_switch_page(ui, page: int) -> None:
    deck_id = _deck_id(ui)
    api.set_button_switch_page(deck_id, _page(ui), selected_button.index, page)


def _highlight_first_button(ui) -> None:
    button = ui.pages.currentWidget().findChildren(QtWidgets.QToolButton)[0]
    button.setChecked(False)
    button.click()


def change_page(ui, page: int) -> None:
    api.set_page(_deck_id(ui), page)
    redraw_buttons(ui)
    _highlight_first_button(ui)


def select_image(window) -> None:
    file_name = QFileDialog.getOpenFileName(
        window, "Open Image", os.path.expanduser("~"), "Image Files (*.png *.jpg *.bmp)"
    )[0]
    deck_id = _deck_id(window.ui)
    api.set_button_icon(deck_id, _page(window.ui), selected_button.index, file_name)
    redraw_buttons(window.ui)


def redraw_buttons(ui) -> None:
    deck_id = _deck_id(ui)
    current_tab = ui.pages.currentWidget()
    buttons = current_tab.findChildren(QtWidgets.QToolButton)
    for button in buttons:
        # Give "info" priority
        info = api.get_button_info(deck_id, _page(ui), button.index)
        if info:
            button.setText(info)
            continue

        button.setText(api.get_button_text(deck_id, _page(ui), button.index))
        button.setIcon(QIcon(api.get_button_icon(deck_id, _page(ui), button.index)))


def set_brightness(ui, value: int) -> None:
    deck_id = _deck_id(ui)
    api.set_brightness(deck_id, value)


def set_information(ui, index: int, button=None, build: bool=False) -> None:
    if not button:
        button = selected_button
    deck_id = _deck_id(ui)
    prev_information_index = api.get_button_information_index(deck_id, _page(ui), button.index)
    if prev_information_index == index and not build:
        return

    api.set_button_information_index(deck_id, _page(ui), button.index, index)

    if index == 1:
        # Current Time (H:M:S)
        api.set_button_live_time(deck_id, _page(ui), button.index, True)
    elif index == 2:
        # Current Time (H)
        api.set_button_live_hour(deck_id, _page(ui), button.index, True)
    elif index == 3:
        # Current Time (M)
        api.set_button_live_minute(deck_id, _page(ui), button.index, True)
    else:
        api.set_button_live_time(deck_id, _page(ui), button.index, False)

    ui.text.setText(api.get_button_text(deck_id, _page(ui), button.index))


def button_clicked(ui, clicked_button, buttons) -> None:
    global selected_button
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)

    deck_id = _deck_id(ui)
    button_id = selected_button.index
    text = api.get_button_text(deck_id, _page(ui), button_id)
    ui.text.setText(text)
    ui.command.setText(api.get_button_command(deck_id, _page(ui), button_id))
    ui.keys.setText(api.get_button_keys(deck_id, _page(ui), button_id))
    ui.write.setPlainText(api.get_button_write(deck_id, _page(ui), button_id))
    ui.change_brightness.setValue(api.get_button_change_brightness(deck_id, _page(ui), button_id))
    ui.switch_page.setValue(api.get_button_switch_page(deck_id, _page(ui), button_id))

    info_index = api.get_button_information_index(deck_id, _page(ui), button_id)
    if info_index == 0:
        api.set_button_info(deck_id, _page(ui), button_id, "")
    ui.information.setCurrentIndex(info_index)

    redraw_buttons(ui)


def build_buttons(ui, tab) -> None:
    deck_id = _deck_id(ui)
    deck = api.get_deck(deck_id)

    if hasattr(tab, "deck_buttons"):
        tab.deck_buttons.hide()
        tab.deck_buttons.deleteLater()

    base_widget = QtWidgets.QWidget(tab)
    tab.children()[0].addWidget(base_widget)
    tab.deck_buttons = base_widget

    row_layout = QtWidgets.QVBoxLayout(base_widget)
    index = 0
    buttons = []
    for _row in range(deck["layout"][0]):  # type: ignore
        column_layout = QtWidgets.QHBoxLayout()
        row_layout.addLayout(column_layout)

        for _column in range(deck["layout"][1]):  # type: ignore
            button = QtWidgets.QToolButton(base_widget)
            button.setCheckable(True)
            button.index = index
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setIconSize(QSize(100, 100))
            button.setStyleSheet(BUTTON_SYTLE)
            buttons.append(button)
            column_layout.addWidget(button)
            index += 1

    for button in buttons:
        button.clicked.connect(
            lambda button=button, buttons=buttons: button_clicked(ui, button, buttons)
        )

        info_index = api.get_button_information_index(deck_id, _page(ui), button.index)
        if info_index != 0:
            set_information(ui, info_index, button, build=True)

    redraw_buttons(ui)
    tab.hide()
    tab.show()


def export_config(window) -> None:
    file_name = QFileDialog.getSaveFileName(
        window, "Export Config", os.path.expanduser("~/streamdeck_ui_export.json"), "JSON (*.json)"
    )[0]
    if not file_name:
        return

    api.export_config(file_name)


def import_config(window) -> None:
    file_name = QFileDialog.getOpenFileName(
        window, "Import Config", os.path.expanduser("~"), "Config Files (*.json)"
    )[0]
    if not file_name:
        return

    api.import_config(file_name)
    redraw_buttons(window.ui)


def sync(ui) -> None:
    api.ensure_decks_connected()
    ui.brightness.setValue(api.get_brightness(_deck_id(ui)))
    ui.pages.setCurrentIndex(api.get_page(_deck_id(ui)))


def build_device(ui, _device_index=None) -> None:
    for page_id in range(ui.pages.count()):
        page = ui.pages.widget(page_id)
        page.setStyleSheet("background-color: black")
        build_buttons(ui, page)

    sync(ui)
    _highlight_first_button(ui)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_shown: bool = True

    def closeEvent(self, event) -> None:  # noqa: N802 - Part of QT signature.
        self.window_shown = False
        self.hide()
        event.ignore()

    def systray_clicked(self, _status=None) -> None:
        self.hide()
        if self.window_shown:
            self.window_shown = False
            return

        self.show()
        self.activateWindow()
        getattr(self, "raise")()  # noqa: B009 - Can't call as self.raise() due to syntax error.
        self.window_shown = True


def queue_text_change(ui, text: str) -> None:
    global text_timer

    if text_timer:
        text_timer.stop()

    text_timer = QTimer()
    text_timer.setSingleShot(True)
    text_timer.timeout.connect(partial(update_button_text, ui, text))
    text_timer.start(500)


def start(_exit: bool = False) -> None:
    app = QApplication(sys.argv)

    logo = QIcon(LOGO)
    main_window = MainWindow()
    ui = main_window.ui
    main_window.setWindowIcon(logo)
    tray = QSystemTrayIcon(logo, app)
    tray.activated.connect(main_window.systray_clicked)

    menu = QMenu()
    action_exit = QAction("Exit")
    action_exit.triggered.connect(app.exit)
    menu.addAction(action_exit)

    tray.setContextMenu(menu)

    ui.text.textChanged.connect(partial(queue_text_change, ui))
    ui.command.textChanged.connect(partial(update_button_command, ui))
    ui.keys.textChanged.connect(partial(update_button_keys, ui))
    ui.write.textChanged.connect(partial(update_button_write, ui))
    ui.change_brightness.valueChanged.connect(partial(update_change_brightness, ui))
    ui.switch_page.valueChanged.connect(partial(update_switch_page, ui))
    ui.imageButton.clicked.connect(partial(select_image, main_window))
    ui.brightness.valueChanged.connect(partial(set_brightness, ui))
    ui.information.currentIndexChanged.connect(partial(set_information, ui))
    for deck_id, deck in api.open_decks().items():
        ui.device_list.addItem(f"{deck['type']} - {deck_id}", userData=deck_id)

    build_device(ui)
    ui.device_list.currentIndexChanged.connect(partial(build_device, ui))

    ui.pages.currentChanged.connect(partial(change_page, ui))

    ui.actionExport.triggered.connect(partial(export_config, main_window))
    ui.actionImport.triggered.connect(partial(import_config, main_window))

    timer = QTimer()
    timer.timeout.connect(partial(sync, ui))
    timer.start(1000)

    api.render()
    tray.show()
    main_window.show()
    if _exit:
        return
    else:
        sys.exit(app.exec_())


if __name__ == "__main__":
    start()
