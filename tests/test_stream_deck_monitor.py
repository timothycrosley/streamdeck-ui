from unittest import TestCase
from time import sleep
from unittest.mock import patch
from streamdeck_ui.stream_deck_monitor import StreamDeckMonitor


def test_start_stop():
    monitor = StreamDeckMonitor()
    monitor.start()
    # FIXME: Need to find a better way to find "evidence" that it worked
    sleep(1)
    monitor.stop()


def test_new_deck():
    # TODO: How to mock this stuff? We need a function that can return
    # a list and change how it behaves on subsequent calls.
    monitor = StreamDeckMonitor()
    monitor.start()
    # FIXME: Need to find a better way to find "evidence" that it worked
    while True:
        sleep(1)
