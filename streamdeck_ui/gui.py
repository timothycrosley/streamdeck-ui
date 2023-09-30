"""Defines the QT powered interface for configuring Stream Decks"""
import os
import shlex
import signal
import sys
from functools import partial
from subprocess import Popen  # nosec - Need to allow users to specify arbitrary commands
from typing import Dict, List, Optional, Union

from importlib_metadata import PackageNotFoundError, version
from PySide6.QtCore import QMimeData, QSettings, QSignalBlocker, QSize, Qt, QTimer, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QDrag, QFont, QIcon, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QDialog,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QSystemTrayIcon,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.cli.server import CLIStreamDeckServer
from streamdeck_ui.config import (
    APP_LOGO,
    APP_NAME,
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_FONT_COLOR,
    DEFAULT_FONT_FALLBACK_PATH,
    DEFAULT_FONT_SIZE,
    STATE_FILE,
    STATE_FILE_BACKUP,
    config_file_need_migration,
    do_config_file_migration,
)
from streamdeck_ui.display.text_filter import is_a_valid_text_filter_font
from streamdeck_ui.modules.fonts import DEFAULT_FONT_FAMILY, FONTS_DICT, find_font_info
from streamdeck_ui.modules.keyboard import Keyboard, pynput_supported
from streamdeck_ui.modules.utils.timers import debounce
from streamdeck_ui.semaphore import Semaphore, SemaphoreAcquireError
from streamdeck_ui.ui_button import Ui_ButtonForm
from streamdeck_ui.ui_main import Ui_MainWindow
from streamdeck_ui.ui_settings import Ui_SettingsDialog

# this ignore is just a workaround to set api with something
# and be able to test
api: StreamDeckServer = StreamDeckServer()

main_window: "MainWindow"
"Reference to the main window, used across multiple functions"

last_image_dir: str = ""
"Stores the last direction where user selected an image from"

selected_button: Optional[QToolButton] = None
"A reference to the currently selected button"

text_update_timer: Optional[QTimer] = None
"Timer used to delay updates to the button text"

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


class DraggableButton(QToolButton):
    """A QToolButton that supports drag and drop and swaps the button properties on drop"""

    def __init__(self, parent, ui, api_: StreamDeckServer):
        super(DraggableButton, self).__init__(parent)

        self.setAcceptDrops(True)
        self.ui = ui
        self.api = api_

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.
        if e.buttons() != Qt.LeftButton:
            return

        self.api.reset_dimmer(_deck())

        mime_data = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.MoveAction)

    def dropEvent(self, e):  # noqa: N802 - Part of QT signature.
        global selected_button

        self.setStyleSheet(BUTTON_STYLE)
        deck_id = _deck()
        page_id = _page()

        index = self.property("index")
        if e.source():
            source_index = e.source().property("index")
            # Ignore drag and drop on yourself
            if source_index == index:
                return

            self.api.swap_buttons(deck_id, page_id, source_index, index)
            # In the case that we've dragged the currently selected button, we have to
            # check the target button instead, so it appears that it followed the drag/drop
            if e.source().isChecked():
                e.source().setChecked(False)
                self.setChecked(True)
                selected_button = self
        else:
            # Handle drag and drop from outside the application
            if e.mimeData().hasUrls:
                file_name = e.mimeData().urls()[0].toLocalFile()
                self.api.set_button_icon(deck_id, page_id, index, file_name)

        if e.source():
            source_index = e.source().property("index")
            icon = self.api.get_button_icon_pixmap(deck_id, page_id, source_index)
            if icon:
                e.source().setIcon(icon)

        icon = self.api.get_button_icon_pixmap(deck_id, page_id, index)
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
            if _deck() == deck_id:
                ui.pages.setCurrentIndex(switch_page - 1)

        switch_state = api.get_button_switch_state(deck_id, page, key)
        if switch_state:
            api.set_button_state(deck_id, page, key, switch_state - 1)
            if _deck() == deck_id:
                if _button() == key:
                    ui.button_states.setCurrentIndex(switch_state - 1)
                redraw_button(key)


def _deck() -> Optional[str]:
    """Returns the currently selected Stream Deck serial number"""
    if main_window.ui.device_list.count() == 0:
        return None
    return main_window.ui.device_list.itemData(main_window.ui.device_list.currentIndex())


