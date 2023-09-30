from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ButtonState:
    text: str = ""
    """Text to display on the button"""
    icon: str = ""
    """Icon to display on the button"""
    keys: str = ""
    """Combination of keys, actionable by the button"""
    write: str = ""
    """Text to write, actionable by the button"""
    command: str = ""
    """Command to execute, actionable by the button"""
    switch_page: int = 0
    """Page to switch, actionable by the button"""
    switch_state: int = 0
    """Button state to switch, actionable by the button"""
    brightness_change: int = 0
    """Brightness percent change (-/+), actionable by the button"""
    text_vertical_align: str = ""
    """Vertical alignment of the text on the button"""
    text_horizontal_align: str = ""
    """Horizontal alignment of the text on the button"""
    font: str = ""
    """Font of the text on the button"""
    font_color: str = ""
    """Font color of the text on the button"""
    font_size: int = 0
    """Font size of the text on the button"""
    background_color: str = ""
    """Background color of the button"""


@dataclass
class ButtonMultiState:
    state: int = 0
    """Current displayed state of the button"""
    states: Dict[int, ButtonState] = field(default_factory=dict)
    """States of the button"""


@dataclass
class DeckState:
    buttons: Dict[int, Dict[int, ButtonMultiState]] = field(default_factory=dict)
    """State of Pages/buttons of the StreamDeck"""
    display_timeout: int = 1800
    """Timeout in seconds before dimming the StreamDeck display"""
    brightness: int = 100
    """"Brightness level of the StreamDeck"""
    brightness_dimmed: int = 0
    """Brightness level of the StreamDeck when dimmed"""
    rotation: int = 0
    """Rotation of the StreamDeck display"""
    page: int = 0
    """Current displayed page in the StreamDeck"""


@dataclass
class DeckStateV1:
    """Old DeckState class, used for backward compatibility"""

    buttons: Dict[int, Dict[int, ButtonState]] = field(default_factory=dict)
    """State of Pages/buttons of the StreamDeck"""
    display_timeout: int = 1800
    """Timeout in seconds before dimming the StreamDeck display"""
    brightness: int = 100
    """"Brightness level of the StreamDeck"""
    brightness_dimmed: int = 0
    """Brightness level of the StreamDeck when dimmed"""
    rotation: int = 0
    """Rotation of the StreamDeck display"""
    page: int = 0
    """Current displayed page in the StreamDeck"""
