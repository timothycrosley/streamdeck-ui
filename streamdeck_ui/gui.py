"""Defines the QT powered interface for configuring Stream Decks"""
import os
import shlex
import sys
import time
from functools import partial
from subprocess import Popen  # nosec - Need to allow users to specify arbitrary commands
from typing import Callable, Dict

import pkg_resources
from pynput.keyboard import Controller, Key
from PySide2 import QtWidgets
from PySide2.QtCore import QMimeData, QSize, Qt, QTimer, QUrl, QSignalBlocker
from PySide2.QtGui import QDesktopServices, QDrag, QIcon
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QSystemTrayIcon,
)

from streamdeck_ui import api
from streamdeck_ui.config import LOGO
from streamdeck_ui.ui_main import Ui_MainWindow
from streamdeck_ui.ui_settings import Ui_SettingsDialog

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

selected_button: QtWidgets.QToolButton = None
"A reference to the currently selected button"

text_update_timer: QTimer = None
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


class Dimmer:
    timeout = 0
    brightness = -1
    brightness_dimmed = -1
    __stopped = False
    __dimmer_brightness = -1
    __timer = None
    __change_timer = None

    def __init__(
        self,
        timeout: int,
        brightness: int,
        brightness_dimmed: int,
        brightness_callback: Callable[[int], None],
    ):
        """Constructs a new Dimmer instance

        :param int timeout: The time in seconds before the dimmer starts.
        :param int brightness: The normal brightness level.
        :param Callable[[int], None] brightness_callback: Callback that receives the current
                                                          brightness level.
        """
        self.timeout = timeout
        self.brightness = brightness
        self.brightness_dimmed = brightness_dimmed
        self.brightness_callback = brightness_callback

    def stop(self) -> None:
        """Stops the dimmer and sets the brightness back to normal. Call
        reset to start normal dimming operation."""
        if self.__timer:
            self.__timer.stop()

        if self.__change_timer:
            self.__change_timer.stop()

        self.__dimmer_brightness = self.brightness
        try:
            self.brightness_callback(self.brightness)
        except KeyError:
            # During detach cleanup, this is likely to happen
            pass
        self.__stopped = True

    def reset(self) -> bool:
        """Reset the dimmer and start counting down again. If it was busy dimming, it will
        immediately stop dimming. Callback fires to set brightness back to normal."""

        self.__stopped = False
        if self.__timer:
            self.__timer.stop()

        if self.__change_timer:
            self.__change_timer.stop()

        if self.timeout:
            self.__timer = QTimer()
            self.__timer.setSingleShot(True)
            self.__timer.timeout.connect(partial(self.change_brightness))
            self.__timer.start(self.timeout * 1000)

        if self.__dimmer_brightness != self.brightness:
            previous_dimmer_brightness = self.__dimmer_brightness
            self.brightness_callback(self.brightness)
            self.__dimmer_brightness = self.brightness
            if previous_dimmer_brightness < 10:
                return True

        return False

    def dim(self, toggle: bool = False):
        """Manually initiate a dim event.
        If the dimmer is stopped, this has no effect."""

        if self.__stopped:
            return

        if toggle and self.__dimmer_brightness == 0:
            self.reset()
        elif self.__timer and self.__timer.isActive():
            # No need for the timer anymore, stop it
            self.__timer.stop()

            # Verify that we're not already at the target brightness nor
            # busy with dimming already
            if self.__change_timer is None and self.__dimmer_brightness:
                self.change_brightness()

    def change_brightness(self):
        """Move the brightness level down by one and schedule another change_brightness event."""
        if self.__dimmer_brightness and self.__dimmer_brightness >= self.brightness_dimmed:
            self.__dimmer_brightness = self.__dimmer_brightness - 1
            self.brightness_callback(self.__dimmer_brightness)
            self.__change_timer = QTimer()
            self.__change_timer.setSingleShot(True)
            self.__change_timer.timeout.connect(partial(self.change_brightness))
            self.__change_timer.start(10)
        else:
            self.__change_timer = None


dimmers: Dict[str, Dimmer] = {}