def _page() -> Optional[int]:
    """Returns the currently selected page index"""
    tab_index = main_window.ui.pages.currentIndex()
    page = main_window.ui.pages.widget(tab_index)
    if page is None:
        return None
    return page.property("page_id")


def _button() -> Optional[int]:
    """Returns the currently selected button index"""
    if selected_button is None:
        return None
    index = selected_button.property("index")

    if index < 0:
        return None

    return index


def _button_state() -> Optional[int]:
    """Returns the currently selected button state index"""
    tab_index = main_window.ui.button_states.currentIndex()
    state = main_window.ui.button_states.widget(tab_index)
    return state.property("button_state_id")


def handle_change_page() -> None:
    """Change the Stream Deck to the desired page and update
    the on-screen buttons.
    """
    global selected_button

    if selected_button:
        selected_button.setChecked(False)
        selected_button = None

    deck_id = _deck()
    page_id = _page()
    if deck_id is not None and page_id is not None:
        api.set_page(deck_id, page_id)
        redraw_buttons()
        api.reset_dimmer(deck_id)
    build_button_state_pages()


def handle_change_button_state() -> None:
    """Change the Stream Deck to the desired button state and update
    the on-screen buttons.
    """
    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    button_state_id = _button_state()
    if deck_id is not None and page_id is not None and button_id is not None and button_state_id is not None:
        api.set_button_state(deck_id, page_id, button_id, button_state_id)
        redraw_button(button_id)
        api.reset_dimmer(deck_id)


def handle_new_page() -> None:
    deck_id = _deck()
    if not deck_id:
        return

    # Add the new page to the api
    new_page_index = api.add_new_page(deck_id)
    build_device(main_window.ui)

    # look for the new page in the ui
    for page in range(main_window.ui.pages.count()):
        if main_window.ui.pages.widget(page).property("page_id") == new_page_index:
            main_window.ui.pages.setCurrentIndex(page)
            break
    main_window.ui.remove_page.setEnabled(True)


def handle_delete_page_with_confirmation() -> None:
    confirm = QMessageBox(main_window)
    confirm.setWindowTitle("Delete Page")
    confirm.setText("Are you sure you want to delete this page?")
    confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirm.setIcon(QMessageBox.Icon.Question)
    button = confirm.exec()
    if button == QMessageBox.StandardButton.Yes:
        handle_delete_page()


def handle_delete_page() -> None:
    deck_id = _deck()
    page_id = _page()
    if deck_id is None or page_id is None:
        return

    pages = api.get_pages(deck_id)
    if len(pages) == 1:
        return

    new_page = _closest_page(page_id, pages)
    tab_index_to_move = -1
    tab_index_to_remove = -1
    for tab_index in range(main_window.ui.pages.count()):
        tab = main_window.ui.pages.widget(tab_index)
        if tab.property("page_id") == new_page:
            tab_index_to_move = tab_index
        if tab.property("page_id") == page_id:
            tab_index_to_remove = tab_index

    main_window.ui.pages.setCurrentIndex(tab_index_to_move)
    api.remove_page(deck_id, page_id)
    main_window.ui.pages.removeTab(tab_index_to_remove)
    if main_window.ui.pages.count() == 1:
        main_window.ui.remove_page.setEnabled(False)


def handle_new_button_state() -> None:
    deck_id = _deck()
    page_id = _page()
    button_id = _button()

    if deck_id is None or page_id is None or button_id is None:
        return

    new_button_state_index = api.add_new_button_state(deck_id, page_id, button_id)
    build_button_state_pages()

    for button_state in range(main_window.ui.button_states.count()):
        if main_window.ui.button_states.widget(button_state).property("button_state_id") == new_button_state_index:
            main_window.ui.button_states.setCurrentIndex(button_state)
            break
    main_window.ui.remove_button_state.setEnabled(True)


def handle_delete_button_state_with_confirmation() -> None:
    confirm = QMessageBox(main_window)
    confirm.setWindowTitle("Delete Button State")
    confirm.setText("Are you sure you want to delete this button state?")
    confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirm.setIcon(QMessageBox.Icon.Question)
    button = confirm.exec()
    if button == QMessageBox.StandardButton.Yes:
        handle_delete_button_state()


