from fractions import Fraction
from typing import Callable, Tuple

from PIL import Image

from streamdeck_ui.display import filter


class EmptyFilter(filter.Filter):
    """
    This is the empty (base) filter where all pipelines start from.

    :param str name: The name of the filter. The name is useful for debugging purposes.
    """

    def __init__(self):
        super(EmptyFilter, self).__init__()

        # For EmptyFilter - create a unique hashcode based on the name of the type
        # This will create "some value" that uniquely identifies this filter output
        # Since it never changes, this works.
        # Calculate it once for speed
        self.hashcode = hash(self.__class__)

    def initialize(self, size: Tuple[int, int]):
        self.image = Image.new("RGB", size)

    def transform(self, get_input: Callable[[], Image.Image], get_output: Callable[[int], Image.Image], input_changed: bool, time: Fraction) -> Tuple[Image.Image, int]:
        """
        Returns an empty Image object.

        :param Fraction time: The current time in seconds, expressed as a fractional number since
        the start of the pipeline.
        """
        if not input_changed:
            return (None, self.hashcode)
        return ((self.image), self.hashcode)
