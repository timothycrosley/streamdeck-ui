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

        frame_duration = []

        try:
            kind = filetype.guess(self.file)
            if kind is None:
                svg_code = open(self.file).read()
                png = cairosvg.svg2png(svg_code, output_height=size[1], output_width=size[0])
                image_file = BytesIO(png)
                image = Image.open(image_file)
                frame_duration.append(-1)
            else:
                image = Image.open(self.file)
                image.seek(0)
                while True:
                    try:
                        frame_duration.append(image.info['duration'])
                        image.seek(image.tell() + 1)
                    except EOFError: 
                        # Reached the final frame
                        break
                    except KeyError:
                        # If the key 'duration' can't be found, it's not an animation
                        frame_duration.append(-1)
                        break

        except (OSError, IOError) as icon_error:
            # FIXME: caller should handle this?
            print(f"Unable to load icon {self.file} with error {icon_error}")
            image = Image.new("RGB", size)

        frames = ImageSequence.Iterator(image)

        # Scale all the frames to the target size
        self.frames = []
        for frame, milliseconds in zip(frames, frame_duration):
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

        if self.current_frame[1] >= 0 and time - self.frame_time > self.current_frame[1]/1000:
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
