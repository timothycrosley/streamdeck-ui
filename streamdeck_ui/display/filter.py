from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image


class Filter(ABC):
    """
    A filter transforms a given input image to the desired output image. A filter can signal that it
    is complete and will be removed from the pipeline.

    :param str name: The name of the filter. The name is useful for debugging purposes.
    """

    size: Tuple[int, int]
    "The image size (width, height) in pixels that this filter transforms."

    is_complete: bool
    "Indicates if the filter is complete and should no longer be processed."

    def __init__(self):
        self.is_complete = False

    @abstractmethod
    def initialize(self, size: Tuple[int, int]):
        """Initializes the filter with the provided frame size. Since the construction
        of the filter can happen before the size of the display is known, initialization
        should be done here.

        :param size: The filter image size
        :type size: Tuple[int, int]
        """
        pass

    @abstractmethod
    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        Transforms the given input image to the desired output image.
        The default behaviour is to return the orignal image.

        :param Callable[[], PIL.Image] get_input: A function that returns the input image to transform. Note that calling
        this will create a copy of the input image, and it is safe to manipulate directly.

        :param Callable[[int], PIL.Image] get_output: Provide the hashcode of the new frame and it will
        return the output frame if it already exists. This avoids having to redraw an output frame that is already
        cached.

        :param bool input_changed: True if the input is different from previous run, False otherwise.
        When true, you have to return an Image.

        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.

        :rtype: PIL.Image
        :return: The transformed output image. If this filter did not modify the input, return None. This signals to the
        pipeline manager that there was no change and a cached version will be moved to the next stage.
        """
        pass
