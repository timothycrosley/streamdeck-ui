from fractions import Fraction
from typing import List, Tuple

from PIL import Image

from streamdeck_ui.display import filter
from streamdeck_ui.display import empty_filter


class Pipeline:
    filters: List[filter.Filter] = []

    def __init__(self, size: Tuple[int, int]) -> None:
        self.filters.append(empty_filter.EmptyFilter((32, 32)))
        self.time = Fraction(0)

    def add(self, filter: filter.Filter) -> None:
        self.filters.append(filter)

    def execute(self) -> Image:
        # TODO: Calculate new time value for pipeline run
        image = None
        for current_filter in self.filters:
            image = current_filter.transform(image, self.time)
        return image
