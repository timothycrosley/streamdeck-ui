import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QToolButton


@pytest.mark.serial
def test_add_button_state(qtbot, api_and_window, mocker):
    """Test the behaviour of the add button state button."""
    main_window, api = api_and_window
    method_spy = mocker.spy(api, "add_new_button_state")

    # 1. select a deck button
    buttons = main_window.ui.pages.widget(0).deck_buttons.findChildren(QToolButton)
    qtbot.mouseClick(buttons[0], Qt.LeftButton)
    # 2. click the add button state button
    qtbot.mouseClick(main_window.ui.add_button_state, Qt.LeftButton)

    method_spy.assert_called_once()


@pytest.mark.serial
def test_remove_button_state_with_confirmation(qtbot, api_and_window, mock_confirm_dialog_exec, mocker):
    """Test the behaviour of the remove button state button when user confirms the action."""
    main_window, api = api_and_window
    method_spy = mocker.spy(api, "remove_button_state")

    # ensure that the confirmation dialog returns yes
    mock_confirm_dialog_exec.return_value = QMessageBox.StandardButton.Yes

    # select a deck button
    buttons = main_window.ui.pages.widget(0).deck_buttons.findChildren(QToolButton)
    qtbot.mouseClick(buttons[0], Qt.LeftButton)

    # check how many button states are present
    assert main_window.ui.button_states.count() == 3

    # click the remove button state button
    qtbot.mouseClick(main_window.ui.remove_button_state, Qt.LeftButton)

    # check that the button state was removed
    assert main_window.ui.button_states.count() == 2

    method_spy.assert_called_once()


@pytest.mark.serial
def test_remove_button_state_with_no_confirmation(qtbot, api_and_window, mock_confirm_dialog_exec, mocker):
    """Test the remove button state menu item when user cancels the action."""
    main_window, api = api_and_window

    method_spy = mocker.spy(api, "remove_button_state")

    # ensure that the confirmation dialog returns yes
    mock_confirm_dialog_exec.return_value = QMessageBox.StandardButton.No

    # select a deck button
    buttons = main_window.ui.pages.widget(0).deck_buttons.findChildren(QToolButton)
    qtbot.mouseClick(buttons[0], Qt.LeftButton)

    # check how many button states are present
    assert main_window.ui.button_states.count() == 3

    # click the remove button state button
    qtbot.mouseClick(main_window.ui.remove_button_state, Qt.LeftButton)

    # check that the button state was not removed
    assert main_window.ui.button_states.count() == 3

    method_spy.assert_not_called()