class DraggableButton(QtWidgets.QToolButton):
    """A QToolButton that supports drag and drop and swaps the button properties on drop"""

    def __init__(self, parent, ui):
        super(DraggableButton, self).__init__(parent)

        self.setAcceptDrops(True)
        self.ui = ui

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.

        if e.buttons() != Qt.LeftButton:
            return

        dimmers[_deck_id(self.ui)].reset()

        mimedata = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec_(Qt.MoveAction)

    def dropEvent(self, e):  # noqa: N802 - Part of QT signature.
        global selected_button

        self.setStyleSheet(BUTTON_STYLE)
        serial_number = _deck_id(self.ui)
        page = _page(self.ui)

        if e.source():
            # Ignore drag and drop on yourself
            if e.source().index == self.index:
                return

            api.swap_buttons(serial_number, page, e.source().index, self.index)
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
                api.set_button_icon(serial_number, page, self.index, file_name)

        icon = api.get_button_icon_pixmap(serial_number, page, e.source().index)
        if icon:
            e.source().setIcon(icon)

        icon = api.get_button_icon_pixmap(serial_number, page, self.index)
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


def _replace_special_keys(key):
    """Replaces special keywords the user can use with their character equivalent."""
    if key.lower() == "plus":
        return "+"
    if key.lower() == "comma":
        return ","
    if key.lower().startswith("delay"):
        return key.lower()
    return key


def handle_keypress(ui, deck_id: str, key: int, state: bool) -> None:

    # TODO: Handle both key down and key up events in future.
    if state:

        if dimmers[deck_id].reset():
            return

        keyboard = Controller()
        page = api.get_page(deck_id)

        command = api.get_button_command(deck_id, page, key)
        if command:
            try:
                Popen(shlex.split(command))
            except Exception as error:
                print(f"The command '{command}' failed: {error}")

        keys = api.get_button_keys(deck_id, page, key)
        if keys:
            keys = keys.strip().replace(" ", "")
            for section in keys.split(","):
                # Since + and , are used to delimit our section and keys to press,
                # they need to be substituted with keywords.
                section_keys = [_replace_special_keys(key_name) for key_name in section.split("+")]

                # Translate string to enum, or just the string itself if not found
                section_keys = [getattr(Key, key_name.lower(), key_name) for key_name in section_keys]

                for key_name in section_keys:
                    if isinstance(key_name, str) and key_name.startswith("delay"):
                        sleep_time_arg = key_name.split("delay", 1)[1]
                        if sleep_time_arg:
                            try:
                                sleep_time = float(sleep_time_arg)
                            except Exception:
                                print(f"Could not convert sleep time to float '{sleep_time_arg}'")
                                sleep_time = 0
                        else:
                            # default if not specified
                            sleep_time = 0.5

                        if sleep_time:
                            try:
                                time.sleep(sleep_time)
                            except Exception:
                                print(f"Could not sleep with provided sleep time '{sleep_time}'")
                    else:
                        try:
                            keyboard.press(key_name)
                        except Exception:
                            print(f"Could not press key '{key_name}'")

                for key_name in section_keys:
                    if not (isinstance(key_name, str) and key_name.startswith("delay")):
                        try:
                            keyboard.release(key_name)
                        except Exception:
                            print(f"Could not release key '{key_name}'")

        write = api.get_button_write(deck_id, page, key)
        if write:
            try:
                keyboard.type(write)
            except Exception as error:
                print(f"Could not complete the write command: {error}")

        brightness_change = api.get_button_change_brightness(deck_id, page, key)
        if brightness_change:
            try:
                api.change_brightness(deck_id, brightness_change)
                dimmers[deck_id].brightness = api.get_brightness(deck_id)
                dimmers[deck_id].reset()
            except Exception as error:
                print(f"Could not change brightness: {error}")

        switch_page = api.get_button_switch_page(deck_id, page, key)
        if switch_page:
            api.set_page(deck_id, switch_page - 1)
            if _deck_id(ui) == deck_id:
                ui.pages.setCurrentIndex(switch_page - 1)


def _deck_id(ui) -> str:
    """Returns the currently selected Stream Deck serial number

    :param ui: A reference to the ui object
    :type ui: _type_
    :return: The serial number
    :rtype: str
    """
    return ui.device_list.itemData(ui.device_list.currentIndex())


def _page(ui) -> int:
    return ui.pages.currentIndex()


