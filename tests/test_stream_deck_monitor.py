import threading
from time import sleep
from unittest import TestCase
from unittest.mock import patch

from streamdeck_ui.stream_deck_monitor import StreamDeckMonitor


def test_start_stop():
    lock: threading.Lock = threading.Lock()
    monitor = StreamDeckMonitor(lock, lambda serial, deck: None, lambda serial: None)
    monitor.start()
    # FIXME: Need to find a better way to find "evidence" that it worked
    sleep(1)
    monitor.stop()
