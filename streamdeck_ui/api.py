from typing import Dict, List, Tuple, Union

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices import StreamDeck

state: Dict[str, Dict[int, Dict[str, str]]] = {}


def decks() -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    """Returns all decks we know about"""
    streamdecks: List[StreamDeck] = DeviceManager().enumerate()
    [deck.open() for deck in streamdecks]
    return {
        deck.id().decode(): {"type": deck.deck_type(), "layout": deck.key_layout()}
        for deck in streamdecks
    }


def set_button_text(deck_id: str, button: int, text: str) -> None:
    """Set the text associated with a button"""
    state.setdefault(deck_id, {}).setdefault(button, {})["text"] = text


def set_button_icon(deck_id: str, button: int, icon: str) -> None:
    """Sets the icon associated with a button"""
    state.setdefault(deck_id, {}).setdefault(button, {})["icon"] = icon
