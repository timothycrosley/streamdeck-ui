from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image, ImageEnhance

from streamdeck_ui.display.filter import Filter


class KeypressFilter(Filter):
    """This filter is applied whenever a key is being pressed"""

    def __init__(self):
        super(KeypressFilter, self).__init__()
        self.last_time: Fraction = Fraction()
        self.brightness = 1
        self.dim_brightness = 0.5
        self.filter_hash = hash(self.__class__)
        self.active = False
        self.last_state = False

    def initialize(self, size: Tuple[int, int]):
        self.blank_image = Image.new("RGB", size)
        self.size = size
        pass

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        frame_hash = hash((self.filter_hash, self.active))
        if input_changed or self.active != self.last_state:
            self.last_state = self.active
            image = get_output(frame_hash)
            if image:
                return (image, frame_hash)

            input = get_input()
            if self.active:
                input = get_input()
                background = self.blank_image.copy()
                input.thumbnail((self.size[0] - 10, self.size[1] - 10), Image.ANTIALIAS)
                # Reduce the image by 10px

                enhancer = ImageEnhance.Brightness(input)
                input = enhancer.enhance(2)
                # Light it up a bit

                background.paste(input, (5, 5))
                # Center the image

                return (background, frame_hash)
            else:
                return (input, frame_hash)
        return (None, frame_hash)
