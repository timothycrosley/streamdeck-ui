from unittest.mock import MagicMock, patch

import pytest

from streamdeck_ui.modules.keyboard import Keyboard


def test_write_without_pynput_supported():
    keyboard = Keyboard()
    keyboard.pynput_supported = False
    with pytest.raises(Exception, match="Virtual keyboard functionality is not supported on this system."):
        keyboard.write("test")


def test_keys_without_pynput_supported():
    keyboard = Keyboard()
    keyboard.pynput_supported = False
    with pytest.raises(Exception, match="Virtual keyboard functionality is not supported on this system."):
        keyboard.keys("ctrl+1")


@patch("streamdeck_ui.modules.keyboard.Controller")
def test_write_with_pynput_supported(mock_controller: MagicMock):
    keyboard = Keyboard(mock_controller)
    keyboard.pynput_supported = True
    keyboard.write("test")
    mock_controller.press.assert_called()
    mock_controller.release.assert_called()


@patch("streamdeck_ui.modules.keyboard.Controller")
def test_keys_with_pynput_supported(mock_controller: MagicMock):
    keyboard = Keyboard(mock_controller)
    keyboard.pynput_supported = True
    keyboard.keys("ctrl+1")
    mock_controller.press.assert_called()
    mock_controller.release.assert_called()
