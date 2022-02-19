from threading import Event, Thread
from time import sleep
from StreamDeck import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from typing import Dict, Optional, Callable


class StreamDeckMonitor:
    """Periodically checks if Stream Decks are attached or
    removed and raises the corresponding events.
    """
    streamdecks : Dict[str, StreamDeck]
    "A dictionary with the key as device id and value as StreamDeck"

    monitor_thread : Optional[Thread]
    "The thread the monitors Stream Decks"

    def __init__(self, attached : Callable[[str, StreamDeck], None], detatched : Callable[[str], None]):
        """Creates a new StreamDeckMonitor instance

        :param attached: A callback function that is called when a new StreamDeck is attached. Note
        this runs on a background thread.
        :type attached: Callable[[StreamDeck], None]
        :param detatched: A callback function that is called when a previously attached StreamDeck
        is detatched. Note this runs on a background thread. The id of the device is passed as
        the only argument.
        :type detatched: Callable[[str], None]
        """
        self.quit = Event()
        self.streamdecks = {}
        self.monitor_thread = None
        self.attached = attached
        self.detatched = detatched

    def start(self):
        """Starts the monitor thread. If it is already running, nothing
        happens.
        """
        if not self.quit.is_set:
            return

        self.monitor_thread = Thread(target=self._run)
        # Won't prevent application from exiting, although we will always
        # attempt to gracefully shut down thread anyways
        self.monitor_thread.isDaemon = True
        self.quit.clear()
        self.monitor_thread.start()

    def stop(self):
        """Stops the monitor thread. If it is not running, nothing happens.
        Stopping will wait for the run thread to complete before returning.
        """
        if self.quit.is_set():
            return

        self.quit.set()
        try:
            self.monitor_thread.join()
        except RuntimeError:
            pass
        self.pipelmonitor_thread = None

        for streamdeck_id in self.streamdecks:
            self.detatched(streamdeck_id)

        self.streamdecks = {}

    def _run(self):
        """Runs the internal monitor thread until completion
        """
        while not self.quit.is_set():

            # REVIEW: Is it OK to enumerate and create decks each time? How expensive is it
            attached_streamdecks = DeviceManager.DeviceManager().enumerate()
            for streamdeck in attached_streamdecks:
                streamdeck_id = streamdeck.id()
                if streamdeck_id not in self.streamdecks:
                    self.streamdecks[streamdeck_id] = streamdeck
                    self.attached(streamdeck_id, streamdeck)

            for streamdeck_id in list(self.streamdecks.keys()):
                if streamdeck_id not in [deck.id() for deck in attached_streamdecks]:
                    streamdeck = self.streamdecks[streamdeck_id]
                    del self.streamdecks[streamdeck_id]
                    self.detatched(streamdeck_id)
            sleep(1)
