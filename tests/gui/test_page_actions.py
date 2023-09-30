from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox


def test_add_new_page(qtbot, api_and_window, mocker):
    """Test the behaviour of the add page button"""
    main_window, api = api_and_window

    method_spy = mocker.spy(api, "add_new_page")

    # check how many pages are present
    assert main_window.ui.pages.count() == 2

    # click the add page button
    qtbot.mouseClick(main_window.ui.add_page, Qt.LeftButton)

    # check that the page was added
    assert main_window.ui.pages.count() == 3

    method_spy.assert_called_once()


def test_remove_page_with_confirmation(qtbot, api_and_window, mock_confirm_dialog_exec, mocker):
    """Test the behavior of the remove page button when user confirms the action."""
    main_window, api = api_and_window

    method_spy = mocker.spy(api, "remove_page")

    # ensure that the confirmation dialog returns yes
    mock_confirm_dialog_exec.return_value = QMessageBox.StandardButton.Yes

    # check how many pages are present
    assert main_window.ui.pages.count() == 2

    # click the remove page button
    qtbot.mouseClick(main_window.ui.remove_page, Qt.LeftButton)

    # check that the page was removed
    assert main_window.ui.pages.count() == 1

    method_spy.assert_called_once()


def test_remove_page_with_no_confirmation(qtbot, api_and_window, mock_confirm_dialog_exec, mocker):
    """Test the remove page menu item when user cancels the action."""
    main_window, api = api_and_window

    method_spy = mocker.spy(api, "remove_page")

    # ensure that the confirmation dialog returns yes
    mock_confirm_dialog_exec.return_value = QMessageBox.StandardButton.No

    # check how many pages are present
    assert main_window.ui.pages.count() == 2

    # click the remove page button
    qtbot.mouseClick(main_window.ui.remove_page, Qt.LeftButton)

    # check that the page was not removed
    assert main_window.ui.pages.count() == 2

    method_spy.assert_not_called()
