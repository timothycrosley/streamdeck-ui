from unittest.mock import MagicMock

from streamdeck_ui.cli import commands


def test_set_page():
    cfg = {
        "command": "set_page",
        "deck": 0,
        "page": 0,
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetPageCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_page.assert_called_once_with(0, 0)


def test_set_brightness():
    cfg = {
        "command": "set_brightness",
        "deck": 0,
        "value": 0,
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetBrightnessCommand)
    assert cmd.deck_index == 0
    assert cmd.brightness == 0

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_brightness.assert_called_once_with(0, 0)


def test_set_button_text():
    cfg = {
        "command": "set_text",
        "deck": 0,
        "page": 0,
        "button": 0,
        "text": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonTextCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.button_text == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_text.assert_called_once_with(0, 0, 0, "test")


def test_set_button_write():
    cfg = {
        "command": "set_write",
        "deck": 0,
        "page": 0,
        "button": 0,
        "write": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonWriteCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.button_write == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_write.assert_called_once_with(0, 0, 0, "test")


def test_set_alignment():
    cfg = {
        "command": "set_alignment",
        "deck": 0,
        "page": 0,
        "button": 0,
        "alignment": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonTextAlignmentCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.button_text_alignment == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_text_vertical_align.assert_called_once_with(0, 0, 0, "test")


def test_set_button_cmd():
    cfg = {
        "command": "set_cmd",
        "deck": 0,
        "page": 0,
        "button": 0,
        "button_cmd": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonCmdCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.button_cmd == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_command.assert_called_once_with(0, 0, 0, "test")


def test_set_button_keys():
    cfg = {
        "command": "set_keys",
        "deck": 0,
        "page": 0,
        "button": 0,
        "button_keys": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonKeysCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.button_keys == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_keys.assert_called_once_with(0, 0, 0, "test")


def test_set_button_icon():
    cfg = {
        "command": "set_icon",
        "deck": 0,
        "page": 0,
        "button": 0,
        "icon": "test",
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.SetButtonIconCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0
    assert cmd.icon_path == "test"

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_icon.assert_called_once_with(0, 0, 0, "test")


def test_clear_button_icon():
    cfg = {
        "command": "clear_icon",
        "deck": 0,
        "page": 0,
        "button": 0,
    }
    cmd = commands.create_command(cfg)

    assert isinstance(cmd, commands.ClearButtonIconCommand)
    assert cmd.deck_index == 0
    assert cmd.page_index == 0
    assert cmd.button_index == 0

    api = MagicMock()
    ui = MagicMock()

    cmd.execute(api, ui)

    api.set_button_icon.assert_called_once_with(0, 0, 0, "")


def test_unknown_command():
    cfg = {
        "command": "unknown",
    }
    cmd = commands.create_command(cfg)

    assert cmd is None
