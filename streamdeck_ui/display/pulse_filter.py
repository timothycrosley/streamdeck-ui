import random
from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image, ImageEnhance

from streamdeck_ui.display.filter import Filter


class PulseFilter(Filter):
    def __init__(self, size: Tuple[int, int]):
        super(PulseFilter, self).__init__(size)
        self.last_time: Fraction = Fraction()
        self.pulse_delay = 1 / 25
        self.brightness = random.uniform(0, 1)
        self.direction = -0.1

    def transform(self, get_input: Callable[[], Image.Image], input_changed: bool, time: Fraction) -> Image.Image:
        if time - self.last_time > self.pulse_delay:
            self.last_time = time
            self.brightness += self.direction
            if self.brightness < 0.5:
                self.brightness = 0.5
                self.direction *= -1

            if self.brightness > 1:
                self.brightness = 1
                self.direction *= -1
            input = get_input()
            enhancer = ImageEnhance.Brightness(input)
            input = enhancer.enhance(self.brightness)
            return input
        return None
