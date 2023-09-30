from unittest.mock import MagicMock

from tests.api.helpers import assert_state_saved


def test_brightness(api_server, streamdeck_serial):
    """Test the brightness state was updated."""
    api_server.set_brightness(streamdeck_serial, 10)
    assert api_server.get_brightness(streamdeck_serial) == 10
    assert_state_saved(api_server)


def test_brightness_dimmed(api_server, streamdeck_serial):
    """Test the brightness state was updated."""
    api_server.set_brightness_dimmed(streamdeck_serial, 10)
    assert api_server.get_brightness_dimmed(streamdeck_serial) == 10
    assert_state_saved(api_server)


def test_change_brightness(api_server, streamdeck_serial):
    """Test the brightness state was updated."""
    api_server.change_brightness(streamdeck_serial, -100)
    assert api_server.get_brightness(streamdeck_serial) == 0
    assert_state_saved(api_server)
    # check the dimmer was reset it
    dimmer = api_server.dimmers[streamdeck_serial]
    assert isinstance(dimmer, MagicMock)
    dimmer.reset.assert_called()


def test_display_timeout(api_server, streamdeck_serial):
    """Test the display timeout state was updated."""
    api_server.set_display_timeout(streamdeck_serial, 10)
    assert api_server.get_display_timeout(streamdeck_serial) == 10
    assert_state_saved(api_server)
