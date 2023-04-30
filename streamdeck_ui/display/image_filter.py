import itertools
import os
from fractions import Fraction
from io import BytesIO
from typing import Callable, Tuple

import cairosvg
import filetype
from PIL import Image, ImageSequence

from streamdeck_ui.display.filter import Filter


class ImageFilter(Filter):
    """
    Represents a static image. It transforms the input image by replacing it with a static image.
    """

    def __init__(self, file: str):
        super(ImageFilter, self).__init__()
        self.file = os.path.expanduser(file)

    def initialize(self, size: Tuple[int, int]):
        # Each frame needs to have a unique hashcode. Start with file name as baseline.
        image_hash = hash((self.__class__, self.file))
        frame_duration = []
        frame_hash = []

        try:
            kind = filetype.guess(self.file)
            if kind is None:
                svg_code = open(self.file).read()
                png = cairosvg.svg2png(svg_code, output_height=size[1], output_width=size[0])
                image_file = BytesIO(png)
                image = Image.open(image_file)
                frame_duration.append(-1)
                frame_hash.append(image_hash)
            else:
                image = Image.open(self.file)
                image.seek(0)
                # Frame number is used to create unique hash
                frame_number = 1
                while True:
                    try:
                        frame_duration.append(image.info["duration"])
                        # Create tuple and hash it, to combine the image and frame hashcodes
                        frame_hash.append(hash((image_hash, frame_number)))
                        image.seek(image.tell() + 1)
                        frame_number += 1
                    except EOFError:
                        # Reached the final frame
                        break
                    except KeyError:
                        # If the key 'duration' can't be found, it's not an animation
                        frame_duration.append(-1)
                        frame_hash.append(image_hash)
                        break

        except OSError as icon_error:
            # FIXME: caller should handle this?
            print(f"Unable to load icon {self.file} with error {icon_error}")
            image = Image.new("RGB", size)
            frame_duration.append(-1)
            frame_hash.append(image_hash)

        frames = ImageSequence.Iterator(image)

        # Scale all the frames to the target size
        self.frames = []
        for frame, milliseconds, hashcode in zip(frames, frame_duration, frame_hash):
            frame = frame.copy()
            frame.thumbnail(size, Image.LANCZOS)
            self.frames.append((frame, milliseconds, hashcode))

        self.frame_cycle = itertools.cycle(self.frames)
        self.current_frame = next(self.frame_cycle)
        self.frame_time = Fraction()

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        # Unpack tuple to make code a bit easier to understand
        frame, duration, hashcode = self.current_frame

        if duration >= 0 and time - self.frame_time > duration / 1000:
            self.frame_time = time
            self.current_frame = next(self.frame_cycle)

            # Unpack updated value
            frame, duration, hashcode = self.current_frame

            image = get_output(hashcode)
            if image:
                return (image, hashcode)

            input = get_input()
            if frame.mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(frame, frame)
            else:
                input.paste(frame)
            return (input, hashcode)

        if input_changed:
            image = get_output(hashcode)
            if image:
                return (image, hashcode)

            input = get_input()

            if frame.mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(frame, frame)
            else:
                input.paste(frame)
            return (input, hashcode)
        else:
            return (None, hashcode)
