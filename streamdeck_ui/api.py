from typing import List, Dict

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices import StreamDeck



def decks() -> Dict[str, str]:
    """Returns all decks we know about"""
    streamdecks: List[StreamDeck] = DeviceManager().enumerate()
    [deck.open() for deck in streamdecks]
    return {deck.id().decode(): deck.deck_type() for deck in streamdecks}
