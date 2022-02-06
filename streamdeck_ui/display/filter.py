from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Tuple

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
    def transform(self, input: Image, time: Fraction) -> Image:
        """
        Transforms the given input image to te desired output image.
        The default behaviour is to return the orignal image.

        :param PIL.Image input: The input image to transform.
        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.

        :rtype: PIL.Image
        :return: The transformed output image.
        """
        pass
