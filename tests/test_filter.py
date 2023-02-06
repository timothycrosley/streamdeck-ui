import os
from fractions import Fraction

import pytest

from streamdeck_ui.display import empty_filter, image_filter, pipeline


def get_asset(file_name):
    """Resolve the given file name to a full path."""
    return os.path.join(os.path.dirname(__file__), "assets", file_name)


def test_default():
    default = empty_filter.EmptyFilter()
    default.initialize((16, 16))
    image, _ = default.transform(lambda: None, lambda hash: None, True, Fraction(0))
    assert image is not None
    assert default.is_complete is False


# TODO: Incorrect file locations default to "empty". Probably better that it throws.
@pytest.mark.parametrize("image", ["smile.png", "smile.jpg", "smile.svg", "dog.gif"])
def test_image_filter(image: str):

    size = (72, 72)
    pipe = pipeline.Pipeline()

    filter = empty_filter.EmptyFilter()
    filter.initialize(size)

    pipe.add(filter)
    time = Fraction(0)

    filter = image_filter.ImageFilter(get_asset(image))
    filter.initialize(size)
    pipe.add(filter)
    image, _ = pipe.execute(time)
    image, _ = pipe.execute(1)
    image, _ = pipe.execute(2)


def test_pipeline():
    size = (72, 72)
    pipe = pipeline.Pipeline()

    filter = empty_filter.EmptyFilter()
    filter.initialize(size)
    pipe.add(filter)

    filter = image_filter.ImageFilter(os.path.join(os.path.dirname(__file__), "assets/smile.png"))
    filter.initialize(size)
    pipe.add(filter)
    time = Fraction(0)
    final_image, _ = pipe.execute(time)
    assert final_image is not None
