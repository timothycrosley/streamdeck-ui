from fractions import Fraction
from io import BytesIO
import itertools
from typing import Callable, Tuple

import cairosvg
import filetype
from PIL import Image, ImageSequence

from streamdeck_ui.display.filter import Filter


class ImageFilter(Filter):
    """
    Represents a static image. It transforms the input image by replacing it with a static image.
    """

    def __init__(self, size: Tuple[int, int], file: str):
        super(ImageFilter, self).__init__(size)
        self.file = file
        self.image = None

        try:
            kind = filetype.guess(self.file)
            if kind is None:
                svg_code = open(self.file).read()
                png = cairosvg.svg2png(svg_code, output_height=size[1], output_width=size[0])
                image_file = BytesIO(png)
                self.image = Image.open(image_file)
                # TODO: refactor and remove self.image
                frames = ImageSequence.Iterator(self.image)
            else:
                rgba_icon = Image.open(self.file)

                self.frame_timestamp = [0]

                rgba_icon.seek(0)
                frames_n = 1
                while True:
                    try:
                        self.frame_timestamp.append(self.frame_timestamp[-1]+rgba_icon.info['duration'])
                        rgba_icon.seek(rgba_icon.tell() + 1)
                        frames_n += 1
                    except EOFError:  # end of gif
                        # frames_n -= 1
                        break
                    except KeyError:  # no gif
                        break
                frames = ImageSequence.Iterator(rgba_icon)

                if len(self.frame_timestamp) > 1:
                    del self.frame_timestamp[0]

        except (OSError, IOError) as icon_error:
            # FIXME: caller should handle this?
            print(f"Unable to load icon {self.file} with error {icon_error}")
            self.image = Image.new("RGB", size)

        # Scale all the frames to the target size
        self.frames = []
        for frame, milliseconds in zip(frames, self.frame_timestamp):
            frame = frame.copy()
            frame.thumbnail(size, Image.LANCZOS)
            self.frames.append((frame, milliseconds))

        self.frame_cycle = itertools.cycle(self.frames)

        self.current_frame = next(self.frame_cycle)
        self.frame_time = 0

    def transform(self, get_input: Callable[[], Image.Image], input_changed: bool, time: Fraction) -> Image.Image:
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        if time - self.frame_time > self.current_frame[1]/1000:
            self.frame_time = time
            self.current_frame = next(self.frame_cycle)
            input = get_input()
            if self.current_frame[0].mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(self.current_frame[0], self.current_frame[0])
            else:
                input.paste(self.current_frame[0])
            return input

        if input_changed:
            input = get_input()

            if self.current_frame[0].mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(self.current_frame[0], self.current_frame[0])
            else:
                input.paste(self.current_frame[0])
            return input
        else:
            return None