def handle_delete_button_state() -> None:
    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    button_state_id = _button_state()
    if deck_id is None or page_id is None or button_id is None or button_state_id is None:
        return

    api.remove_button_state(deck_id, page_id, button_id, button_state_id)
    main_window.ui.button_states.removeTab(main_window.ui.button_states.currentIndex())
    if main_window.ui.button_states.count() == 1:
        main_window.ui.remove_button_state.setEnabled(False)


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


def redraw_buttons() -> None:
    deck_id = _deck()
    page_id = _page()
    if deck_id is None or page_id is None:
        return
    current_tab = main_window.ui.pages.currentWidget()
    buttons = current_tab.findChildren(QToolButton)
    for button in buttons:
        if not button.isHidden():
            # When rebuilding the buttons, we hide the old ones
            # and mark for deletion. They still hang around so
            # ignore them here
            icon = api.get_button_icon_pixmap(deck_id, page_id, button.property("index"))
            if icon is not None:
                button.setIcon(icon)


def redraw_button(button_index: int) -> None:
    deck_id = _deck()
    page_id = _page()
    if deck_id is None or page_id is None:
        return

    current_tab = main_window.ui.pages.currentWidget()
    buttons = current_tab.findChildren(QToolButton)
    for button in buttons:
        if not button.isHidden():
            if button.property("index") == button_index:
                icon = api.get_button_icon_pixmap(deck_id, page_id, button.property("index"))
                if icon is not None:
                    button.setIcon(icon)


def set_brightness(value: int) -> None:
    deck_id = _deck()
    if deck_id is None:
        return
    api.set_brightness(deck_id, value)


def set_brightness_dimmed(value: int) -> None:
    deck_id = _deck()
    if deck_id is None:
        return
    api.set_brightness_dimmed(deck_id, value)
    api.reset_dimmer(deck_id)


def button_clicked(clicked_button, buttons) -> None:
    """This method build the button states tabs user interface.
    It is called when a button is clicked on the main page."""
    global selected_button
    selected_button = clicked_button

    # uncheck all other buttons
    for button in buttons:
        if button == clicked_button:
            continue
        button.setChecked(False)
    # if no button is selected, do nothing
    if selected_button is None:
        return
    if not selected_button.isChecked():
        selected_button = None
        return

    deck_id = _deck()
    if deck_id is not None:
        api.reset_dimmer(deck_id)
    build_button_state_pages()


def build_button_state_pages():
    ui = main_window.ui
    blocker = QSignalBlocker(ui.button_states)
    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    active_tab_index = 0

    try:
        if ui.button_states.count() > 0:
            ui.button_states.clear()

        if button_id is not None and deck_id is not None and page_id is not None:
            current_state = api.get_button_state(deck_id, page_id, button_id)

            for button_state_id in api.get_button_states(deck_id, page_id, button_id):
                page = QWidget()
                page.setLayout(QVBoxLayout())
                page.setProperty("deck_id", deck_id)
                page.setProperty("page_id", page_id)
                page.setProperty("button_id", button_id)
                page.setProperty("button_state_id", button_state_id)
                label = _build_tab_label("State", button_state_id)
                tab_index = ui.button_states.addTab(page, label)
                page_tab = ui.button_states.widget(tab_index)
                build_button_state_form(page_tab)
                if button_state_id == current_state:
                    active_tab_index = tab_index
        else:
            # add text "No button selected"
            page = QWidget()
            page.setLayout(QVBoxLayout())
            page.setProperty("deck_id", deck_id)
            page.setProperty("page_id", page_id)
            page.setProperty("button_id", button_id)
            page.setProperty("button_state_id", None)
            label = _build_tab_label("State", 0)
            tab_index = ui.button_states.addTab(page, label)
            page_tab = ui.button_states.widget(tab_index)
            build_button_state_form(page_tab)

        some_state = button_id is not None and ui.button_states.count() > 0
        more_than_one_state = button_id is not None and ui.button_states.count() > 1

        ui.remove_button_state.setEnabled(more_than_one_state)

        if some_state:
            ui.button_states.setCurrentIndex(active_tab_index)
            ui.add_button_state.setEnabled(True)
            redraw_button(button_id)
        else:
            ui.add_button_state.setEnabled(False)
    finally:
        blocker.unblock()


