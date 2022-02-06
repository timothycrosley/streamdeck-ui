from fractions import Fraction
from typing import List, Tuple

from PIL import Image

from streamdeck_ui.display.empty_filter import EmptyFilter
from streamdeck_ui.display.filter import Filter


class Pipeline:
    def __init__(self, size: Tuple[int, int]) -> None:
        self.filters: List[filter.Filter] = []
        self.filters.append(EmptyFilter(size))
        self.time = Fraction(0)

    def add(self, filter: Filter) -> None:
        self.filters.append(filter)

    def execute(self) -> Image:
        # TODO: Calculate new time value for pipeline run
        image = None
        for current_filter in self.filters:
            image = current_filter.transform(image, self.time)
        return image
