from time import sleep

import pytest

from streamdeck_ui.dimmer import Dimmer


@pytest.mark.parametrize("brightness, dim_percent, dimmed", [(100, 0, 0), (100, 50, 50), (100, 100, 100), (50, 50, 25)])
def test_dim_to_zero(brightness: int, dim_percent: int, dimmed: int):

    call_count = 0
    last_value = -1

    def dim(value: int):
        nonlocal last_value
        nonlocal call_count
        call_count = call_count + 1
        last_value = value

    dimmer = Dimmer(1, brightness, dim_percent, dim)
    dimmer.reset()
    sleep(1.1)
    assert dimmer.dimmed
    assert call_count == 2
    assert last_value == dimmed