def update_button_text(ui, text: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        if deck_id:
            # There may be no decks attached
            api.set_button_text(deck_id, _page(ui), selected_button.index, text)
            icon = api.get_button_icon_pixmap(deck_id, _page(ui), selected_button.index)
            if icon:
                selected_button.setIcon(icon)


def update_button_command(ui, command: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_command(deck_id, _page(ui), selected_button.index, command)


def update_button_keys(ui, keys: str) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_keys(deck_id, _page(ui), selected_button.index, keys)


def update_button_write(ui) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_write(deck_id, _page(ui), selected_button.index, ui.write.toPlainText())


def update_change_brightness(ui, amount: int) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_change_brightness(deck_id, _page(ui), selected_button.index, amount)


def update_switch_page(ui, page: int) -> None:
    if selected_button:
        deck_id = _deck_id(ui)
        api.set_button_switch_page(deck_id, _page(ui), selected_button.index, page)


def change_page(ui, page: int) -> None:
    global selected_button

    """Change the Stream Deck to the desired page and update
    the on-screen buttons.

    :param ui: Reference to the ui
    :type ui: _type_
    :param page: The page number to switch to
    :type page: int
    """
    selected_button.setChecked(False)

    deck_id = _deck_id(ui)
    if deck_id:
        api.set_page(deck_id, page)
        redraw_buttons(ui)
        dimmers[deck_id].reset()

    reset_button_configuration(ui)


def select_image(window) -> None:
    global last_image_dir
    deck_id = _deck_id(window.ui)
    image = api.get_button_icon(deck_id, _page(window.ui), selected_button.index)
    image_file = ""
    if not image:
        if not last_image_dir:
            image_file = os.path.expanduser("~")
        else:
            image_file = last_image_dir
    file_name = QFileDialog.getOpenFileName(window, "Open Image", image_file, "Image Files (*.png *.jpg *.bmp *.svg *.gif)")[0]
    if file_name:
        last_image_dir = os.path.dirname(file_name)
        deck_id = _deck_id(window.ui)
        api.set_button_icon(deck_id, _page(window.ui), selected_button.index, file_name)
        redraw_buttons(window.ui)


def remove_image(window) -> None:
    deck_id = _deck_id(window.ui)
    image = api.get_button_icon(deck_id, _page(window.ui), selected_button.index)
    if image:
        confirm = QMessageBox(window)
        confirm.setWindowTitle("Remove image")
        confirm.setText("Are you sure you want to remove the image for this button?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setIcon(QMessageBox.Question)
        button = confirm.exec_()
        if button == QMessageBox.Yes:
            api.set_button_icon(deck_id, _page(window.ui), selected_button.index, "")
            redraw_buttons(window.ui)


def redraw_buttons(ui) -> None:
    deck_id = _deck_id(ui)
    current_tab = ui.pages.currentWidget()
    buttons = current_tab.findChildren(QtWidgets.QToolButton)
    for button in buttons:
        icon = api.get_button_icon_pixmap(deck_id, _page(ui), button.index)
        if icon:
            button.setIcon(icon)


def set_brightness(ui, value: int) -> None:
    deck_id = _deck_id(ui)
    api.set_brightness(deck_id, value)
    dimmers[deck_id].brightness = value
    dimmers[deck_id].reset()


def set_brightness_dimmed(ui, value: int, full_brightness: int) -> None:
    deck_id = _deck_id(ui)
    api.set_brightness_dimmed(deck_id, value)
    dimmers[deck_id].brightness_dimmed = int(full_brightness * (value / 100))
    dimmers[deck_id].reset()


def button_clicked(ui, clicked_button, buttons) -> None:
    global selected_button
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)

    deck_id = _deck_id(ui)
    button_id = selected_button.index
    if selected_button.isChecked():
        enable_button_configuration(ui, True)
        ui.text.setText(api.get_button_text(deck_id, _page(ui), button_id))
        ui.command.setText(api.get_button_command(deck_id, _page(ui), button_id))
        ui.keys.setCurrentText(api.get_button_keys(deck_id, _page(ui), button_id))
        ui.write.setPlainText(api.get_button_write(deck_id, _page(ui), button_id))
        ui.change_brightness.setValue(api.get_button_change_brightness(deck_id, _page(ui), button_id))
        ui.switch_page.setValue(api.get_button_switch_page(deck_id, _page(ui), button_id))
        dimmers[deck_id].reset()
    else:
        selected_button = None
        reset_button_configuration(ui)


def enable_button_configuration(ui, enabled: bool):
    ui.text.setEnabled(enabled)
    ui.command.setEnabled(enabled)
    ui.keys.setEnabled(enabled)
    ui.write.setEnabled(enabled)
    ui.change_brightness.setEnabled(enabled)
    ui.switch_page.setEnabled(enabled)
    ui.imageButton.setEnabled(enabled)
    ui.removeButton.setEnabled(enabled)


def reset_button_configuration(ui):
    """Clears the configuration for a button and disables editing of them. This is done when
    there is no key selected or if there are no devices connected.
    """
    ui.text.clear()
    ui.command.clear()
    ui.keys.clearEditText()
    ui.write.clear()
    ui.change_brightness.setValue(0)
    ui.switch_page.setValue(0)
    enable_button_configuration(ui, False)


def browse_documentation():
    url = QUrl("https://timothycrosley.github.io/streamdeck-ui")
    QDesktopServices.openUrl(url)


def browse_github():
    url = QUrl("https://github.com/timothycrosley/streamdeck-ui")
    QDesktopServices.openUrl(url)


def build_buttons(ui, tab) -> None:
    if hasattr(tab, "deck_buttons"):
        tab.deck_buttons.hide()
        tab.deck_buttons.deleteLater()
        # Remove the inner page
        del tab.children()[0]
        # Remove the property
        del tab.deck_buttons

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
            button = DraggableButton(base_widget, ui)
            button.setCheckable(True)
            button.index = index
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            button.setToolButtonStyle(Qt.ToolButtonIconOnly)
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
    file_name = QFileDialog.getSaveFileName(window, "Export Config", os.path.expanduser("~/streamdeck_ui_export.json"), "JSON (*.json)")[0]
    if not file_name:
        return

    api.export_config(file_name)


def import_config(window) -> None:
    file_name = QFileDialog.getOpenFileName(window, "Import Config", os.path.expanduser("~"), "Config Files (*.json)")[0]
    if not file_name:
        return

    api.import_config(file_name)
    redraw_buttons(window.ui)


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
    style = ""
    if ui.device_list.count() > 0:
        style = "background-color: black"

    for page_id in range(ui.pages.count()):
        page = ui.pages.widget(page_id)
        page.setStyleSheet(style)
        build_buttons(ui, page)

    if ui.device_list.count() > 0:
        # Set the active page for this device
        ui.pages.setCurrentIndex(api.get_page(_deck_id(ui)))

        # Draw the buttons for the active page
        redraw_buttons(ui)
    else:
        reset_button_configuration(ui)


class MainWindow(QMainWindow):
    """Represents the main streamdeck-ui configuration Window. A QMainWindow
    object provides a lot of standard main window features out the box.

    The QtCreator UI designer allows you to create a UI quickly. It compiles
    into a class called Ui_MainWindow() and everything comes together by
    calling the setupUi() method and passing a reference to the QMainWindow.

    :param QMainWindow: The parent QMainWindow object
    :type QMainWindow: [type]
    """

    ui : Ui_MainWindow
    "A reference to all the UI objects for the main window"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_shown: bool = True

    def closeEvent(self, event) -> None:  # noqa: N802 - Part of QT signature.
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
        dependencies = ("streamdeck", "pyside2", "pillow", "pynput")
        for dep in dependencies:
            try:
                dist = pkg_resources.get_distribution(dep)
                body.append("{} {}".format(dep, dist.version))
            except pkg_resources.DistributionNotFound:
                pass
        QtWidgets.QMessageBox.about(self, title, "\n".join(body))


def queue_update_button_text(ui, text: str) -> None:
    """Instead of directly updating the text (label) associated with
    the button, add a small delay. If this is called before the
    timer fires, delay it again. Effectively this creates an update
    queue. It makes the textbox more response, as rendering the button
    and saving to the API each time can feel somewhat slow.

    :param ui: Reference to the ui
    :type ui: _type_
    :param text: The new text value
    :type text: str
    """
    global text_update_timer

    if text_update_timer:
        text_update_timer.stop()

    text_update_timer = QTimer()
    text_update_timer.setSingleShot(True)
    text_update_timer.timeout.connect(partial(update_button_text, ui, text))
    text_update_timer.start(500)


def change_brightness(deck_id: str, brightness: int):
    """Changes the brightness of the given streamdeck, but does not save
    the state."""
    api.decks[deck_id].set_brightness(brightness)


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui : Ui_SettingsDialog = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.show()


def show_settings(window : MainWindow) -> None:
    """Shows the settings dialog and allows the user the change deck specific
    settings. Settings are not saved until OK is clicked."""
    ui = window.ui
    deck_id = _deck_id(ui)
    settings = SettingsDialog(window)
    dimmers[deck_id].stop()

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
    if settings.exec_():
        # Commit changes
        if existing_index != settings.ui.dim.currentIndex():
            dimmers[deck_id].timeout = settings.ui.dim.currentData()
            api.set_display_timeout(deck_id, settings.ui.dim.currentData())
        set_brightness(window.ui, settings.ui.brightness.value())
        set_brightness_dimmed(window.ui, settings.ui.brightness_dimmed.value(), settings.ui.brightness.value())
    else:
        # User cancelled, reset to original brightness
        change_brightness(deck_id, api.get_brightness(deck_id))

    dimmers[deck_id].reset()


def disable_dim_settings(settings: SettingsDialog, _index: int) -> None:
    disable = dimmer_options.get(settings.ui.dim.currentText()) == 0
    settings.ui.brightness_dimmed.setDisabled(disable)
    settings.ui.label_brightness_dimmed.setDisabled(disable)


def dim_all_displays() -> None:
    for _deck_id, dimmer in dimmers.items():
        dimmer.dim(True)


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
    ui.switch_page.valueChanged.connect(partial(update_switch_page, ui))
    ui.imageButton.clicked.connect(partial(select_image, main_window))
    ui.removeButton.clicked.connect(partial(remove_image, main_window))
    ui.settingsButton.clicked.connect(partial(show_settings, main_window))
    ui.actionExport.triggered.connect(partial(export_config, main_window))
    ui.actionImport.triggered.connect(partial(import_config, main_window))
    ui.actionExit.triggered.connect(app.exit)
    ui.actionAbout.triggered.connect(main_window.about_dialog)
    ui.actionDocs.triggered.connect(browse_documentation)
    ui.actionGithub.triggered.connect(browse_github)
    enable_button_configuration(ui, False)
    return main_window


def create_tray(logo: QIcon, app: QApplication, main_window: QMainWindow) -> QSystemTrayIcon:
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
    tray.activated.connect(main_window.systray_clicked)

    menu = QMenu()
    action_dim = QAction("Dim display (toggle)", main_window)
    action_dim.triggered.connect(dim_all_displays)
    action_configure = QAction("Configure...", main_window)
    action_configure.triggered.connect(main_window.bring_to_top)
    menu.addAction(action_dim)
    menu.addAction(action_configure)
    menu.addSeparator()
    action_exit = QAction("Exit", main_window)
    action_exit.triggered.connect(app.exit)
    menu.addAction(action_exit)
    tray.setContextMenu(menu)
    return tray


def streamdeck_cpu_changed(ui, serial_number: str, cpu: int):
    if (cpu > 100):
        cpu == 100
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
        # REVIEW: Does dimmer belong in UI layer? Seems like API logic.
    dimmers[serial_number] = Dimmer(
        api.get_display_timeout(serial_number),
        api.get_brightness(serial_number),
        api.get_brightness_dimmed(serial_number),
        partial(change_brightness, serial_number),
    )
    dimmers[serial_number].reset()
    build_device(ui)


def streamdeck_detatched(ui, serial_number):
    index = ui.device_list.findData(serial_number)
    if index != -1:
        # Should not be (how can you remove a device that was never attached?)
        # Check anyways
        dimmer = dimmers[serial_number]
        dimmer.stop()
        del dimmers[serial_number]
        ui.device_list.removeItem(index)


def start(_exit: bool = False) -> None:
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
        version = pkg_resources.get_distribution("streamdeck_ui").version
    except pkg_resources.DistributionNotFound:
        version = "devel"

    # The QApplication object holds the Qt event loop and you need one of these
    # for your application
    app = QApplication(sys.argv)
    app.setApplicationName("Streamdeck UI")
    app.setApplicationVersion(version)
    logo = QIcon(LOGO)
    app.setWindowIcon(logo)
    main_window = create_main_window(logo, app)
    ui = main_window.ui
    tray = create_tray(logo, app, main_window)

    api.streamdeck_keys.key_pressed.connect(partial(handle_keypress, ui))

    ui.device_list.currentIndexChanged.connect(partial(build_device, ui))
    ui.pages.currentChanged.connect(partial(change_page, ui))

    api.plugevents.attached.connect(partial(streamdeck_attached, ui))
    api.plugevents.detatched.connect(partial(streamdeck_detatched, ui))
    api.plugevents.cpu_changed.connect(partial(streamdeck_cpu_changed, ui))
    api.start()

    tray.show()
    if show_ui:
        main_window.show()

    if _exit:
        return
    else:
        app.exec_()
        api.stop()
        sys.exit()


if __name__ == "__main__":
    start()
