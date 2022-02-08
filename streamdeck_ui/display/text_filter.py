import os
from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from streamdeck_ui.config import FONTS_PATH
from streamdeck_ui.display.filter import Filter


class TextFilter(Filter):
    # Static instance - no need to create one per Filter instance
    font_blur = None

    def __init__(self, size: Tuple[int, int], text: str, font: str):
        super(TextFilter, self).__init__(size)
        self.text = text
        self.true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)
        # fmt: off
        kernel = [
            0, 1, 2, 1, 0,
            1, 2, 4, 2, 1,
            2, 4, 8, 4, 1,
            1, 2, 4, 2, 1,
            0, 1, 2, 1, 0]
        # fmt: on
        TextFilter.font_blur = ImageFilter.Kernel((5, 5), kernel, scale=0.1 * sum(kernel))
        self.offset = 0.0
        self.offset_direction = 1
        self.image = None
        self._create_text()

    def _create_text(self):
        self.image = Image.new("RGBA", self.size)
        backdrop_draw = ImageDraw.Draw(self.image)

        # TODO: The hard coded position should be improved
        # Note that you cannot simply take the height of the font
        # because it varies (for example, a "g" character) and
        # causes label alignment issues.
        label_w, label_h = backdrop_draw.textsize(self.text, font=self.true_font)
        label_pos = ((self.size[0] - label_w) // 2, self.size[1] - 20)

        backdrop_draw.text(label_pos, text=self.text, font=self.true_font, fill="black")
        self.image = self.image.filter(TextFilter.font_blur)

        foreground_draw = ImageDraw.Draw(self.image)
        foreground_draw.text(label_pos, text=self.text, font=self.true_font, fill="white")

    def transform(self, get_input: Callable[[], Image.Image], input_changed: bool, time: Fraction) -> Image.Image:
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        if input_changed:
            input = get_input()
            input.paste(self.image, self.image)
            return input
        return None
