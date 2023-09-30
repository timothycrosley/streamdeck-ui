import json
from unittest.mock import mock_open, patch

import pytest

from streamdeck_ui.config import (
    CONFIG_FILE_PREVIOUS_VERSION,
    CONFIG_FILE_VERSION,
    read_state_from_config,
    write_state_to_config,
)
from streamdeck_ui.model import ButtonMultiState, ButtonState, DeckState

TEST_CONFIG_STATE = {
    "DL4XXXXXX": {
        "buttons": {
            0: {
                0: {
                    "state": 0,
                    "states": {
                        0: {
                            "text": "",
                            "icon": "",
                            "keys": "",
                            "write": "",
                            "command": "",
                            "switch_page": 0,
                            "switch_state": 0,
                            "brightness_change": 0,
                            "text_vertical_align": "",
                            "text_horizontal_align": "",
                            "font": "",
                            "font_color": "",
                            "font_size": 0,
                            "background_color": "",
                        }
                    },
                }
            }
        },
        "display_timeout": 0,
        "brightness": 0,
        "brightness_dimmed": 0,
        "rotation": 0,
        "page": 0,
    }
}
TEST_CONFIG_STATE_V1 = {
    "DL4XXXXXX": {
        "buttons": {
            0: {
                0: {
                    "text": "",
                    "icon": "",
                    "keys": "",
                    "write": "",
                    "command": "",
                    "switch_page": 0,
                    "brightness_change": 0,
                    "text_vertical_align": "",
                    "text_horizontal_align": "",
                    "font": "",
                    "font_color": "",
                    "font_size": 0,
                    "background_color": "",
                }
            }
        },
        "display_timeout": 0,
        "brightness": 0,
        "brightness_dimmed": 0,
        "rotation": 0,
        "page": 0,
    }
}

TEST_CONFIG_STATE_V1_WITH_MISSING_KEYS = {
    "DL4XXXXXX": {
        "buttons": {0: {0: {}}},
    }
}

TEST_MODEL_STATE = {
    "DL4XXXXXX": DeckState(
        buttons={
            0: {
                0: ButtonMultiState(
                    state=0,
                    states={0: ButtonState()},
                )
            }
        },
        display_timeout=0,
        brightness=0,
        brightness_dimmed=0,
        rotation=0,
    )
}


# fmt: off
@pytest.mark.parametrize(
    "file_version, expected_exception, config_state",
    [
        (CONFIG_FILE_PREVIOUS_VERSION, None, TEST_CONFIG_STATE_V1),
        (CONFIG_FILE_PREVIOUS_VERSION, None, TEST_CONFIG_STATE_V1_WITH_MISSING_KEYS),
        (CONFIG_FILE_VERSION, None, TEST_CONFIG_STATE),
        (CONFIG_FILE_VERSION + 1, ValueError, TEST_CONFIG_STATE)
    ],
)
# fmt: on
def test_read_state_from_config(file_version, expected_exception, config_state):
    """Ensure that the config file content is correctly read, and that the correct error is raised when the file version is not correct"""
    mock_content = {"streamdeck_ui_version": file_version, "state": config_state}
    mock_json_str = json.dumps(mock_content)
    with patch("builtins.open", mock_open(read_data=mock_json_str)):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = mock_content
            if expected_exception:
                with pytest.raises(expected_exception):
                    read_state_from_config("mock_path")
            else:
                result = read_state_from_config("mock_path")
                assert result == TEST_MODEL_STATE


@pytest.mark.parametrize(
    "raise_exception, expected_exception",
    [(None, None), (Exception("Write Error"), ValueError)],
)
def test_write_state_to_config(raise_exception, expected_exception):
    """Ensure that the config file content is correctly written, and that the correct error is raised"""
    m = mock_open()
    with patch("builtins.open", m):
        with patch("json.dump") as mock_json_dump:
            with patch("os.replace") as mock_os_replace:
                if raise_exception:
                    mock_json_dump.side_effect = raise_exception

                if expected_exception:
                    with pytest.raises(expected_exception):
                        write_state_to_config("mock_path", TEST_MODEL_STATE)
                else:
                    write_state_to_config("mock_path", TEST_MODEL_STATE)
                    m.assert_called_once_with("mock_path.tmp", "w")
                    mock_json_dump.assert_called_once()
                    mock_os_replace.assert_called_once()
                    assert mock_json_dump.call_args[0][0]["state"] == TEST_CONFIG_STATE
                    assert mock_json_dump.call_args[0][0]["streamdeck_ui_version"] == CONFIG_FILE_VERSION
