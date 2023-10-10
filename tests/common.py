from unittest.mock import MagicMock

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.model import ButtonMultiState, ButtonState, DeckState

STREAMDECK_SERIAL = "DL4XXXXXX"
STREAMDECK_KEY_COUNT = 3
STREAMDECK_TYPE = "Stream Deck Original"

# the number of pages in the test state
PAGES = 3


def func_gen_page() -> dict:
    page = {}
    for i in range(0, PAGES):
        page[i] = ButtonMultiState(
            state=0,
            states={key_id: ButtonState(text=f"State {key_id}") for key_id in range(0, STREAMDECK_KEY_COUNT)},
        )
    return page


class TestableStreamDeckServer(StreamDeckServer):
    """A testable version of the StreamDeckServer."""

    def __init__(self):
        super().__init__()

    def expose_save_state(self):
        return self._save_state


def create_test_api_server() -> TestableStreamDeckServer:
    """Created a testable version of the StreamDeckServer.
    with some default values."""
    api = TestableStreamDeckServer()
    deck = MagicMock()
    deck.key_layout.return_value = (1, 1)
    deck.key_count.return_value = STREAMDECK_KEY_COUNT
    display_handler = MagicMock()
    display_handler.get_image.return_value = None
    api.display_handlers[STREAMDECK_SERIAL] = display_handler

    api.decks_by_serial[STREAMDECK_SERIAL] = deck
    api.dimmers[STREAMDECK_SERIAL] = MagicMock()

    api.state = {
        STREAMDECK_TYPE: DeckState(
            buttons={
                0: func_gen_page(),
                1: func_gen_page(),
                2: func_gen_page(),
            },
        ),
        STREAMDECK_SERIAL: DeckState(
            buttons={
                0: func_gen_page(),
                1: func_gen_page(),
            },
        ),
    }
    # we don't want to save the state to disk
    api._save_state = MagicMock()
    api.export_config = MagicMock()
    api.import_config = MagicMock()
    return api
