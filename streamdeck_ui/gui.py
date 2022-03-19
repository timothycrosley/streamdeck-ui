"""Defines the QT powered interface for configuring Stream Decks"""
import os
import sys
from functools import partial
from typing import Dict, List, Optional, Tuple

import pkg_resources
from pynput.keyboard import Controller
from PySide2 import QtWidgets
from PySide2.QtCore import QMimeData, QSignalBlocker, QSize, Qt, QTimer, QUrl
from PySide2.QtGui import QDesktopServices, QDrag, QIcon
from PySide2.QtWidgets import QAbstractItemView, QAction, QApplication, QDialog, QFileDialog, QMainWindow, QMenu, QMessageBox, QSizePolicy, QSystemTrayIcon, QTreeWidgetItem

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.config import LOGO, STATE_FILE
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


text_update_timer: Optional[QTimer] = None
"Timer used to delay updates to the button text"

dimmer_options = {"Never": 0, "10 Seconds": 10, "1 Minute": 60, "5 Minutes": 300, "10 Minutes": 600, "15 Minutes": 900, "30 Minutes": 1800, "1 Hour": 3600, "5 Hours": 7200, "10 Hours": 36000}
last_image_dir = ""

plugins = []



class ActionTree(QtWidgets.QTreeWidget):
    def __init__(self, parent, parent_window, api: StreamDeckServer):
        super(ActionTree, self).__init__(parent)

        self.setAcceptDrops(True)
        self.api = api
        self.parent_window = parent_window

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.
        if e.buttons() != Qt.LeftButton:
            return

        mimedata = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec_(Qt.MoveAction)

    def dropEvent(self, e):  # noqa: N802 - Part of QT signature.
        if e.source():
            if isinstance(e.source(), ActionSelectTree):
                    selected_item = e.source().currentItem()
                    action = selected_item.data(0, Qt.UserRole)
                    self.parent_window.add_action("keydown", action)

    def dragEnterEvent(self, e):  # noqa: N802 - Part of QT signature.
        if isinstance(e.source(), ActionSelectTree):
            e.accept()

class ActionSelectTree(QtWidgets.QTreeWidget):
    def __init__(self, parent, ui, api: StreamDeckServer):
        super(ActionSelectTree, self).__init__(parent)

        # self.setAcceptDrops(True)
        self.ui = ui
        self.api = api

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.

        if e.buttons() != Qt.LeftButton:
            return

        # Can't drag category items
        if self.currentItem().is_category:
            return

        mimedata = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec_(Qt.MoveAction)

class DraggableButton(QtWidgets.QToolButton):
    """A QToolButton that supports drag and drop and swaps the button properties on drop"""

    def __init__(self, parent, parent_window, api: StreamDeckServer, index: int):
        super(DraggableButton, self).__init__(parent)

        self.index = index
        self.setAcceptDrops(True)
        self.parent_window = parent_window
        self.api = api
        self.index

    def mouseMoveEvent(self, e):  # noqa: N802 - Part of QT signature.

        if e.buttons() != Qt.LeftButton:
            return

        self.api.reset_dimmer(self.parent_window.serial_number())

        mimedata = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec_(Qt.MoveAction)

    def dropEvent(self, e):  # noqa: N802 - Part of QT signature.
        global selected_button

        self.setStyleSheet(BUTTON_STYLE)
        serial_number = self.parent_window.serial_number()
        page = self.parent_window.page()

        if e.source():

            if isinstance(e.source(), ActionSelectTree):
                selected_item = e.source().currentItem()
                action = selected_item.data(0, Qt.UserRole)

                # We could be dragging a tree node onto a button that is not the
                # currently selected button
                if selected_button != self:
                    selected_button.setChecked(False)
                    self.setChecked(True)
                    selected_button = self
                self.parent_window.add_action("keydown", action)

                return
            else:

                # Ignore drag and drop on yourself
                if e.source().index == self.index:
                    return

                self.api.swap_buttons(serial_number, page, e.source().index, self.index)
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
                self.api.set_button_icon(serial_number, page, self.index, file_name)

        icon = self.api.get_button_icon_pixmap(serial_number, page, e.source().index)
        if icon:
            e.source().setIcon(icon)

        icon = self.api.get_button_icon_pixmap(serial_number, page, self.index)
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


