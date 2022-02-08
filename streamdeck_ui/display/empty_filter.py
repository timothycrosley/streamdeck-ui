from fractions import Fraction
from typing import Tuple, Callable

from PIL import Image

from streamdeck_ui.display import filter


class EmptyFilter(filter.Filter):
    """
    This is the empty (base) filter where all pipelines start from.

    :param str name: The name of the filter. The name is useful for debugging purposes.
    """

    def __init__(self, size: Tuple[int, int]):
        super(EmptyFilter, self).__init__(size)
        self.image = Image.new("RGB", size)

    def transform(self, get_input: Callable[[], Image.Image], input_changed: bool, time: Fraction) -> Image.Image:
        """
        Returns an empty Image object.

        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.
        """
        if input_changed:
            return self.image
        else:
            return None
