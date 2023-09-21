"""Defines the QT powered interface for configuring Stream Decks"""
import os
import shlex
import signal
import sys
from functools import partial
from subprocess import Popen  # nosec - Need to allow users to specify arbitrary commands
from typing import Dict, List, Optional

import pkg_resources
from PySide6 import QtWidgets
from PySide6.QtCore import QMimeData, QSettings, QSignalBlocker, QSize, Qt, QTimer, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QDrag, QIcon, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QSystemTrayIcon,
)

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.cli.server import CLIStreamDeckServer
from streamdeck_ui.config import (
    APP_LOGO,
    APP_NAME,
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_FONT_COLOR,
    FONTS_PATH,
    STATE_FILE,
)
from streamdeck_ui.modules.keyboard import Keyboard, pynput_supported
from streamdeck_ui.semaphore import Semaphore, SemaphoreAcquireError
from streamdeck_ui.ui_main import Ui_MainWindow
from streamdeck_ui.ui_settings import Ui_SettingsDialog

api: StreamDeckServer

BUTTON_STYLE = """
    QToolButton {
    margin: 2px;
    border: 2px solid #444444;
    border-radius: 8px;
    background-color: #000000;
    border-style: outset;}
    QToolButton:checked {
    margin: 2px;
    border: 2px solid #cccccc;
    border-radius: 8px;
    background-color: #000000;
    border-style: outset;}
"""

BUTTON_DRAG_STYLE = """
    QToolButton {
    margin: 2px;
    border: 2px solid #999999;
    border-radius: 8px;
    background-color: #000000;
    border-style: outset;}
"""

DEVICE_PAGE_STYLE = """
background-color: black
"""

selected_button: Optional[QtWidgets.QToolButton] = None
"A reference to the currently selected button"

text_update_timer: Optional[QTimer] = None
"Timer used to delay updates to the button text"

dimmer_options = {
    "Never": 0,
    "10 Seconds": 10,
    "1 Minute": 60,
    "5 Minutes": 300,
    "10 Minutes": 600,
    "15 Minutes": 900,
    "30 Minutes": 1800,
    "1 Hour": 3600,
    "5 Hours": 7200,
    "10 Hours": 36000,
}
last_image_dir = ""


class DraggableButton(QtWidgets.QToolButton):
    """A QToolButton that supports drag and drop and swaps the button properties on drop"""

    def __init__(self, parent, ui, api: StreamDeckServer):
        super(DraggableButton, self).__init__(parent)

        self.setAcceptDrops(True)
        self.ui = ui
        self.api = api

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.
        if e.buttons() != Qt.LeftButton:
            return

        self.api.reset_dimmer(_deck_id(self.ui))

        mimedata = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec(Qt.MoveAction)

    def dropEvent(self, e):  # noqa: N802 - Part of QT signature.
        global selected_button

        self.setStyleSheet(BUTTON_STYLE)
        serial_number = _deck_id(self.ui)
        page = _page(self.ui)

        index = self.property("index")
        if e.source():
            source_index = e.source().property("index")
            # Ignore drag and drop on yourself
            if source_index == index:
                return

            self.api.swap_buttons(serial_number, page, source_index, index)
            # In the case that we've dragged the currently selected button, we have to
            # check the target button instead so it appears that it followed the drag/drop
            if e.source().isChecked():
                e.source().setChecked(False)
                self.setChecked(True)
                selected_button = self
        else:
            # Handle drag and drop from outside the application
            if e.mimeData().hasUrls:
                file_name = e.mimeData().urls()[0].toLocalFile()
                self.api.set_button_icon(serial_number, page, index, file_name)

        if e.source():
            source_index = e.source().property("index")
            icon = self.api.get_button_icon_pixmap(serial_number, page, source_index)
            if icon:
                e.source().setIcon(icon)

        icon = self.api.get_button_icon_pixmap(serial_number, page, index)
        if icon:
            self.setIcon(icon)

    def dragEnterEvent(self, e):  # noqa: N802 - Part of QT signature.
        if type(self) is DraggableButton:
            e.setAccepted(True)
            self.setStyleSheet(BUTTON_DRAG_STYLE)
        else:
            e.setAccepted(False)

    def dragLeaveEvent(self, e):  # noqa: N802 - Part of QT signature.
        self.setStyleSheet(BUTTON_STYLE)


