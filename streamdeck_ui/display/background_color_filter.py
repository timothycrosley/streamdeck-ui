from fractions import Fraction
from typing import Tuple, Callable, Optional

from streamdeck_ui.display.filter import Filter

from PIL import Image, ImageColor


class BackgroundColorFilter(Filter):
    def __init__(self, color: str):
        super(BackgroundColorFilter, self).__init__()
        self.image = None
        self.color = to_rgb(color)
        self.hashcode = hash((self.__class__, self.color))

    def initialize(self, size: Tuple[int, int]):
        self.image = Image.new("RGB", size)
        self.image.paste(self.color, (0, 0, size[0], size[1]))

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image],
                  input_changed: bool, time: Fraction) -> Tuple[Optional[Image.Image], int]:
        if not input_changed:
            return None, self.hashcode
        return self.image, self.hashcode


def to_rgb(hex_str: str) -> tuple[int, ...]:
    """
    Converts a hex string or a color string to an RGB tuple.
    """
    if hex_str.startswith("#"):
        hex_str = hex_str.lstrip("#")
        return tuple(int(hex_str[i: i + 2], 16) for i in (0, 2, 4))
    return ImageColor.getrgb(hex_str)
