from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image, ImageEnhance

from streamdeck_ui.display.filter import Filter


class PulseFilter(Filter):
    def __init__(self):
        super(PulseFilter, self).__init__()
        self.last_time: Fraction = Fraction()
        self.pulse_delay = 0.5
        self.brightness = 1
        self.dim_brightness = 0.5
        self.filter_hash = hash(self.__class__)

    def initialize(self, size: Tuple[int, int]):
        pass

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        brightness_changed = False
        if time - self.last_time > self.pulse_delay:
            brightness_changed = True
            self.last_time = time

            if self.brightness == self.dim_brightness:
                self.brightness = 1
            else:
                self.brightness = self.dim_brightness

        frame_hash = hash((self.filter_hash, self.brightness))
        if input_changed or brightness_changed:
            image = get_output(frame_hash)
            if image:
                return (image, frame_hash)

            input = get_input()
            enhancer = ImageEnhance.Brightness(input)
            input = enhancer.enhance(self.brightness)
            return (input, frame_hash)
        return (None, frame_hash)