selected_button: Optional[DraggableButton] = None
"A reference to the currently selected button"


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui: Ui_SettingsDialog = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.show()


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

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_shown: bool = True

        # TODO: This replaces the stock "QTreeWidget" with one that has the drag/drop events overriden
        # This is hacky - and there are ways to improve this so that the Qt Designer understands
        # the custom widget.
        # https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html#custom-widgets-in-qt-designer
        # https://stackoverflow.com/questions/52128188/using-a-custom-pyside2-widget-in-qt-designer

        # Replace action selection tree
        self.ui.select_action_tree.deleteLater()
        self.ui.select_action_tree = ActionSelectTree(self.ui.toprightwidget, None, None)
        self.ui.select_action_tree.setObjectName("select_action_tree")
        self.ui.select_action_tree.setEnabled(True)
        self.ui.select_action_tree.setAlternatingRowColors(False)
        self.ui.select_action_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.select_action_tree.setIconSize(QSize(32, 32))
        self.ui.select_action_tree.setTextElideMode(Qt.ElideLeft)
        self.ui.select_action_tree.setIndentation(40)
        self.ui.select_action_tree.setRootIsDecorated(False)
        self.ui.select_action_tree.setUniformRowHeights(False)
        self.ui.select_action_tree.setItemsExpandable(False)
        self.ui.select_action_tree.setExpandsOnDoubleClick(False)
        self.ui.select_action_tree.header().setVisible(False)
        self.ui.verticalLayout_9.addWidget(self.ui.select_action_tree)

        # Replace action tree
        self.ui.action_tree.deleteLater()
        self.ui.action_tree = ActionTree(self.ui.topleftwidget, self, api)
        self.ui.action_tree.setObjectName(u"action_tree")
        self.ui.action_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.action_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.action_tree.setIndentation(0)
        self.ui.action_tree.header().setVisible(False)
        self.ui.action_tree.header().setHighlightSections(False)
        self.ui.verticalLayout_8.addWidget(self.ui.action_tree)

        action_header = self.ui.action_tree.headerItem()
        action_header.setText(1, "Configuration");
        action_header.setText(0, "Action");

        # end of hack

        self.ui.select_action_tree.doubleClicked.connect(self.add_action_button)

        self.ui.action_tree.setDragEnabled(False)
        self.ui.action_tree.setAcceptDrops(False)
        # The only way to accept drops is to set InternalMove
        self.ui.action_tree.setDragDropMode(QAbstractItemView.InternalMove)

        self.ui.select_action_tree.setDragEnabled(True)
        self.ui.select_action_tree.setDropIndicatorShown(False)
        self.ui.select_action_tree.setDragDropMode(QAbstractItemView.DragOnly)

        self.ui.add_action_button.clicked.connect(self.add_action_button)

        self.ui.select_image_button.clicked.connect(self.select_image)
        self.ui.vertical_text_button.clicked.connect(self.align_text_vertical)
        self.ui.remove_image_button.clicked.connect(self.remove_image)

        self.ui.actionExport.triggered.connect(self.export_config)
        self.ui.actionImport.triggered.connect(self.import_config)
        self.ui.settingsButton.clicked.connect(self.show_settings)

        self.ui.remove_action_button.clicked.connect(self.remove_action_button)
        self.ui.up_action_button.clicked.connect(self.up_action_button)
        self.ui.down_action_button.clicked.connect(self.down_action_button)
        self.ui.actionDocs.triggered.connect(self.browse_documentation)
        self.ui.actionGithub.triggered.connect(self.browse_github)
        self.ui.settingsButton.setEnabled(False)
        self.enable_button_configuration(False)

        self.ui.text.textChanged.connect(self.update_button_text)
        self.ui.actionAbout.triggered.connect(self.about_dialog)

        self.ui.actionExit.triggered.connect(app.exit)

    def change_brightness(self, deck_id: str, brightness: int):
        """Changes the brightness of the given streamdeck, but does not save
        the state."""
        api.decks[deck_id].set_brightness(brightness)

    # TODO: This will all be removed
    def handle_keypress(self, deck_id: str, key: int, state: bool) -> None:

        if state:
            page = api.get_page(deck_id)

            brightness_change = api.get_button_change_brightness(deck_id, page, key)
            if brightness_change:
                try:
                    api.change_brightness(deck_id, brightness_change)
                except Exception as error:
                    print(f"Could not change brightness: {error}")

            switch_page = api.get_button_switch_page(deck_id, page, key)
            if switch_page:
                api.set_page(deck_id, switch_page - 1)
                if self.serial_number() == deck_id:
                    self.ui.pages.setCurrentIndex(switch_page - 1)

    def serial_number(self) -> str:
        """Returns the currently selected Stream Deck serial number

        :return: The serial number
        :rtype: str
        """
        return self.ui.device_list.itemData(self.ui.device_list.currentIndex())

    def page(self) -> int:
        """Returns the current page (tab) the user is on.

        :return: The page index
        :rtype: int
        """
        return self.ui.pages.currentIndex()

    def streamdeck_cpu_changed(self, serial_number: str, cpu: int):
        if cpu > 100:
            cpu == 100
        if self.serial_number() == serial_number:
            self.ui.cpu_usage.setValue(cpu)
            self.ui.cpu_usage.setToolTip(f"Rendering CPU usage: {cpu}%")
            self.ui.cpu_usage.update()

    def update_button_text(self) -> None:
        if selected_button:
            deck_id = self.serial_number()
            if deck_id:
                # There may be no decks attached
                api.set_button_text(deck_id, self.page(), selected_button.index, self.ui.text.toPlainText())
                icon = api.get_button_icon_pixmap(deck_id, self.page(), selected_button.index)
                if icon:
                    selected_button.setIcon(icon)

    def update_button_command(self, command: str) -> None:
        if selected_button:
            deck_id = self.serial_number()
            api.set_button_command(deck_id, self.page(), selected_button.index, command)

    def update_button_keys(self, keys: str) -> None:
        if selected_button:
            deck_id = self.serial_number()
            api.set_button_keys(deck_id, self.page(), selected_button.index, keys)

    def update_change_brightness(self, amount: int) -> None:
        if selected_button:
            deck_id = self.serial_number()
            api.set_button_change_brightness(deck_id, self.page(), selected_button.index, amount)

    def update_switch_page(self, page: int) -> None:
        if selected_button:
            deck_id = self.serial_number()
            api.set_button_switch_page(deck_id, self.page(), selected_button.index, page)

    def up_action_button(self) -> None:
        items = self.ui.action_tree.selectedItems()
        if items:
            item = items[0]
            item_data = item.data(0, Qt.UserRole)
            if item_data:
                action, index, event = item_data
                if index:
                    action_settings = api.get_action_settings_list(self.serial_number(), self.page(), selected_button.index, event)
                    action_settings[index-1], action_settings[index] = action_settings[index], action_settings[index-1] 
                    api.set_action_settings_list(self.serial_number(), self.page(), selected_button.index, event, action_settings)

                    # Rebuild the action list
                    self.build_actions(self.serial_number(), self.page(), selected_button.index)

                    # Re-select the new item
                    self.ui.action_tree.topLevelItem(0).child(index-1).setSelected(True)


    def down_action_button(self) -> None:
        items = self.ui.action_tree.selectedItems()
        if items:
            item = items[0]
            item_data = item.data(0, Qt.UserRole)
            if item_data:
                action, index, event = item_data

                action_settings = api.get_action_settings_list(self.serial_number(), self.page(), selected_button.index, event)

                if index < (len(action_settings)-1):
                    action_settings[index], action_settings[index + 1] = action_settings[index + 1], action_settings[index] 
                    api.set_action_settings_list(self.serial_number(), self.page(), selected_button.index, event, action_settings)

                    # Rebuild the action list
                    self.build_actions(self.serial_number(), self.page(), selected_button.index)

                    # Re-select the new item
                    self.ui.action_tree.topLevelItem(0).child(index+1).setSelected(True)

    def remove_action_button(self) -> None:
        serial_number = self.serial_number()

        items = self.ui.action_tree.selectedItems()
        if items:
            selected_item = items[0]

            # Parent items (events) don't have data
            if selected_item.data(0, Qt.UserRole) and selected_button is not None:

                confirm = QMessageBox(self)
                confirm.setWindowTitle("Remove action")
                confirm.setText("Are you sure you want to remove the selected action?")
                confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm.setIcon(QMessageBox.Question)
                button = confirm.exec_()
                if button == QMessageBox.Yes:
                    action, index, event = selected_item.data(0, Qt.UserRole)
                    api.remove_action_setting(serial_number, self.page(), selected_button.index, event, index)

                    # Rebuild the action list
                    self.build_actions(serial_number, self.page(), selected_button.index)

                    # Clear the configuration area
                    self.load_plugin_ui()

    def enable_button_configuration(self, enabled: bool):
        self.ui.text.setEnabled(enabled)
        self.ui.select_image_button.setEnabled(enabled)
        self.ui.remove_image_button.setEnabled(enabled)
        self.ui.vertical_text_button.setEnabled(enabled)
        self.ui.up_action_button.setEnabled(enabled)
        self.ui.down_action_button.setEnabled(enabled)
        self.ui.add_action_button.setEnabled(enabled)
        self.ui.action_tree.setEnabled(enabled)
        self.ui.select_action_tree.setEnabled(enabled)
        self.ui.remove_action_button.setEnabled(enabled)

    def browse_documentation(self):
        url = QUrl("https://github.com/timothycrosley/streamdeck-ui#readme")
        QDesktopServices.openUrl(url)

    def browse_github(self):
        url = QUrl("https://github.com/timothycrosley/streamdeck-ui")
        QDesktopServices.openUrl(url)

    def disable_dim_settings(self, settings: SettingsDialog, _index: int) -> None:
        disable = dimmer_options.get(settings.ui.dim.currentText()) == 0
        settings.ui.brightness_dimmed.setDisabled(disable)
        settings.ui.label_brightness_dimmed.setDisabled(disable)

    def toggle_dim_all(self) -> None:
        api.toggle_dimmers()

    def set_brightness(self, value: int) -> None:
        deck_id = self.serial_number()
        api.set_brightness(deck_id, value)

    def set_brightness_dimmed(self, value: int, full_brightness: int) -> None:
        deck_id = self.serial_number()
        api.set_brightness_dimmed(deck_id, int(full_brightness * (value / 100)))
        api.reset_dimmer(deck_id)

    def show_settings(self) -> None:
        """Shows the settings dialog and allows the user the change deck specific
        settings. Settings are not saved until OK is clicked."""
        deck_id = self.serial_number()
        settings = SettingsDialog(self)
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
        settings.ui.brightness.valueChanged.connect(partial(self.change_brightness, deck_id))
        settings.ui.dim.currentIndexChanged.connect(partial(self.disable_dim_settings, settings))
        if settings.exec_():
            # Commit changes
            if existing_index != settings.ui.dim.currentIndex():
                # dimmers[deck_id].timeout = settings.ui.dim.currentData()
                api.set_display_timeout(deck_id, settings.ui.dim.currentData())
            self.set_brightness(settings.ui.brightness.value())
            self.set_brightness_dimmed(settings.ui.brightness_dimmed.value(), settings.ui.brightness.value())
        else:
            # User cancelled, reset to original brightness
            self.change_brightness(deck_id, api.get_brightness(deck_id))

        api.reset_dimmer(deck_id)

    def export_config(self) -> None:
        file_name = QFileDialog.getSaveFileName(self, "Export Config", os.path.expanduser("~/streamdeck_ui_export.json"), "JSON (*.json)")[0]
        if not file_name:
            return
        api.export_config(file_name)

    def import_config(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, "Import Config", os.path.expanduser("~"), "Config Files (*.json)")[0]
        if not file_name:
            return

        api.import_config(file_name)
        self.redraw_buttons()

    def remove_image(self) -> None:
        deck_id = self.serial_number()
        image = api.get_button_icon(deck_id, self.page(), selected_button.index)  # type: ignore # Index property added
        if image:
            confirm = QMessageBox(self)
            confirm.setWindowTitle("Remove image")
            confirm.setText("Are you sure you want to remove the image for this button?")
            confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm.setIcon(QMessageBox.Question)
            button = confirm.exec_()
            if button == QMessageBox.Yes:
                api.set_button_icon(deck_id, self.page(), selected_button.index, "")  # type: ignore # Index property added
                self.redraw_buttons()

    def align_text_vertical(self) -> None:
        serial_number = self.serial_number()
        position = api.get_text_vertical_align(serial_number, self.page(), selected_button.index)  # type: ignore # Index property added
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

        api.set_text_vertical_align(serial_number, self.page(), selected_button.index, position)  # type: ignore # Index property added
        self.redraw_buttons()

    def select_image(self) -> None:
        global last_image_dir
        deck_id = self.serial_number()
        image_file = api.get_button_icon(deck_id, self.page(), selected_button.index)  # type: ignore # Index property added
        if not image_file:
            if not last_image_dir:
                image_file = os.path.expanduser("~")
            else:
                image_file = last_image_dir
        file_name = QFileDialog.getOpenFileName(self, "Open Image", image_file, "Image Files (*.png *.jpg *.bmp *.svg *.gif)")[0]
        if file_name:
            last_image_dir = os.path.dirname(file_name)
            deck_id = self.serial_number()
            api.set_button_icon(deck_id, self.page(), selected_button.index, file_name)  # type: ignore # Index property added
            self.redraw_buttons()

    def change_page(self, page: int) -> None:
        global selected_button

        """Change the Stream Deck to the desired page and update
        the on-screen buttons.

        :param ui: Reference to the ui
        :type ui: _type_
        :param page: The page number to switch to
        :type page: int
        """
        if selected_button:
            selected_button.setChecked(False)
            selected_button = None

        deck_id = self.serial_number()
        if deck_id:
            api.set_page(deck_id, page)
            self.redraw_buttons()
            api.reset_dimmer(deck_id)

        self.reset_button_configuration()

    def button_clicked(self, clicked_button, buttons) -> None:
        global selected_button

        ui = self.ui
        selected_button = clicked_button
        for button in buttons:
            if button == clicked_button:
                continue

            button.setChecked(False)

        deck_id = self.serial_number()
        button_id = selected_button.index  # type: ignore # Index property added
        if selected_button.isChecked():  # type: ignore # False positive mypy
            self.enable_button_configuration(True)

            # Populate tree view with actions
            self.build_actions(deck_id, self.page(), button_id)
            ui.text.setPlainText(api.get_button_text(deck_id, self.page(), button_id))

            image_path = api.get_button_icon(deck_id, self.page(), button_id)
            if image_path:
                image_path = os.path.basename(image_path)
            ui.image_label.setText(image_path)
            api.reset_dimmer(deck_id)
        else:
            selected_button = None
            self.reset_button_configuration()

    def redraw_buttons(self) -> None:
        deck_id = self.serial_number()
        current_tab = self.ui.pages.currentWidget()
        buttons = current_tab.findChildren(QtWidgets.QToolButton)
        for button in buttons:
            if not button.isHidden():
                # When rebuilding the buttons, we hide the old ones
                # and mark for deletion. They still hang around so
                # ignore them here
                icon = api.get_button_icon_pixmap(deck_id, self.page(), button.index)
                if icon:
                    button.setIcon(icon)

    def reset_button_configuration(self):
        """Clears the configuration for a button and disables editing of them. This is done when
        there is no key selected or if there are no devices connected.
        """
        self.ui.text.clear()
        self.ui.image_label.clear()
        self.ui.action_tree.clear()
        self.load_plugin_ui()
        self.enable_button_configuration(False)

    def build_buttons(self, tab) -> None:
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

        deck_id = self.serial_number()

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
                button = DraggableButton(base_widget, self, api, index)
                button.setCheckable(True)
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
            button.clicked.connect(lambda button=button, buttons=buttons: self.button_clicked(button, buttons))

    def build_device(self, _device_index=None) -> None:
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
        ui = self.ui
        if ui.device_list.count() > 0:
            style = "background-color: black"

        for page_id in range(ui.pages.count()):
            page = ui.pages.widget(page_id)
            page.setStyleSheet(style)
            self.build_buttons(page)

        if ui.device_list.count() > 0:
            ui.settingsButton.setEnabled(True)
            # Set the active page for this device
            ui.pages.setCurrentIndex(api.get_page(self.serial_number()))

            # Draw the buttons for the active page
            self.redraw_buttons()
        else:
            ui.settingsButton.setEnabled(False)
            self.reset_button_configuration()

    def streamdeck_attached(self, deck: Dict):

        serial_number = deck["serial_number"]
        blocker = QSignalBlocker(self.ui.device_list)
        try:
            self.ui.device_list.addItem(f"{deck['type']} - {serial_number}", userData=serial_number)
        finally:
            blocker.unblock()
        self.build_device(self)

    def streamdeck_detached(self, serial_number):
        index = self.ui.device_list.findData(serial_number)
        if index != -1:
            # Should not be (how can you remove a device that was never attached?)
            # Check anyways
            self.ui.device_list.removeItem(index)

    def add_action_button(self) -> None:
        items = self.ui.select_action_tree.selectedItems()
        if items:
            selected_item = items[0]
            action = selected_item.data(0, Qt.UserRole)

            # Category items don't have an action
            if action:
                self.add_action("keydown", action)

    def add_action(self, event: str, action):

        if selected_button is not None:
            serial_number = self.serial_number()
            page = self.page()
            button = selected_button.index

            api.add_action_setting(serial_number, page, button, event, action().id())

            self.ui.action_tree.clear()
            self.build_actions(serial_number, self.page(), selected_button.index)
            self.ui.action_tree.scrollToBottom()

            keydown_item = self.ui.action_tree.topLevelItem(self.ui.action_tree.topLevelItemCount() - 1)
            keydown_item.child(keydown_item.childCount() - 1).setSelected(True)

    def build_actions(self, serial_number: str, page: int, button_id: int):

        ui = self.ui
        ui.action_tree.clear()
        actions = api.get_action_list(serial_number, page, button_id, "keydown")

        # This must be fixed - it's just a hack. We want to automatically
        # group actions by the even they're bound to
        key_pressed = QTreeWidgetItem(["When key pressed:"])

        icon = QIcon()
        icon.addFile(":/icons/icons/keyboard-enter.png", QSize(), QIcon.Normal, QIcon.Off)
        key_pressed.setIcon(0, icon)
        key_pressed.setExpanded(True)
        key_pressed.setData(0, Qt.UserRole, None)

        # What needs to happen here:
        # For a given button, iterate over the actions
        # Look at the setting - match it to an available plugin
        # Initialize the action (or should they already be initialized, since they
        # need to be ready to run when you press the button?)
        # Ask it for the category and summary

        for index, action in enumerate(actions):
            # Verify that plugin exists
            tree_item = QTreeWidgetItem([action.get_name(), action.get_summary()])
            key_pressed.addChild(tree_item)

            # Store the action, its index in the settings and event type in a tuple so
            # we can remove it or act on it later.
            tree_item.setData(0, Qt.UserRole, (action, index, "keydown"))

        ui.action_tree.itemSelectionChanged.connect(self.load_plugin_ui)
        ui.action_tree.addTopLevelItem(key_pressed)
        ui.action_tree.expandAll()
        ui.action_tree.resizeColumnToContents(0)
        ui.action_tree.resizeColumnToContents(1)

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

    def update_plugins(self, plugins):

        # Create unique list of categories
        categories: Dict[str, QTreeWidgetItem] = {}

        for _key, action in plugins.items():
            obj = action()
            category = obj.get_category()

            if category not in categories:
                widget = QTreeWidgetItem([category])
                widget.setIcon(0, obj.get_icon())
                widget.setExpanded(True)
                widget.is_category = True
                categories[category] = widget

        # Sort categories alphabetically
        categories = {k: v for k, v in sorted(categories.items())}

        # Add all parent nodes
        for _, widget in categories.items():
            self.ui.select_action_tree.addTopLevelItem(widget)

        # All child items (note these are not currently sorted)
        # TODO:  Set sorted on tree or sort
        for _key, action in plugins.items():
            obj = action()

            parent = categories[obj.get_category()]
            widget = QTreeWidgetItem([obj.get_name()])
            widget.is_category = False
            parent.addChild(widget)
            # Use the UserRole to associate the action object with the QTreeWidgetItem.
            # This can be used to retrieve a reference to the action in the event handler.
            widget.setData(0, Qt.UserRole, action)

        self.ui.select_action_tree.expandAll()

    def load_plugin_ui(self):

        # TODO: Could we somehow bind the action back to the UI?
        # When the summary changes, update the UI
        old = self.ui.actionlayout.takeAt(0)
        if old:
            old.widget().deleteLater()

        item = None
        items = self.ui.action_tree.selectedItems()
        if items:
            item = items[0]
            action = item.data(0, Qt.UserRole)

        if item and item.data(0, Qt.UserRole):
            action, _index, _event = item.data(0, Qt.UserRole)
            if action:
                self.ui.actionlayout.addWidget(action.get_ui(self))


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
    action_dim.triggered.connect(main_window.toggle_dim_all)
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


def start(_exit: bool = False) -> None:
    global api
    global plugins
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

    api = StreamDeckServer()
    if os.path.isfile(STATE_FILE):
        api.open_config(STATE_FILE)

    plugins = api.load_plugins()

    # The QApplication object holds the Qt event loop and you need one of these
    # for your application
    app = QApplication(sys.argv)
    app.setApplicationName("Streamdeck UI")
    app.setApplicationVersion(version)
    logo = QIcon(LOGO)
    app.setWindowIcon(logo)
    main_window = MainWindow(app)
    ui = main_window.ui
    tray = create_tray(logo, app, main_window)

    main_window.update_plugins(plugins)
    api.streamdeck_keys.key_pressed.connect(main_window.handle_keypress)

    ui.device_list.currentIndexChanged.connect(main_window.build_device)
    ui.pages.currentChanged.connect(main_window.change_page)

    api.plugevents.attached.connect(main_window.streamdeck_attached)
    api.plugevents.detached.connect(main_window.streamdeck_detached)
    api.plugevents.cpu_changed.connect(main_window.streamdeck_cpu_changed)

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
