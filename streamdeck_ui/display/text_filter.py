import os
from streamdeck_ui.display.filter import Filter
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction
from streamdeck_ui.config import FONTS_PATH


class TextFilter(Filter):
    def __init__(self, size: Tuple[int, int], text: str, font: str):
        super(TextFilter, self).__init__(size)
        self.text = text
        self.true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)

    def transform(self, input: Image, time: Fraction):
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        draw = ImageDraw.Draw(input)

        label_w, label_h = draw.textsize(self.text, font=self.true_font)
        label_pos = ((input.width - label_w) // 2, input.height - 20)

        draw.text(label_pos, text=self.text, font=self.true_font, fill="white")

        return input
