from unittest.mock import MagicMock, patch

import pytest

from tests.common import STREAMDECK_SERIAL, TestableStreamDeckServer, create_test_api_server


@pytest.fixture(autouse=True)
def mock_filters():
    """Mock filters used when button states changes. we mock the api version of them"""
    filter_classes = [
        "streamdeck_ui.api.TextFilter",
        "streamdeck_ui.api.BackgroundColorFilter",
        "streamdeck_ui.api.ImageFilter",
    ]
    mocks = {}
    for filter_class in filter_classes:
        mocks[filter_class] = MagicMock()
        patch(filter_class, mocks[filter_class]).start()

    yield mocks

    patch.stopall()


@pytest.fixture
def api_server() -> TestableStreamDeckServer:
    return create_test_api_server()


@pytest.fixture
def streamdeck_serial() -> str:
    return STREAMDECK_SERIAL
