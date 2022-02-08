from fractions import Fraction
from typing import List, Tuple

from PIL.Image import Image

from streamdeck_ui.display.empty_filter import EmptyFilter
from streamdeck_ui.display.filter import Filter


class Pipeline:
    def __init__(self, size: Tuple[int, int]) -> None:
        self.filters: List[Tuple[Filter, Image]] = []
        self.filters.append((EmptyFilter(size), None))
        self.time = Fraction(0)
        self.first_run = True

    def add(self, filter: Filter) -> None:
        self.filters.append((filter, None))
        self.first_run = True

    def execute(self) -> Image:
        """
        Executes all the filter in the pipeline and returns the final image, or None if the pipeline did not yield any changes.
        """

        # TODO: Calculate new time value for pipeline run
        image = None
        is_modified = False
        for i, (current_filter, cached) in enumerate(self.filters):
            image = current_filter.transform(lambda: image.copy(), is_modified | self.first_run, self.time)

            if not image:
                # Filter indicated that it did NOT change anything, pull up the last
                # cached value for the next step in the pipeline
                image = cached
            else:
                # The filter changed the image, cache it for future use
                # Update tuple with cached image
                self.filters[i] = (current_filter, image)
                is_modified = True

        if self.first_run:
            # Force an update the first time the pipeline runs
            is_modified = True
            self.first_run = False

        return image if is_modified else None

    def last_result(self) -> Image:
        """
        Returns the last known output of the pipeline
        """
        return self.filters[-1][1]