def build_button_state_form(tab) -> None:
    global selected_button
    global main_window

    if hasattr(tab, "button_form"):
        for widget in tab.findChildren(QWidget):
            widget.hide()
            widget.deleteLater()

        tab.button_form.hide()
        tab.button_form.deleteLater()
        del tab.children()[0]
        del tab.button_form

    base_widget = QWidget(tab)
    tab.children()[0].addWidget(base_widget)

    tab.button_form = base_widget

    tab_ui = Ui_ButtonForm()
    tab_ui.setupUi(base_widget)

    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    button_state_id = tab.property("button_state_id")

    # set values
    # reset the button configuration to the default
    _reset_build_button_state_form(tab_ui)

    if deck_id is None or page_id is None or button_id is None or button_state_id is None:
        enable_button_configuration(tab_ui, False)
        return

    enable_button_configuration(tab_ui, True)
    button_state = api.get_button_state_object(deck_id, page_id, button_id, button_state_id)

    tab_ui.text.setText(button_state.text)
    tab_ui.command.setText(button_state.command)
    tab_ui.keys.setCurrentText(button_state.keys)
    tab_ui.write.setPlainText(button_state.write)
    tab_ui.change_brightness.setValue(button_state.brightness_change)
    tab_ui.text_font_size.setValue(button_state.font_size or DEFAULT_FONT_SIZE)
    tab_ui.text_color.setPalette(QPalette(button_state.font_color or DEFAULT_FONT_COLOR))
    tab_ui.background_color.setPalette(QPalette(button_state.background_color or DEFAULT_BACKGROUND_COLOR))
    tab_ui.change_brightness.setValue(button_state.brightness_change)
    tab_ui.switch_page.setValue(button_state.switch_page)
    tab_ui.switch_state.setValue(button_state.switch_state)

    font_family, font_style = find_font_info(button_state.font or DEFAULT_FONT_FALLBACK_PATH)
    prepare_button_state_form_text_font_list(tab_ui, font_family)
    prepare_button_state_form_text_font_style_list(tab_ui, font_family, font_style)

    # connect signals
    tab_ui.text.textChanged.connect(partial(debounced_update_button_text, tab_ui))
    tab_ui.command.textChanged.connect(partial(debounced_update_button_attribute, "command"))
    tab_ui.keys.currentTextChanged.connect(partial(debounced_update_button_attribute, "keys"))
    tab_ui.write.textChanged.connect(lambda: debounced_update_button_attribute("write", tab_ui.write.toPlainText()))
    tab_ui.change_brightness.valueChanged.connect(partial(update_button_attribute, "change_brightness"))
    tab_ui.text_font_size.valueChanged.connect(partial(update_displayed_button_attribute, "font_size"))
    tab_ui.text_font.currentTextChanged.connect(lambda: update_button_attribute_font(tab_ui, "family"))
    tab_ui.text_font_style.currentTextChanged.connect(lambda: update_button_attribute_font(tab_ui, "style"))
    tab_ui.text_color.clicked.connect(partial(show_button_state_font_color_dialog, tab_ui))
    tab_ui.background_color.clicked.connect(partial(show_button_state_background_color_dialog, tab_ui))
    tab_ui.switch_page.valueChanged.connect(partial(update_button_attribute, "switch_page"))
    tab_ui.switch_state.valueChanged.connect(partial(update_button_attribute, "switch_state"))
    tab_ui.add_image.clicked.connect(partial(show_button_state_image_dialog))
    tab_ui.remove_image.clicked.connect(show_button_state_remove_image_dialog)
    tab_ui.text_h_align.clicked.connect(partial(update_align_text_horizontal))
    tab_ui.text_v_align.clicked.connect(partial(update_align_text_vertical))


def enable_button_configuration(ui: Ui_ButtonForm, enabled: bool):
    ui.text.setEnabled(enabled)
    ui.command.setEnabled(enabled)
    ui.keys.setEnabled(enabled)
    ui.text_font.setEnabled(enabled)
    ui.text_font_style.setEnabled(enabled)
    ui.text_font_size.setEnabled(enabled)
    ui.write.setEnabled(enabled)
    ui.change_brightness.setEnabled(enabled)
    ui.switch_page.setEnabled(enabled)
    ui.switch_state.setEnabled(enabled)
    ui.add_image.setEnabled(enabled)
    ui.remove_image.setEnabled(enabled)
    ui.text_h_align.setEnabled(enabled)
    ui.text_v_align.setEnabled(enabled)
    ui.text_color.setEnabled(enabled)
    ui.background_color.setEnabled(enabled)
    # default black color looks like it's enabled even when it's not
    # we set it to white when disabled to make it more obvious
    if enabled:
        ui.background_color.setPalette(QPalette(DEFAULT_BACKGROUND_COLOR))
    else:
        ui.background_color.setPalette(QPalette(DEFAULT_FONT_COLOR))
    # fields that depends on pynput be supported
    ui.label_5.setVisible(pynput_supported)
    ui.keys.setVisible(pynput_supported)
    ui.label_6.setVisible(pynput_supported)
    ui.write.setVisible(pynput_supported)


