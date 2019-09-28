from typing import Dict, List, Tuple, Union

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices import StreamDeck


def decks() -> Dict[str, Dict[str, Union[str, Tuple[int, int]]]]:
    """Returns all decks we know about"""
    streamdecks: List[StreamDeck] = DeviceManager().enumerate()
    [deck.open() for deck in streamdecks]
    return {
        deck.id().decode(): {"type": deck.deck_type(), "layout": deck.key_layout()}
        for deck in streamdecks
    }
