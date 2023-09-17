from unittest.mock import MagicMock, patch

import pytest

from streamdeck_ui.api import StreamDeckServer

STREAMDECK_SERIAL = "DL4XXXXXX"
STREAMDECK_KEY_COUNT = 3


def func_gen_page() -> dict:
    page = {}
    for i in range(0, STREAMDECK_KEY_COUNT):
        page[i] = {}
    return page


@pytest.fixture
def api_server():
    """Test the tear_up method."""
    api = StreamDeckServer()
    deck = MagicMock()
    deck.key_count.return_value = STREAMDECK_KEY_COUNT
    api.display_handlers[STREAMDECK_SERIAL] = MagicMock()
    api.decks[STREAMDECK_SERIAL] = deck
    api.state = {STREAMDECK_SERIAL: {"buttons": {0: func_gen_page()}}}
    return api


def test_add_new_page(api_server):
    """test adding new pages"""
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.add_new_page(STREAMDECK_SERIAL)

    assert api_server.get_pages(STREAMDECK_SERIAL) == [0, 1, 2]


def test_remove_pages_at_end(api_server):
    """test remove pages at the end"""
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.remove_page(STREAMDECK_SERIAL, 2)

    assert api_server.get_pages(STREAMDECK_SERIAL) == [0, 1]


def test_remove_page_in_middle(api_server):
    """test remove pages should present the page ids"""
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.remove_page(STREAMDECK_SERIAL, 1)
    api_server.remove_page(STREAMDECK_SERIAL, 2)

    assert api_server.get_pages(STREAMDECK_SERIAL) == [0, 3]


def test_remove_page_cannot_delete_last_page(api_server):
    """test remove a page should do nothing if there is only one page"""
    api_server.remove_page(STREAMDECK_SERIAL, 0)

    assert api_server.get_pages(STREAMDECK_SERIAL) == [0]


def test_adding_new_page_in_empty_page_id(api_server):
    """Should add a page between page ids if does not exist"""
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.add_new_page(STREAMDECK_SERIAL)
    api_server.remove_page(STREAMDECK_SERIAL, 1)
    api_server.add_new_page(STREAMDECK_SERIAL)

    assert api_server.get_pages(STREAMDECK_SERIAL) == [0, 1, 2]
