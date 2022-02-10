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

        # Each frame needs to have a unique hashcode. Start with file name as baseline.
        image_hash = hash((self.__class__, file))
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
                        frame_duration.append(image.info['duration'])
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

        except (OSError, IOError) as icon_error:
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
        self.frame_time = 0

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        The transformation returns the loaded image, ando overwrites whatever came before.
        """

        if self.current_frame[1] >= 0 and time - self.frame_time > self.current_frame[1]/1000:
            self.frame_time = time
            # FIXME: Unpack the current frame tuple
            self.current_frame = next(self.frame_cycle)

            image = get_output(self.current_frame[2])
            if image:
                return (image, self.current_frame[2])

            input = get_input()
            if self.current_frame[0].mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(self.current_frame[0], self.current_frame[0])
            else:
                input.paste(self.current_frame[0])
            return (input, self.current_frame[2])

        if input_changed:
            image = get_output(self.current_frame[2])
            if image:
                return (image, self.current_frame[2])
                
            input = get_input()

            if self.current_frame[0].mode == "RGBA":
                # Use the transparency mask of the image to paste
                input.paste(self.current_frame[0], self.current_frame[0])
            else:
                input.paste(self.current_frame[0])
            return (input, self.current_frame[2])
        else:
            return (None, self.current_frame[2])