def prepare_button_state_form_text_font_list(ui: Ui_ButtonForm, current_font_family: str) -> None:
    """Prepares the font selection combo box with all available fonts"""
    blocker = QSignalBlocker(ui.text_font)
    try:
        ui.text_font.clear()
        ui.text_font.clearEditText()
        for i, font_family in enumerate(FONTS_DICT):
            ui.text_font.addItem(font_family)
            font = QFont(font_family)
            ui.text_font.setItemData(i, font)
            ui.text_font.setItemData(i, font, Qt.FontRole)  # type: ignore [attr-defined]
        ui.text_font.setCurrentText(current_font_family)
    finally:
        blocker.unblock()


def prepare_button_state_form_text_font_style_list(
    ui: Ui_ButtonForm, current_font_family: str, current_font_style: str
) -> None:
    """Prepares the font style selection combo box with all available styles for the selected font"""
    blocker = QSignalBlocker(ui.text_font_style)
    try:
        ui.text_font_style.clear()
        ui.text_font_style.clearEditText()
        for _i, font_style in enumerate(FONTS_DICT[current_font_family]):
            ui.text_font_style.addItem(font_style)
        if current_font_style:
            ui.text_font_style.setCurrentText(current_font_style)
    finally:
        blocker.unblock()


def show_button_state_font_color_dialog(ui: Ui_ButtonForm) -> None:
    current_color = ui.text_color.palette().color(QPalette.ColorRole.Button)
    color = QColorDialog.getColor(current_color, ui.text_color, "Select text color")

    if color.isValid():
        ui.text_color.setPalette(QPalette(color))
        color_hex = color.name()
        update_displayed_button_attribute("font_color", color_hex)


def show_button_state_background_color_dialog(ui: Ui_ButtonForm) -> None:
    current_color = ui.background_color.palette().color(QPalette.ColorRole.Button)
    color = QColorDialog.getColor(current_color, ui.background_color, "Select background color")

    if color.isValid():
        ui.background_color.setPalette(QPalette(color))
        color_hex = color.name()
        update_displayed_button_attribute("background_color", color_hex)


def show_button_state_image_dialog() -> None:
    global last_image_dir
    deck_id = _deck()
    page_id = _page()
    button_id = _button()

    if deck_id is None or page_id is None or button_id is None:
        return

    image_file = api.get_button_icon(deck_id, page_id, button_id)

    if not image_file:
        if not last_image_dir:
            image_file = os.path.expanduser("~")
        else:
            image_file = last_image_dir

    file_name = QFileDialog.getOpenFileName(
        main_window, "Open Image", image_file, "Image Files (*.png *.jpg *.bmp *.svg *.gif)"
    )[0]

    if file_name:
        last_image_dir = os.path.dirname(file_name)
        update_displayed_button_attribute("icon", file_name)


def show_button_state_remove_image_dialog() -> None:
    deck_id = _deck()
    page_id = _page()
    button_id = _button()

    if deck_id is None or page_id is None or button_id is None:
        return

    image = api.get_button_icon(deck_id, page_id, button_id)
    if image:
        confirm = QMessageBox(main_window)
        confirm.setWindowTitle("Remove image")
        confirm.setText("Are you sure you want to remove the image for this button?")
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm.setIcon(QMessageBox.Icon.Question)
        button = confirm.exec()
        if button == QMessageBox.StandardButton.Yes:
            update_displayed_button_attribute("icon", "")


def update_align_text_vertical() -> None:
    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    align_changes = {
        "": "middle-bottom",
        "bottom": "middle-bottom",
        "middle-bottom": "middle",
        "middle": "middle-top",
        "middle-top": "top",
    }
    if deck_id is not None and page_id is not None and button_id is not None:
        current_position = api.get_button_text_vertical_align(deck_id, page_id, button_id)
        next_position = align_changes.get(current_position, "")
        update_displayed_button_attribute("text_vertical_align", next_position)


