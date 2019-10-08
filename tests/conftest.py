from unittest.mock import MagicMock

from streamdeck_ui import api

api.DeviceManager = MagicMock()
api.StreamDeck = MagicMock()
api.ImageHelpers = MagicMock()
api.export_config = MagicMock()
