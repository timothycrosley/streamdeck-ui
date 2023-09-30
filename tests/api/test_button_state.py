from tests.api.helpers import assert_display_handler_not_used, assert_display_handler_used, assert_state_saved


def test_button_text(api_server, streamdeck_serial):
    """Test the button text state was updated."""
    api_server.set_button_text(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_text(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_icon(api_server, streamdeck_serial):
    """Test the button icon state was updated."""
    api_server.set_button_icon(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_icon(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_keys(api_server, streamdeck_serial):
    """Test the button keys state was updated."""
    api_server.set_button_keys(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_keys(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_button_write(api_server, streamdeck_serial):
    """Test the button write state was updated."""
    api_server.set_button_write(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_write(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_button_command(api_server, streamdeck_serial):
    """Test the button command state was updated."""
    api_server.set_button_command(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_command(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_button_font_color(api_server, streamdeck_serial):
    """Test the button font color state was updated."""
    api_server.set_button_font_color(streamdeck_serial, 0, 0, "#FFF000")
    assert api_server.get_button_font_color(streamdeck_serial, 0, 0) == "#FFF000"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_font_size(api_server, streamdeck_serial):
    """Test the button font size state was updated."""
    api_server.set_button_font_size(streamdeck_serial, 0, 0, 20)
    assert api_server.get_button_font_size(streamdeck_serial, 0, 0) == 20
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_font(api_server, streamdeck_serial):
    """Test the button font state was updated."""
    api_server.set_button_font(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_font(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_text_vertical_align(api_server, streamdeck_serial):
    """Test the button text vertical align state was updated."""
    api_server.set_button_text_vertical_align(streamdeck_serial, 0, 0, "middle")
    assert api_server.get_button_text_vertical_align(streamdeck_serial, 0, 0) == "middle"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_text_horizontal_align(api_server, streamdeck_serial):
    """Test the button text horizontal align state was updated."""
    api_server.set_button_text_horizontal_align(streamdeck_serial, 0, 0, "test")
    assert api_server.get_button_text_horizontal_align(streamdeck_serial, 0, 0) == "test"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_background_color(api_server, streamdeck_serial):
    """Test the button background color state was updated."""
    api_server.set_button_background_color(streamdeck_serial, 0, 0, "#FFF000")
    assert api_server.get_button_background_color(streamdeck_serial, 0, 0) == "#FFF000"
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_switch_page(api_server, streamdeck_serial):
    """Test the button switch page state was updated."""
    api_server.set_button_switch_page(streamdeck_serial, 0, 0, 1)
    assert api_server.get_button_switch_page(streamdeck_serial, 0, 0) == 1
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_button_change_brightness(api_server, streamdeck_serial):
    """Test the button change brightness state was updated."""
    api_server.set_button_change_brightness(streamdeck_serial, 0, 0, 10)
    assert api_server.get_button_change_brightness(streamdeck_serial, 0, 0) == 10
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_button_state(api_server, streamdeck_serial):
    """Test the button state was updated."""
    api_server.set_button_state(streamdeck_serial, 0, 0, 1)
    assert api_server.get_button_state(streamdeck_serial, 0, 0) == 1
    assert_state_saved(api_server)
    assert_display_handler_used(api_server, streamdeck_serial)


def test_button_switch_state(api_server, streamdeck_serial):
    """Test the button switch state was updated."""
    api_server.set_button_switch_state(streamdeck_serial, 0, 0, 1)
    assert api_server.get_button_switch_state(streamdeck_serial, 0, 0) == 1
    assert_state_saved(api_server)
    assert_display_handler_not_used(api_server, streamdeck_serial)


def test_add_new_button_state(api_server, streamdeck_serial):
    """Test adding new button state."""
    api_server.add_new_button_state(streamdeck_serial, 0, 0)
    assert api_server.get_button_states(streamdeck_serial, 0, 0) == [0, 1, 2, 3]


def test_remove_button_state_at_end(api_server, streamdeck_serial):
    """Test removing button state at the end."""
    api_server.remove_button_state(streamdeck_serial, 0, 0, 2)

    assert api_server.get_button_states(streamdeck_serial, 0, 0) == [0, 1]


def test_remove_button_state_in_middle(api_server, streamdeck_serial):
    """Test removing button state in the middle."""
    api_server.remove_button_state(streamdeck_serial, 0, 0, 1)

    assert api_server.get_button_states(streamdeck_serial, 0, 0) == [0, 2]


def test_remove_button_state_cannot_delete_last_button_state(api_server, streamdeck_serial):
    """Test removing button state should do nothing if there's only one button state."""
    api_server.remove_button_state(streamdeck_serial, 0, 0, 2)
    api_server.remove_button_state(streamdeck_serial, 0, 0, 1)
    api_server.remove_button_state(streamdeck_serial, 0, 0, 0)

    assert api_server.get_button_states(streamdeck_serial, 0, 0) == [0]
