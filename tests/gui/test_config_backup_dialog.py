from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from streamdeck_ui.gui import show_migration_config_warning_and_check


@pytest.mark.serial
def test_do_not_show_migration_dialog_if_not_needed(
    qtbot, api_and_window, mock_confirm_dialog_exec, mock_migration_dialog, mocker
):
    """Test that dialog was not show when config file does not need migration"""
    # simulate the config file does not need migration
    mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].return_value = None
    mock_migration_dialog["streamdeck_ui.gui.config_file_need_migration"].return_value = False

    # allow test app exit was not called
    app_exit_mock = MagicMock()
    mocker.patch("streamdeck_ui.gui.sys.exit", app_exit_mock)

    # execute the config migration logic
    show_migration_config_warning_and_check(QApplication.instance())

    # conform the dialog was not shown
    assert not mock_confirm_dialog_exec.called

    # confirm that the migration logic was not called
    assert not mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].called


@pytest.mark.serial
def test_show_migration_dialog_with_confirm(
    qtbot, api_and_window, mock_confirm_dialog_exec, mock_migration_dialog, mocker
):
    """Test that dialog was show and the migration logic was called when user confirms the dialog"""
    # simulate the config file needs migration
    mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].return_value = None
    mock_migration_dialog["streamdeck_ui.gui.config_file_need_migration"].return_value = True

    # allow test app exit was not called
    app_exit_mock = MagicMock()
    mocker.patch("streamdeck_ui.gui.sys.exit", app_exit_mock)

    # execute the config migration logic
    show_migration_config_warning_and_check(QApplication.instance())

    # confirm the dialog was not shown
    assert not mock_confirm_dialog_exec.called

    # confirm that the migration logic was not called
    assert not mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].called


@pytest.mark.serial
def test_show_migration_dialog_without_confirm(
    qtbot, api_and_window, mock_confirm_dialog_exec, mock_migration_dialog, mocker
):
    """Test that dialog was show and the migration logic was not called when user cancels the dialog"""
    # simulate the config file needs migration
    mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].return_value = None
    mock_migration_dialog["streamdeck_ui.gui.config_file_need_migration"].return_value = True

    # avoid the app to exit when user says no
    app_exit_mock = MagicMock()
    mocker.patch("streamdeck_ui.gui.sys.exit", app_exit_mock)

    # simulate the user clicking the cancel button
    mock_confirm_dialog_exec.return_value = QMessageBox.StandardButton.No

    # execute the config migration logic
    show_migration_config_warning_and_check(QApplication.instance())

    # confirm that the migration logic was not called
    assert not mock_migration_dialog["streamdeck_ui.gui.do_config_file_migration"].called
