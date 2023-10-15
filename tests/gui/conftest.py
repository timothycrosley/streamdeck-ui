from typing import Tuple
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from streamdeck_ui.config import APP_LOGO
from streamdeck_ui.gui import MainWindow, build_device, create_main_window, create_tray
from tests.common import STREAMDECK_SERIAL, TestableStreamDeckServer, create_test_api_server


@pytest.fixture(autouse=True)
def mock_classes():
    """Automatically mock out classes used by byt GUI"""
    classes = [
        "streamdeck_ui.gui.CLIStreamDeckServer",
        "streamdeck_ui.gui.Semaphore",
        "streamdeck_ui.gui.QFileDialog",
        "PySide6.QtWidgets.QAbstractButton.setIcon",
    ]

    mocks = {}
    for class_ in classes:
        mocks[class_] = MagicMock()
        patch(class_, mocks[class_]).start()

    yield mocks

    patch.stopall()


@pytest.fixture
def api_and_window(mock_classes) -> Tuple[MainWindow, TestableStreamDeckServer]:
    """Return the application window.
    the application will behave as if a deck was connected with a single button
    and two pages exists ."""
    api = create_test_api_server()
    patch("streamdeck_ui.gui.api", api).start()
    main_window = create_main_window(api, QApplication.instance())
    create_tray(QIcon(APP_LOGO), QApplication.instance())

    # we simulate what happens when a deck is connected
    main_window.ui.device_list.addItem("test", userData=STREAMDECK_SERIAL)
    build_device(main_window.ui, api)

    yield main_window, api

    patch.stopall()


@pytest.fixture
def mock_desktop_services_open_url(mock_classes) -> MagicMock:
    """Mock the desktop services open url method."""
    mock = MagicMock()
    patch("streamdeck_ui.gui.QDesktopServices.openUrl", mock).start()

    yield mock

    patch.stopall()


@pytest.fixture
def mock_message_box_about(mock_classes):
    """Mock the message box about method."""
    mock = MagicMock()
    patch("streamdeck_ui.gui.QMessageBox.about", mock).start()

    yield mock

    patch.stopall()


@pytest.fixture
def mock_confirm_dialog_exec(mock_classes):
    """Mock the confirm dialog exec method to choose no."""
    mock = MagicMock()
    mock.exec.return_value = QMessageBox.StandardButton.Yes
    patch("streamdeck_ui.gui.QMessageBox.exec", mock).start()

    yield mock

    patch.stopall()


@pytest.fixture
def mock_migration_dialog(mock_classes):
    do_config_file_migration_mock = MagicMock()
    patch("streamdeck_ui.gui.do_config_file_migration", do_config_file_migration_mock).start()

    config_file_need_migration_mock = MagicMock()
    patch("streamdeck_ui.gui.config_file_need_migration", config_file_need_migration_mock)

    yield {
        "streamdeck_ui.gui.do_config_file_migration": do_config_file_migration_mock,
        "streamdeck_ui.gui.config_file_need_migration": config_file_need_migration_mock,
    }

    patch.stopall()
