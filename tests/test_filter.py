import os
from fractions import Fraction

import pytest

from streamdeck_ui.display import empty_filter, image_filter, pipeline


def get_asset(file_name):
    """Resolve the given file name to a full path."""
    return os.path.join(os.path.dirname(__file__), "assets", file_name)


def test_default():
    default = empty_filter.EmptyFilter((32, 32))
    image = default.transform(None, Fraction(0))
    assert image is not None
    assert default.is_complete is False


# TODO: Incorrect file locations default to "empty". Probably better that it throws.
@pytest.mark.parametrize("image", ["smile.png", "smile.jpg", "smile.svg", "dog.gif"])
def test_image_filter(image: str):

    size = (72, 72)
    pipe = pipeline.Pipeline(size)

    pipe.add(empty_filter.EmptyFilter(size))
    time = Fraction(0)

    pipe.add(image_filter.ImageFilter(size, get_asset(image)))
    image = pipe.execute(time)
    image = pipe.execute(1)
    image = pipe.execute(2)


def test_pipeline():
    pipe = pipeline.Pipeline((32, 32))

    filter = image_filter.ImageFilter((32, 32), os.path.join(os.path.dirname(__file__), "assets/smile.png"))
    pipe.add(filter)
    final_image = pipe.execute()

    assert final_image is not None