def handle_keypress(ui, deck_id: str, key: int, state: bool) -> None:
    # TODO: Handle both key down and key up events in future.
    if state:
        if api.reset_dimmer(deck_id):
            return

        page = api.get_page(deck_id)
        command = api.get_button_command(deck_id, page, key)
        if command:
            try:
                Popen(shlex.split(command))  # nosec, need to allow execution of arbitrary commands
            except Exception as error:
                print(f"The command '{command}' failed: {error}")

        keyboard = Keyboard()

        keys = api.get_button_keys(deck_id, page, key)
        if keys:
            try:
                keyboard.keys(keys)
            except Exception as error:
                print(f"Could not press keys '{keys}': {error}")

        write = api.get_button_write(deck_id, page, key)
        if write:
            try:
                keyboard.write(write)
            except Exception as error:
                print(f"Could not complete the write command: {error}")

        brightness_change = api.get_button_change_brightness(deck_id, page, key)
        if brightness_change:
            try:
                api.change_brightness(deck_id, brightness_change)
            except Exception as error:
                print(f"Could not change brightness: {error}")

        switch_page = api.get_button_switch_page(deck_id, page, key)
        if switch_page:
            api.set_page(deck_id, switch_page - 1)
            if _deck_id(ui) == deck_id:
                ui.pages.setCurrentIndex(switch_page - 1)


def _deck_id(ui: Ui_MainWindow) -> str:
    """Returns the currently selected Stream Deck serial number

    :param ui: A reference to the ui object
    :type ui: _type_
    :return: The serial number
    :rtype: str
    """
    return ui.device_list.itemData(ui.device_list.currentIndex())


def _page(ui: Ui_MainWindow) -> int:
    tab_index = ui.pages.currentIndex()
    page = ui.pages.widget(tab_index)
    return page.property("page_id")


def _button(_ui: Ui_MainWindow) -> int:
    if selected_button is not None:
        index = selected_button.property("index")
        return index
    return -1


