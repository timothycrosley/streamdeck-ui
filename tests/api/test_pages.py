from unittest.mock import MagicMock

from tests.api.helpers import assert_state_saved


def test_add_new_page(api_server, streamdeck_serial):
    """test adding new pages"""
    api_server.add_new_page(streamdeck_serial)

    assert api_server.get_pages(streamdeck_serial) == [0, 1, 2]


def test_remove_pages_at_end(api_server, streamdeck_serial):
    """test remove pages at the end"""
    api_server.add_new_page(streamdeck_serial)
    api_server.remove_page(streamdeck_serial, 2)

    assert api_server.get_pages(streamdeck_serial) == [0, 1]


def test_remove_page_in_middle(api_server, streamdeck_serial):
    """test remove pages should present the page ids"""
    api_server.add_new_page(streamdeck_serial)
    api_server.add_new_page(streamdeck_serial)
    api_server.remove_page(streamdeck_serial, 1)
    api_server.remove_page(streamdeck_serial, 2)

    assert api_server.get_pages(streamdeck_serial) == [0, 3]


def test_remove_page_cannot_delete_last_page(api_server, streamdeck_serial):
    """test remove a page should do nothing if there is only one page"""
    api_server.remove_page(streamdeck_serial, 1)
    api_server.remove_page(streamdeck_serial, 0)

    assert api_server.get_pages(streamdeck_serial) == [0]


def test_adding_new_page_in_empty_page_id(api_server, streamdeck_serial):
    """Should add a page between page ids if does not exist"""
    api_server.add_new_page(streamdeck_serial)
    api_server.remove_page(streamdeck_serial, 1)
    api_server.add_new_page(streamdeck_serial)

    assert api_server.get_pages(streamdeck_serial) == [0, 1, 2]


def test_page(api_server, streamdeck_serial):
    """Test the page state was updated."""
    api_server.set_page(streamdeck_serial, 1)
    assert api_server.get_page(streamdeck_serial) == 1
    assert_state_saved(api_server)
    display_handler = api_server.display_handlers[streamdeck_serial]
    assert isinstance(display_handler, MagicMock)
    display_handler.set_page.assert_called()
    display_handler.synchronize.assert_called()


def test_set_non_existing_page(api_server, streamdeck_serial):
    """Test the page state was not updated."""
    page_before = api_server.get_page(streamdeck_serial)
    api_server.set_page(streamdeck_serial, 10)
    assert api_server.get_page(streamdeck_serial) == page_before
    display_handler = api_server.display_handlers[streamdeck_serial]
    assert isinstance(display_handler, MagicMock)
    display_handler.set_page.assert_not_called()
    display_handler.synchronize.assert_not_called()