def update_align_text_horizontal() -> None:
    deck_id = _deck()
    page_id = _page()
    button_id = _button()
    align_changes = {
        "": "left",
        "left": "right",
        "center": "left",
    }
    if deck_id is not None and page_id is not None and button_id is not None:
        current_position = api.get_button_text_vertical_align(deck_id, page_id, button_id)
        next_position = align_changes.get(current_position, "")
        update_displayed_button_attribute("text_horizontal_align", next_position)


@debounce(timeout=500)
def debounced_update_button_text(ui: Ui_ButtonForm) -> None:
    """Instead of directly updating the text (label) associated with
    the button, add a small delay. If this is called before the
    timer fires, delay it again. Effectively this creates an update
    queue. It makes the textbox more response, as rendering the button
    and saving to the API each time can feel somewhat slow.
    """
    text = ui.text.toPlainText()
    update_displayed_button_attribute("text", text)


@debounce(timeout=500)
def debounced_update_button_attribute(attribute: str, value: str) -> None:
    """Instead of directly updating the attribute associated with
    the button, add a small delay. If this is called before the
    timer fires, delay it again. Effectively this creates an update
    queue. It makes the textbox more response, as rendering the button
    and saving to the API each time can feel somewhat slow.
    """
    update_button_attribute(attribute, value)


def update_button_attribute_font(ui: Ui_ButtonForm, kind: str) -> None:
    """Update the font associated with the button"""
    font_family = ui.text_font.currentText()
    font_style = ui.text_font_style.currentText()
    # when the font family changes, update the font style list
    if kind == "family":
        prepare_button_state_form_text_font_style_list(ui, font_family, "")
        font_style = list(FONTS_DICT[font_family])[0]

    font = FONTS_DICT[font_family][font_style]

    # if the font is not valid, we roll back the change to current value
    # in case rollback fails, we set the default font
    if is_a_valid_text_filter_font(font):
        update_displayed_button_attribute("font", font)
    else:
        deck_id = _deck()
        page_id = _page()
        button_id = _button()
        if deck_id is not None and page_id is not None and button_id is not None:
            current_font = api.get_button_font(deck_id, page_id, button_id)
            font_family, _ = find_font_info(current_font)
            ui.text_font.setCurrentText(font_family)
        else:
            ui.text_font.setCurrentText(DEFAULT_FONT_FAMILY)


def _reset_build_button_state_form(ui: Ui_ButtonForm):
    """Clears the configuration for a button and disables editing of them."""
    ui.text.clear()
    ui.command.clear()
    ui.keys.clearEditText()
    ui.text_font.clearEditText()
    ui.text_font_size.setValue(0)
    # ui.text_font.setCurrentIndex(-1)
    # ui.text_font_style.setCurrentIndex(-1)
    ui.text_color.setPalette(QPalette(DEFAULT_FONT_COLOR))
    ui.background_color.setPalette(QPalette(DEFAULT_BACKGROUND_COLOR))
    ui.write.clear()
    ui.change_brightness.setValue(0)
    ui.switch_page.setValue(0)
    ui.switch_state.setValue(0)


def browse_documentation():
    url = QUrl("https://streamdeck-linux-gui.github.io/streamdeck-linux-gui/")
    QDesktopServices.openUrl(url)


def browse_github():
    url = QUrl("https://github.com/streamdeck-linux-gui/streamdeck-linux-gui")
    QDesktopServices.openUrl(url)


def build_buttons(ui, tab) -> None:
    global selected_button

    if hasattr(tab, "deck_buttons"):
        buttons = tab.findChildren(QToolButton)
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

    deck_id = _deck()

    if not deck_id:
        return
    deck_rows, deck_columns = api.get_deck_layout(deck_id)

    # Create a new base_widget with tab as it's parent
    # This is effectively a "blank tab"
    base_widget = QWidget(tab)

    # Add an inner page (QtWidget) to the page
    tab.children()[0].addWidget(base_widget)

    # Set a property - this allows us to check later
    # if we've already created the buttons
    tab.deck_buttons = base_widget

    row_layout = QVBoxLayout(base_widget)
    index = 0
    buttons = []
    for _row in range(deck_rows):
        column_layout = QHBoxLayout()
        row_layout.addLayout(column_layout)

        for _column in range(deck_columns):
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
        button.clicked.connect(
            lambda current_button=button, all_buttons=buttons: button_clicked(current_button, all_buttons)
        )


