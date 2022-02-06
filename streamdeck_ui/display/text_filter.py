import os
from streamdeck_ui.display.filter import Filter
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fractions import Fraction
from streamdeck_ui.config import FONTS_PATH


class TextFilter(Filter):
    # Static instance - no need to create one per Filter instance
    font_blur = None

    def __init__(self, size: Tuple[int, int], text: str, font: str):
        super(TextFilter, self).__init__(size)
        self.text = text
        self.true_font = ImageFont.truetype(os.path.join(FONTS_PATH, font), 14)
        kernel = [
            0, 1, 2, 1, 0,
            1, 2, 4, 2, 1,
            2, 4, 8, 4, 1,
            1, 2, 4, 2, 1,
            0, 1, 2, 1, 0]
        TextFilter.font_blur = ImageFilter.Kernel((5, 5), kernel, scale=0.1 * sum(kernel))

    def transform(self, input: Image, time: Fraction):
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        blurred = Image.new('RGBA', input.size)
        backdrop_draw = ImageDraw.Draw(blurred)

        # TODO: The hard coded position should be improved
        # Note that you cannot simply take the height of the font
        # because it varies (for example, a "g" character) and
        # causes label alignment issues.
        label_w, label_h = backdrop_draw.textsize(self.text, font=self.true_font)
        label_pos = ((input.width - label_w) // 2, input.height - 20)

        backdrop_draw.text(label_pos, text=self.text, font=self.true_font, fill="black")
        blurred = blurred.filter(TextFilter.font_blur)

        # Apply the blurred font backdrop and use itself as a mask too (second arg)
        input.paste(blurred, blurred)

        draw = ImageDraw.Draw(input)
        draw.text(label_pos, text=self.text, font=self.true_font, fill="white")

        return input
