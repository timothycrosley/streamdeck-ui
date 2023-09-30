from unittest.mock import MagicMock


def assert_display_handler_used(api_server, streamdeck_serial):
    """Assert that the underline logic is called when the state is updated."""
    display_handler = api_server.display_handlers[streamdeck_serial]
    assert isinstance(display_handler, MagicMock)
    # the display_handler replace to update the filters of the button
    api_server.display_handlers[streamdeck_serial].replace.assert_called()
    # the display_handler synchronize to update the button
    api_server.display_handlers[streamdeck_serial].synchronize.assert_called()


def assert_display_handler_not_used(api_server, streamdeck_serial):
    """Assert that the underline logic is not called when the state is updated."""
    display_handler = api_server.display_handlers[streamdeck_serial]
    assert isinstance(display_handler, MagicMock)
    # the display_handler replace to update the filters of the button
    display_handler.replace.assert_not_called()
    # the display_handler synchronize to update the button
    display_handler.synchronize.assert_not_called()


def assert_state_saved(api_server):
    """Assert that the state was saved."""
    exposed_save_state = api_server.expose_save_state()
    exposed_save_state.assert_called()