def export_config(window, api) -> None:
    file_name = QFileDialog.getSaveFileName(
        window, "Export Config", os.path.expanduser("~/streamdeck_ui_export.json"), "JSON (*.json)"
    )[0]
    if not file_name:
        return

    api.export_config(file_name)


def import_config(window, api) -> None:
    file_name = QFileDialog.getOpenFileName(window, "Import Config", os.path.expanduser("~"), "Config Files (*.json)")[
        0
    ]
    if not file_name:
        return

    api.import_config(file_name)
    redraw_buttons()


def _build_tab_label(prefix: str, page_id: int) -> str:
    return f"{prefix} {page_id + 1}" if page_id == 0 else f"{page_id + 1}"


def build_device(ui, _device_index=None) -> None:
    """This method builds the device configuration user interface.
    It is called if you switch to a different Stream Deck,
    a Stream Deck is added or when the last one is removed.
    It must deal with the case where there is no Stream Deck as
    a result.
    """
    blocker = QSignalBlocker(ui.pages)
    try:
        deck_id = _deck()
        style = DEVICE_PAGE_STYLE if ui.device_list.count() > 0 else ""

        # the device was removed while we were building the ui, then we skip
        if deck_id is None:
            return

        # clear the pages
        if ui.pages.count() > 0:
            ui.pages.clear()

        current_page = api.get_page(deck_id)
        active_tab_index = 0

        # Add the pages
        for page_id in api.get_pages(deck_id):
            page = QWidget()
            page.setLayout(QGridLayout())
            page.setProperty("deck_id", deck_id)
            page.setProperty("page_id", page_id)
            page.setStyleSheet(style)
            label = _build_tab_label("Page", page_id)
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
            redraw_buttons()
        else:
            ui.settingsButton.setEnabled(False)
            ui.add_page.setEnabled(False)
    finally:
        blocker.unblock()