def update_button_text(ui, text: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        if deck_id:
            # There may be no decks attached
            api.set_button_text(deck_id, _page(ui), _button(ui), text)
            icon = api.get_button_icon_pixmap(deck_id, _page(ui), _button(ui))
            if icon:
                selected_button.setIcon(icon)


def update_button_command(ui, command: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_command(deck_id, _page(ui), _button(ui), command)


def update_button_keys(ui, keys: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_keys(deck_id, _page(ui), _button(ui), keys)


def update_button_write(ui) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_write(deck_id, _page(ui), _button(ui), ui.write.toPlainText())


def update_change_brightness(ui, amount: int) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_change_brightness(deck_id, _page(ui), _button(ui), amount)


def update_switch_page(ui, page: int) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_switch_page(deck_id, _page(ui), _button(ui), page)


def handle_change_page(ui) -> None:
    """Change the Stream Deck to the desired page and update
    the on-screen buttons.
    """
    global selected_button

    if selected_button:
        selected_button.setChecked(False)
        selected_button = None

    deck_id = _deck_id(ui)
    page = _page(ui)
    if deck_id:
        api.set_page(deck_id, page)
        redraw_buttons(ui)
        api.reset_dimmer(deck_id)

    reset_button_configuration(ui)


def handle_new_page(ui) -> None:
    deck_id = _deck_id(ui)
    if not deck_id:
        return

    # Add the new page to the api
    new_page_index = api.add_new_page(deck_id)
    build_device(ui)

    # look for the new page in the ui
    for page in range(ui.pages.count()):
        if ui.pages.widget(page).property("page_id") == new_page_index:
            ui.pages.setCurrentIndex(page)
            break
    ui.remove_page.setEnabled(True)


def handle_delete_page_with_confirmation(main_window, ui) -> None:
    confirm = QMessageBox(main_window)
    confirm.setWindowTitle("Delete Page")
    confirm.setText("Are you sure you want to delete this page?")
    confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirm.setIcon(QMessageBox.Icon.Question)
    button = confirm.exec()
    if button == QMessageBox.StandardButton.Yes:
        handle_delete_page(ui)


def handle_delete_page(ui) -> None:
    deck_id = _deck_id(ui)
    if not deck_id:
        return
    pages = api.get_pages(deck_id)
    if len(pages) == 1:
        return

    page = _page(ui)
    new_page = _closest_page(page, pages)
    tab_index_to_move = -1
    tab_index_to_remove = -1
    for tab_index in range(ui.pages.count()):
        tab = ui.pages.widget(tab_index)
        if tab.property("page_id") == new_page:
            tab_index_to_move = tab_index
        if tab.property("page_id") == page:
            tab_index_to_remove = tab_index

    ui.pages.setCurrentIndex(tab_index_to_move)
    api.remove_page(deck_id, page)
    ui.pages.removeTab(tab_index_to_remove)
    if ui.pages.count() == 1:
        ui.remove_page.setEnabled(False)


def _closest_page(page: int, pages: List[int]) -> int:
    if page not in pages:
        return -1
    page_index = pages.index(page)
    if page_index == 0:
        return pages[1]
    elif page_index == len(pages) - 1:
        return pages[page_index - 1]
    else:
        prev_page = pages[page_index - 1]
        next_page = pages[page_index + 1]
        if abs(page - prev_page) <= abs(page - next_page):
            return prev_page
        else:
            return next_page


def select_image(window) -> None:
    global last_image_dir
    deck_id = _deck_id(window.ui)
    image_file = api.get_button_icon(deck_id, _page(window.ui), _button(window.ui))
    if not image_file:
        if not last_image_dir:
            image_file = os.path.expanduser("~")
        else:
            image_file = last_image_dir
    file_name = QFileDialog.getOpenFileName(
        window, "Open Image", image_file, "Image Files (*.png *.jpg *.bmp *.svg *.gif)"
    )[0]
    if file_name:
        last_image_dir = os.path.dirname(file_name)
        deck_id = _deck_id(window.ui)
        api.set_button_icon(deck_id, _page(window.ui), _button(window.ui), file_name)
        redraw_buttons(window.ui)


def align_text_vertical(window) -> None:
    serial_number = _deck_id(window.ui)
    position = api.get_text_vertical_align(serial_number, _page(window.ui), _button(window.ui))
    if position == "bottom" or position == "":
        position = "middle-bottom"
    elif position == "middle-bottom":
        position = "middle"
    elif position == "middle":
        position = "middle-top"
    elif position == "middle-top":
        position = "top"
    else:
        position = ""

    api.set_text_vertical_align(serial_number, _page(window.ui), _button(window.ui), position)
    redraw_buttons(window.ui)


def align_text_horizontal(window) -> None:
    serial_number = _deck_id(window.ui)
    position = api.get_text_horizontal_align(serial_number, _page(window.ui), _button(window.ui))
    if position == "center" or position == "":
        position = "left"
    elif position == "left":
        position = "right"
    elif position == "right":
        position = ""

    api.set_text_horizontal_align(serial_number, _page(window.ui), _button(window.ui), position)
    redraw_buttons(window.ui)


def remove_image(window) -> None:
    deck_id = _deck_id(window.ui)
    image = api.get_button_icon(deck_id, _page(window.ui), _button(window.ui))
    if image:
        confirm = QMessageBox(window)
        confirm.setWindowTitle("Remove image")
        confirm.setText("Are you sure you want to remove the image for this button?")
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm.setIcon(QMessageBox.Icon.Question)
        button = confirm.exec()
        if button == QMessageBox.StandardButton.Yes:
            api.set_button_icon(deck_id, _page(window.ui), _button(window.ui), "")
            redraw_buttons(window.ui)


def redraw_buttons(ui) -> None:
    deck_id = _deck_id(ui)
    current_tab = ui.pages.currentWidget()
    buttons = current_tab.findChildren(QtWidgets.QToolButton)
    for button in buttons:
        if not button.isHidden():
            # When rebuilding the buttons, we hide the old ones
            # and mark for deletion. They still hang around so
            # ignore them here
            icon = api.get_button_icon_pixmap(deck_id, _page(ui), button.property("index"))
            if icon:
                button.setIcon(icon)


def set_brightness(ui, value: int) -> None:
    deck_id = _deck_id(ui)
    api.set_brightness(deck_id, value)


def set_brightness_dimmed(ui, value: int) -> None:
    deck_id = _deck_id(ui)
    api.set_brightness_dimmed(deck_id, value)
    api.reset_dimmer(deck_id)


def button_clicked(ui, clicked_button, buttons) -> None:
    global selected_button
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)

    deck_id = _deck_id(ui)
    button_id = _button(ui)
    if selected_button.isChecked():  # type: ignore # False positive mypy
        enable_button_configuration(ui, True)
        ui.text.setText(api.get_button_text(deck_id, _page(ui), button_id))
        ui.command.setText(api.get_button_command(deck_id, _page(ui), button_id))
        ui.keys.setCurrentText(api.get_button_keys(deck_id, _page(ui), button_id))
        ui.write.setPlainText(api.get_button_write(deck_id, _page(ui), button_id))
        ui.text_font.setCurrentText(api.get_button_font(deck_id, _page(ui), button_id))
        ui.text_font_size.setValue(api.get_button_font_size(deck_id, _page(ui), button_id))
        color = api.get_font_color(deck_id, _page(ui), button_id)
        if color:
            ui.text_color.setPalette(QPalette(color))
        else:
            ui.text_color.setPalette(QPalette(DEFAULT_FONT_COLOR))
        background_color = api.get_background_color(deck_id, _page(ui), button_id)
        if background_color:
            ui.background_color.setPalette(QPalette(background_color))
        else:
            ui.background_color.setPalette(QPalette(DEFAULT_BACKGROUND_COLOR))
        ui.change_brightness.setValue(api.get_button_change_brightness(deck_id, _page(ui), button_id))
        ui.switch_page.setValue(api.get_button_switch_page(deck_id, _page(ui), button_id))
        api.reset_dimmer(deck_id)
    else:
        selected_button = None
        reset_button_configuration(ui)


def enable_button_configuration(ui, enabled: bool):
    ui.text.setEnabled(enabled)
    ui.command.setEnabled(enabled)
    ui.keys.setEnabled(enabled)
    ui.text_font.setEnabled(enabled)
    ui.text_font_size.setEnabled(enabled)
    ui.write.setEnabled(enabled)
    ui.change_brightness.setEnabled(enabled)
    ui.switch_page.setEnabled(enabled)
    ui.imageButton.setEnabled(enabled)
    ui.removeButton.setEnabled(enabled)
    ui.text_h_align.setEnabled(enabled)
    ui.text_v_align.setEnabled(enabled)
    ui.text_color.setEnabled(enabled)
    ui.background_color.setEnabled(enabled)
    ui.label_5.setVisible(pynput_supported)
    ui.keys.setVisible(pynput_supported)
    ui.label_6.setVisible(pynput_supported)
    ui.write.setVisible(pynput_supported)


def reset_button_configuration(ui):
    """Clears the configuration for a button and disables editing of them. This is done when
    there is no key selected or if there are no devices connected.
    """
    ui.text.clear()
    ui.command.clear()
    ui.keys.clearEditText()
    ui.text_font.clearEditText()
    ui.text_font_size.setValue(0)
    ui.text_color.setPalette(QPalette(DEFAULT_FONT_COLOR))
    ui.background_color.setPalette(QPalette(DEFAULT_BACKGROUND_COLOR))
    ui.write.clear()
    ui.change_brightness.setValue(0)
    ui.switch_page.setValue(0)
    enable_button_configuration(ui, False)


def browse_documentation():
    url = QUrl("https://streamdeck-linux-gui.github.io/streamdeck-linux-gui/")
    QDesktopServices.openUrl(url)


def browse_github():
    url = QUrl("https://github.com/streamdeck-linux-gui/streamdeck-linux-gui")
    QDesktopServices.openUrl(url)


def build_buttons(ui, tab) -> None:
    global selected_button

    if hasattr(tab, "deck_buttons"):
        buttons = tab.findChildren(QtWidgets.QToolButton)
        for button in buttons:
            button.hide()
            # Mark them as hidden. They will be GC'd later
            button.deleteLater()

        tab.deck_buttons.hide()
        tab.deck_buttons.deleteLater()
        # Remove the inner page
        del tab.children()[0]
        # Remove the property
        del tab.deck_buttons

    selected_button = None
    # When rebuilding any selection is cleared

    deck_id = _deck_id(ui)

    if not deck_id:
        return
    deck = api.get_deck(deck_id)

    # Create a new base_widget with tab as it's parent
    # This is effectively a "blank tab"
    base_widget = QtWidgets.QWidget(tab)

    # Add an inner page (QtQidget) to the page
    tab.children()[0].addWidget(base_widget)

    # Set a property - this allows us to check later
    # if we've already created the buttons
    tab.deck_buttons = base_widget

    row_layout = QtWidgets.QVBoxLayout(base_widget)
    index = 0
    buttons = []
    for _row in range(deck["layout"][0]):  # type: ignore
        column_layout = QtWidgets.QHBoxLayout()
        row_layout.addLayout(column_layout)

        for _column in range(deck["layout"][1]):  # type: ignore
            button = DraggableButton(base_widget, ui, api)
            button.setCheckable(True)
            button.setProperty("index", index)
            button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            button.setIconSize(QSize(80, 80))
            button.setStyleSheet(BUTTON_STYLE)
            buttons.append(button)
            column_layout.addWidget(button)
            index += 1

        column_layout.addStretch(1)
    row_layout.addStretch(1)

    # Note that the button click event captures the ui variable, the current button
    #  and all the other buttons
    for button in buttons:
        button.clicked.connect(lambda button=button, buttons=buttons: button_clicked(ui, button, buttons))


def export_config(window) -> None:
    file_name = QFileDialog.getSaveFileName(
        window, "Export Config", os.path.expanduser("~/streamdeck_ui_export.json"), "JSON (*.json)"
    )[0]
    if not file_name:
        return

    api.export_config(file_name)


def import_config(window) -> None:
    file_name = QFileDialog.getOpenFileName(window, "Import Config", os.path.expanduser("~"), "Config Files (*.json)")[
        0
    ]
    if not file_name:
        return

    api.import_config(file_name)
    redraw_buttons(window.ui)


def _build_tab_label(page_id: int) -> str:
    return f"Page {page_id + 1}" if page_id == 0 else f"{page_id + 1}"


def build_device(ui, _device_index=None) -> None:
    """This method builds the device configuration user interface.
    It is called if you switch to a different Stream Deck,
    a Stream Deck is added or when the last one is removed.
    It must deal with the case where there is no Stream Deck as
    a result.

    :param ui: A reference to the ui
    :type ui: _type_
    :param _device_index: Not used, defaults to None
    :type _device_index: _type_, optional
    """
    blocker = QSignalBlocker(ui.pages)
    try:
        deck_id = _deck_id(ui)
        style = DEVICE_PAGE_STYLE if ui.device_list.count() > 0 else ""

        # clear the pages
        if ui.pages.count() > 0:
            ui.pages.clear()

        current_page = api.get_page(deck_id)
        active_tab_index = 0

        # Add the pages
        for page_id in api.get_pages(deck_id):
            page = QtWidgets.QWidget()
            page.setLayout(QtWidgets.QGridLayout())
            page.setProperty("deck_id", deck_id)
            page.setProperty("page_id", page_id)
            page.setStyleSheet(style)
            label = _build_tab_label(page_id)
            tab_index = ui.pages.addTab(page, label)
            page_tab = ui.pages.widget(tab_index)
            build_buttons(ui, page_tab)
            if page_id == current_page:
                active_tab_index = tab_index

        if ui.pages.count() > 1:
            ui.remove_page.setEnabled(True)
        else:
            ui.remove_page.setEnabled(False)

        if ui.device_list.count() > 0:
            ui.settingsButton.setEnabled(True)
            ui.add_page.setEnabled(True)
            # Set the active page for this device
            ui.pages.setCurrentIndex(active_tab_index)

            # Draw the buttons for the active page
            redraw_buttons(ui)
        else:
            ui.settingsButton.setEnabled(False)
            ui.add_page.setEnabled(False)
            reset_button_configuration(ui)
    finally:
        blocker.unblock()


class MainWindow(QMainWindow):
    """Represents the main streamdeck-ui configuration Window. A QMainWindow
    object provides a lot of standard main window features out the box.

    The QtCreator UI designer allows you to create a UI quickly. It compiles
    into a class called Ui_MainWindow() and everything comes together by
    calling the setupUi() method and passing a reference to the QMainWindow.

    :param QMainWindow: The parent QMainWindow object
    :type QMainWindow: [type]
    """

    ui: Ui_MainWindow
    "A reference to all the UI objects for the main window"

    window_shown: bool
    settings: QSettings

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_shown = True
        self.settings = QSettings("streamdeck-ui", "streamdeck-ui")
        self.restoreGeometry(self.settings.value("geometry", self.saveGeometry()))

    def closeEvent(self, event) -> None:  # noqa: N802 - Part of QT signature.
        self.settings.setValue("geometry", self.saveGeometry())
        self.window_shown = False
        self.hide()
        event.ignore()

    def systray_clicked(self, status=None) -> None:
        if status is QtWidgets.QSystemTrayIcon.ActivationReason.Context:
            return
        if self.window_shown:
            self.hide()
            self.window_shown = False
            return

        self.bring_to_top()

    def bring_to_top(self):
        self.show()
        self.activateWindow()
        self.raise_()
        self.window_shown = True

    def about_dialog(self):
        title = "About StreamDeck UI"
        description = "A Linux compatible UI for the Elgato Stream Deck."
        app = QApplication.instance()
        body = [description, "Version {}\n".format(app.applicationVersion())]
        dependencies = ("streamdeck", "pyside6", "pillow", "pynput")
        for dep in dependencies:
            try:
                dist = pkg_resources.get_distribution(dep)
                body.append("{} {}".format(dep, dist.version))
            except pkg_resources.DistributionNotFound:
                pass
        QtWidgets.QMessageBox.about(self, title, "\n".join(body))


def update_button_text_font(ui, font: str) -> None:
    if not selected_button:
        return
    deck_id = _deck_id(ui)
    if deck_id is None:
        return
    api.set_button_font(deck_id, _page(ui), _button(ui), font)
    icon = api.get_button_icon_pixmap(deck_id, _page(ui), _button(ui))
    if icon:
        selected_button.setIcon(icon)


def update_button_text_font_size(ui, font_size: int) -> None:
    if not selected_button:
        return
    deck_id = _deck_id(ui)
    if deck_id is None:
        return
    api.set_button_font_size(deck_id, _page(ui), _button(ui), font_size)
    icon = api.get_button_icon_pixmap(deck_id, _page(ui), _button(ui))
    if icon:
        selected_button.setIcon(icon)


def queue_update_button_text(ui) -> None:
    """Instead of directly updating the text (label) associated with
    the button, add a small delay. If this is called before the
    timer fires, delay it again. Effectively this creates an update
    queue. It makes the textbox more response, as rendering the button
    and saving to the API each time can feel somewhat slow.

    :param ui: Reference to the ui
    :type ui: _type_
    """
    text = ui.text.toPlainText()

    global text_update_timer

    if text_update_timer:
        text_update_timer.stop()

    text_update_timer = QTimer()
    text_update_timer.setSingleShot(True)
    text_update_timer.timeout.connect(partial(update_button_text, ui, text))  # type: ignore [attr-defined]
    text_update_timer.start(500)


def change_brightness(deck_id: str, brightness: int):
    """Changes the brightness of the given streamdeck, but does not save
    the state."""
    api.decks[deck_id].set_brightness(brightness)


class SettingsDialog(QDialog):
    ui: Ui_SettingsDialog

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.show()


def show_settings(window: MainWindow) -> None:
    """Shows the settings dialog and allows the user the change deck specific
    settings. Settings are not saved until OK is clicked."""
    ui = window.ui
    deck_id = _deck_id(ui)
    settings = SettingsDialog(window)
    api.stop_dimmer(deck_id)

    for label, value in dimmer_options.items():
        settings.ui.dim.addItem(f"{label}", userData=value)

    existing_timeout = api.get_display_timeout(deck_id)
    existing_index = next((i for i, (k, v) in enumerate(dimmer_options.items()) if v == existing_timeout), None)

    if existing_index is None:
        settings.ui.dim.addItem(f"Custom: {existing_timeout}s", userData=existing_timeout)
        existing_index = settings.ui.dim.count() - 1
        settings.ui.dim.setCurrentIndex(existing_index)
    else:
        settings.ui.dim.setCurrentIndex(existing_index)

    existing_brightness_dimmed = api.get_brightness_dimmed(deck_id)
    settings.ui.brightness_dimmed.setValue(existing_brightness_dimmed)

    settings.ui.label_streamdeck.setText(deck_id)
    settings.ui.brightness.setValue(api.get_brightness(deck_id))
    settings.ui.brightness.valueChanged.connect(partial(change_brightness, deck_id))
    settings.ui.dim.currentIndexChanged.connect(partial(disable_dim_settings, settings))
    if settings.exec():
        # Commit changes
        if existing_index != settings.ui.dim.currentIndex():
            # dimmers[deck_id].timeout = settings.ui.dim.currentData()
            api.set_display_timeout(deck_id, settings.ui.dim.currentData())
        set_brightness(window.ui, settings.ui.brightness.value())
        set_brightness_dimmed(window.ui, settings.ui.brightness_dimmed.value())
    else:
        # User cancelled, reset to original brightness
        change_brightness(deck_id, api.get_brightness(deck_id))

    api.reset_dimmer(deck_id)


def disable_dim_settings(settings: SettingsDialog, _index: int) -> None:
    disable = dimmer_options.get(settings.ui.dim.currentText()) == 0
    settings.ui.brightness_dimmed.setDisabled(disable)
    settings.ui.label_brightness_dimmed.setDisabled(disable)


def toggle_dim_all() -> None:
    api.toggle_dimmers()


def create_main_window(logo: QIcon, app: QApplication) -> MainWindow:
    """Creates the main application window and configures slots and signals

    :param logo: The icon displayed in the main application window
    :type logo: QIcon
    :param app: The QApplication that started it all
    :type app: QApplication
    :return: Returns the MainWindow instance
    :rtype: MainWindow
    """
    main_window = MainWindow()
    ui = main_window.ui
    ui.text.textChanged.connect(partial(queue_update_button_text, ui))
    ui.command.textChanged.connect(partial(update_button_command, ui))
    ui.keys.currentTextChanged.connect(partial(update_button_keys, ui))
    ui.write.textChanged.connect(partial(update_button_write, ui))
    ui.change_brightness.valueChanged.connect(partial(update_change_brightness, ui))
    ui.text_font_size.valueChanged.connect(partial(update_button_text_font_size, ui))
    set_button_text_font_list(ui)
    ui.text_color.clicked.connect(partial(show_color_dialog_font, ui))
    ui.background_color.clicked.connect(partial(show_color_dialog_background, ui))
    ui.switch_page.valueChanged.connect(partial(update_switch_page, ui))
    ui.imageButton.clicked.connect(partial(select_image, main_window))
    ui.text_h_align.clicked.connect(partial(align_text_horizontal, main_window))
    ui.text_v_align.clicked.connect(partial(align_text_vertical, main_window))
    ui.removeButton.clicked.connect(partial(remove_image, main_window))
    ui.settingsButton.clicked.connect(partial(show_settings, main_window))
    ui.add_page.clicked.connect(partial(handle_new_page, ui))
    ui.remove_page.clicked.connect(partial(handle_delete_page_with_confirmation, main_window, ui))
    ui.actionExport.triggered.connect(partial(export_config, main_window))
    ui.actionImport.triggered.connect(partial(import_config, main_window))
    ui.actionExit.triggered.connect(app.exit)
    ui.actionAbout.triggered.connect(main_window.about_dialog)
    ui.actionDocs.triggered.connect(browse_documentation)
    ui.actionGithub.triggered.connect(browse_github)
    ui.settingsButton.setEnabled(False)
    enable_button_configuration(ui, False)
    return main_window


def set_button_text_font_list(ui: Ui_MainWindow) -> None:
    """Prepares the font selection combo box with all available fonts"""
    ui.text_font.currentTextChanged.connect(partial(update_button_text_font, ui))
    ui.text_font.clear()
    font_files = [f for f in os.listdir(os.path.join(FONTS_PATH)) if f.endswith(".ttf")]

    ui.text_font.addItem("")
    for font_file in font_files:
        # remove extension from font_file
        ui.text_font.addItem(font_file)


def show_color_dialog_font(ui: Ui_MainWindow) -> None:
    current_color = ui.text_color.palette().color(QPalette.ColorRole.Button)
    color = QColorDialog.getColor(current_color, ui.text_color, "Select text color")

    if color.isValid():
        ui.text_color.setPalette(QPalette(color))
        color_hex = color.name()
        api.set_font_color(_deck_id(ui), _page(ui), _button(ui), color_hex)
        redraw_buttons(ui)


def show_color_dialog_background(ui: Ui_MainWindow) -> None:
    current_color = ui.background_color.palette().color(QPalette.ColorRole.Button)
    color = QColorDialog.getColor(current_color, ui.background_color, "Select background color")

    if color.isValid():
        ui.background_color.setPalette(QPalette(color))
        color_hex = color.name()
        api.set_background_color(_deck_id(ui), _page(ui), _button(ui), color_hex)
        redraw_buttons(ui)


def create_tray(logo: QIcon, app: QApplication, main_window: MainWindow) -> QSystemTrayIcon:
    """Creates a system tray with the provided icon and parent. The main
    window passed will be activated when clicked.

    :param logo: The icon to show in the system tray
    :type logo: QIcon
    :param app: The parent object the tray is bound to
    :type app: QApplication
    :param main_window: The window what will be activated by the tray
    :type main_window: QMainWindow
    :return: Returns the QSystemTrayIcon instance
    :rtype: QSystemTrayIcon
    """
    tray = QSystemTrayIcon(logo, app)
    tray.activated.connect(main_window.systray_clicked)  # type: ignore [attr-defined]

    menu = QMenu()
    action_dim = QAction("Dim display (toggle)", main_window)
    action_dim.triggered.connect(toggle_dim_all)  # type: ignore [attr-defined]
    action_configure = QAction("Configure...", main_window)
    action_configure.triggered.connect(main_window.bring_to_top)  # type: ignore [attr-defined]
    menu.addAction(action_dim)
    menu.addAction(action_configure)
    menu.addSeparator()
    action_exit = QAction("Exit", main_window)
    action_exit.triggered.connect(app.exit)  # type: ignore [attr-defined]
    menu.addAction(action_exit)
    tray.setContextMenu(menu)
    return tray


def streamdeck_cpu_changed(ui, serial_number: str, cpu: int):
    if cpu > 100:
        cpu = 100
    if _deck_id(ui) == serial_number:
        ui.cpu_usage.setValue(cpu)
        ui.cpu_usage.setToolTip(f"Rendering CPU usage: {cpu}%")
        ui.cpu_usage.update()


def streamdeck_attached(ui, deck: Dict):
    serial_number = deck["serial_number"]
    blocker = QSignalBlocker(ui.device_list)
    try:
        ui.device_list.addItem(f"{deck['type']} - {serial_number}", userData=serial_number)
    finally:
        blocker.unblock()
    build_device(ui)


def streamdeck_detached(ui, serial_number):
    index = ui.device_list.findData(serial_number)
    if index != -1:
        # Should not be (how can you remove a device that was never attached?)
        # Check anyway
        blocker = QSignalBlocker(ui.device_list)
        try:
            ui.device_list.removeItem(index)
        finally:
            blocker.unblock()
        build_device(ui)


def sigterm_handler(api, app, signal_value, frame):
    api.stop()
    app.quit()
    if signal_value == signal.SIGTERM:
        # Indicate to systemd that it was a clean termination
        print("Exiting normally")
        sys.exit()
    else:
        # Terminations for other reasons are treated as an error condition
        sys.exit(1)


def start(_exit: bool = False) -> None:
    global api
    show_ui = True
    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Usage: {os.path.basename(sys.argv[0])}")
        print("Flags:")
        print("  -h, --help\tShow this message")
        print("  -n, --no-ui\tRun the program without showing a UI")
        return
    elif "-n" in sys.argv or "--no-ui" in sys.argv:
        show_ui = False

    try:
        version = pkg_resources.get_distribution("streamdeck-linux-gui").version
    except pkg_resources.DistributionNotFound:
        version = "devel"

    try:
        with Semaphore("/tmp/streamdeck_ui.lock"):  # nosec - this file is only observed with advisory lock
            # The semaphore was created, so this is the first instance

            api = StreamDeckServer()
            if os.path.isfile(STATE_FILE):
                api.open_config(STATE_FILE)

            # The QApplication object holds the Qt event loop and you need one of these
            # for your application
            app = QApplication(sys.argv)
            app.setApplicationName(APP_NAME)
            app.setApplicationVersion(version)
            logo = QIcon(APP_LOGO)
            app.setWindowIcon(logo)
            main_window = create_main_window(logo, app)
            ui = main_window.ui
            tray = create_tray(logo, app, main_window)

            api.streamdeck_keys.key_pressed.connect(partial(handle_keypress, ui))

            ui.device_list.currentIndexChanged.connect(partial(build_device, ui))
            ui.pages.currentChanged.connect(lambda: handle_change_page(ui))

            api.plugevents.attached.connect(partial(streamdeck_attached, ui))
            api.plugevents.detached.connect(partial(streamdeck_detached, ui))
            api.plugevents.cpu_changed.connect(partial(streamdeck_cpu_changed, ui))

            api.start()

            cli = CLIStreamDeckServer(api, ui)
            cli.start()

            # Configure signal hanlders
            # https://stackoverflow.com/a/4939113/192815
            timer = QTimer()
            timer.start(500)
            timer.timeout.connect(lambda: None)  # type: ignore [attr-defined] # Let interpreter run to handle signal

            # Handle SIGTERM so we release semaphore and shutdown API gracefully
            signal.signal(signal.SIGTERM, partial(sigterm_handler, api, app))

            # Handle <ctrl+c>
            signal.signal(signal.SIGINT, partial(sigterm_handler, api, app))

            tray.show()
            if show_ui:
                main_window.show()

            if _exit:
                return
            else:
                app.exec()
                api.stop()
                cli.stop()
                sys.exit()

    except SemaphoreAcquireError:
        # The semaphore already exists, so another instance is running
        sys.exit()


if __name__ == "__main__":
    start()
