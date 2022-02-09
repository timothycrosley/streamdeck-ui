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

    def __init__(self, size: Tuple[int, int]):
        self.is_complete = False
        self.size = size

    @abstractmethod
    def transform(self, get_input: Callable[[], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        Transforms the given input image to te desired output image.
        The default behaviour is to return the orignal image.

        :param PIL.Image input: A function that returns the input image to transform. Note that calling
        this will create a copy of the input image, and it is safe to manipulate directly.
        :param bool input_changed: True if the input is different from previous run, False otherwise.
        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.

        :rtype: PIL.Image
        :return: The transformed output image. If this filter did not modify the input, return None. This signals to the
        pipeline manager that there was no change and a cached version will be moved to the next stage.
        """
        pass