class MainWindow(QMainWindow):
    """Represents the main streamdeck-ui configuration Window. A QMainWindow
    object provides a lot of standard main window features out the box.

    The QtCreator UI designer allows you to create a UI quickly. It compiles
    into a class called Ui_MainWindow() and everything comes together by
    calling the setupUi() method and passing a reference to the QMainWindow.
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
        if status is QSystemTrayIcon.ActivationReason.Context:
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
                dist_version = version(dep)
                body.append("{} {}".format(dep, dist_version))
            except PackageNotFoundError:
                pass
        QMessageBox.about(self, title, "\n".join(body))


def update_displayed_button_attribute(attribute: str, value: Union[str, int]) -> None:
    """Updates the given attribute for the currently selected button.
    and updates the icon of the current selected button."""
    updated = update_button_attribute(attribute, value)

    if not updated:
        return

    deck_id = _deck()
    page_id = _page()
    button_id = _button()

    if deck_id is None or page_id is None or button_id is None:
        return

    icon = api.get_button_icon_pixmap(deck_id, page_id, button_id)
    if icon is not None and selected_button is not None:
        selected_button.setIcon(icon)


def update_button_attribute(attribute: str, value: Union[str, int]) -> bool:
    """
    Updates the given attribute for the currently selected button.
    and updates the icon of the current selected button.
    """
    deck_id = _deck()
    page_id = _page()
    button_id = _button()

    if deck_id is None or page_id is None or button_id is None:
        return False

    update_function = getattr(api, f"set_button_{attribute}")
    update_function(deck_id, page_id, button_id, value)

    return True


def change_brightness(deck_id: str, brightness: int):
    """Changes the brightness of the given streamdeck, but does not save
    the state."""
    api.decks_by_serial[deck_id].set_brightness(brightness)


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
    deck_id = _deck()

    if deck_id is None:
        return

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
        if existing_index != settings.ui.dim.currentIndex():
            api.set_display_timeout(deck_id, settings.ui.dim.currentData())
        set_brightness(settings.ui.brightness.value())
        set_brightness_dimmed(settings.ui.brightness_dimmed.value())
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


def create_main_window(api: StreamDeckServer, app: QApplication) -> MainWindow:
    """Creates the main application window and configures slots and signals"""
    global main_window

    main_window = MainWindow()
    ui = main_window.ui

    ui.settingsButton.clicked.connect(partial(show_settings, main_window))
    ui.add_page.clicked.connect(handle_new_page)
    ui.remove_page.clicked.connect(handle_delete_page_with_confirmation)
    ui.add_button_state.clicked.connect(handle_new_button_state)
    ui.add_button_state.setEnabled(False)
    ui.remove_button_state.clicked.connect(handle_delete_button_state_with_confirmation)
    ui.remove_button_state.setEnabled(False)
    ui.actionExport.triggered.connect(partial(export_config, main_window, api))
    ui.actionImport.triggered.connect(partial(import_config, main_window, api))
    ui.actionExit.triggered.connect(app.exit)
    ui.actionAbout.triggered.connect(main_window.about_dialog)
    ui.actionDocs.triggered.connect(browse_documentation)
    ui.actionGithub.triggered.connect(browse_github)
    ui.settingsButton.setEnabled(False)
    ui.button_states.clear()
    build_button_state_pages()

    ui = main_window.ui
    # allow call redraw_button from ui instance
    ui.redraw_button = redraw_button  # type: ignore [attr-defined]

    api.streamdeck_keys.key_pressed.connect(partial(handle_keypress, ui))

    ui.device_list.currentIndexChanged.connect(partial(build_device, ui))
    ui.pages.currentChanged.connect(lambda: handle_change_page())
    ui.button_states.currentChanged.connect(lambda: handle_change_button_state())
    api.plugevents.attached.connect(partial(streamdeck_attached, ui))
    api.plugevents.detached.connect(partial(streamdeck_detached, ui))
    api.plugevents.cpu_changed.connect(partial(streamdeck_cpu_changed, ui))

    return main_window


def show_migration_config_warning_and_check(app: QApplication) -> None:
    """Shows a warning dialog when a different configuration version is detected.
    If the user confirms the migration, the configuration is migrated and the
    application continues. Otherwise, the application exits."""
    if not config_file_need_migration(STATE_FILE):
        return

    confirm = QMessageBox(main_window)
    confirm.setWindowTitle("Old configuration detected")
    confirm.setText(
        "The configuration file format has changed. \n"
        "Do you want to upgrade your configuration to the new format?\n\n"
        f"If you confirm a copy of your current configuration will be created in {STATE_FILE_BACKUP}\n"
        "Otherwise the application will exit."
    )
    confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirm.setIcon(QMessageBox.Icon.Warning)
    button = confirm.exec()

    if button == QMessageBox.StandardButton.No:
        app.quit()
        sys.exit()

    if button == QMessageBox.StandardButton.Yes:
        do_config_file_migration()


def create_tray(logo: QIcon, app: QApplication) -> QSystemTrayIcon:
    """Creates a system tray with the provided icon and parent. The main
    window passed will be activated when clicked.
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
    if _deck() == serial_number:
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


def configure_signals(app: QApplication):
    """Configures the termination signals for the application."""
    # Configure signal handlers
    # https://stackoverflow.com/a/4939113/192815
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)  # type: ignore [attr-defined] # Let interpreter run to handle signal

    # Handle SIGTERM so we release semaphore and shutdown API gracefully
    signal.signal(signal.SIGTERM, partial(sigterm_handler, app))

    # Handle <ctrl+c>
    signal.signal(signal.SIGINT, partial(sigterm_handler, app))


def sigterm_handler(app, signal_value, frame):
    print("Received signal", signal_value, frame)
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
    global main_window
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
        app_version = version("streamdeck-linux-gui")
    except PackageNotFoundError:
        app_version = "devel"

    try:
        with Semaphore("/tmp/streamdeck_ui.lock"):  # nosec - this file is only observed with advisory lock
            # The semaphore was created, so this is the first instance

            # The QApplication object holds the Qt event loop, and you need one of these
            # for your application
            app = QApplication(sys.argv)
            app.setApplicationName(APP_NAME)
            app.setApplicationVersion(app_version)
            logo = QIcon(APP_LOGO)
            app.setWindowIcon(logo)
            main_window = create_main_window(api, app)
            tray = create_tray(logo, app)

            configure_signals(app)

            # check if we want to continue with the configuration migrate
            show_migration_config_warning_and_check(app)

            # read the state file if it exists
            if os.path.isfile(STATE_FILE):
                api.open_config(STATE_FILE)
            api.start()

            cli = CLIStreamDeckServer(api, main_window.ui)
            cli.start()

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
