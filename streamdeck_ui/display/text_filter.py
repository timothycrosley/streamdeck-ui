import os
from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from streamdeck_ui.config import FONTS_PATH
from streamdeck_ui.display.filter import Filter


class TextFilter(Filter):
    font_blur: ImageFilter.Kernel = None
    # Static instance - no need to create one per Filter instance

    image: Image

    def __init__(self, text: str, font: str, vertical_align: str):
        super(TextFilter, self).__init__()
        self.text = text
        self.vertical_align = vertical_align
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

        # Hashcode should be created for anything that makes this frame unique
        self.hashcode = hash((self.__class__, text, font, vertical_align))

    def initialize(self, size: Tuple[int, int]):
        self.image = Image.new("RGBA", size)
        backdrop_draw = ImageDraw.Draw(self.image)

        # Calculate the height and width of the text we're drawing, using the font itself
        label_w, _ = backdrop_draw.textsize(self.text, font=self.true_font)

        # Calculate dimensions for text that include ascender (above the line)
        # and below the line  (descender) characters. This is used to adust the
        # font placement and should allow for button text to horizontally align
        # across buttons. Basically we want to figure out what is the tallest
        # text we will need to draw.
        _, label_h = backdrop_draw.textsize("lLpgyL|", font=self.true_font)

        gap = (size[1] - 5 * label_h) // 4

        if self.vertical_align == "top":
            label_y = 0
        elif self.vertical_align == "middle-top":
            label_y = gap + label_h
        elif self.vertical_align == "middle":
            label_y = size[1] // 2 - (label_h // 2)
        elif self.vertical_align == "middle-bottom":
            label_y = (gap + label_h) * 3
        else:
            label_y = size[1] - label_h
            # Default or "bottom"

        label_pos = ((size[0] - label_w) // 2, label_y)

        backdrop_draw.text(label_pos, text=self.text, font=self.true_font, fill="black")
        self.image = self.image.filter(TextFilter.font_blur)

        foreground_draw = ImageDraw.Draw(self.image)
        foreground_draw.text(label_pos, text=self.text, font=self.true_font, fill="white")

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        if input_changed:
            image = get_output(self.hashcode)
            if image:
                return (image, self.hashcode)

            input = get_input()
            input.paste(self.image, self.image)
            return (input, self.hashcode)
        return (None, self.hashcode)
