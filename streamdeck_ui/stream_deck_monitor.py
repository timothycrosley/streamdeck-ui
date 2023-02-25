from threading import Event, Lock, Thread
from time import sleep
from typing import Callable, Dict, Optional

from StreamDeck import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.Transport.Transport import TransportError


class StreamDeckMonitor:
    """Periodically checks if Stream Decks are attached or
    removed and raises the corresponding events.
    """

    streamdecks: Dict[str, StreamDeck]
    "A dictionary with the key as device id and value as StreamDeck"

    monitor_thread: Optional[Thread]
    "The thread the monitors Stream Decks"

    def __init__(self, lock: Lock, attached: Callable[[str, StreamDeck], None], detached: Callable[[str], None]):
        """Creates a new StreamDeckMonitor instance

        :param lock: A lock object that will be used to get exclusive access while enumerating
        Stream Decks. This lock must be shared by any object that will read or write to the
        Stream Deck.
        :type lock: threading.Lock
        :param attached: A callback function that is called when a new StreamDeck is attached. Note
        this runs on a background thread.
        :type attached: Callable[[StreamDeck], None]
        :param detached: A callback function that is called when a previously attached StreamDeck
        is detached. Note this runs on a background thread. The id of the device is passed as
        the only argument.
        :type detached: Callable[[str], None]
        """
        self.quit = Event()
        self.streamdecks = {}
        self.monitor_thread = None
        self.attached = attached
        self.detached = detached
        self.lock = lock

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
            self.detached(streamdeck_id)

        self.streamdecks = {}

    def _run(self):
        """Runs the internal monitor thread until completion"""
        showed_open_help: bool = False
        showed_enumeration_help: bool = False
        showed_libusb_help: bool = False
        while not self.quit.is_set():
            with self.lock:
                attached_streamdecks = []
                try:
                    attached_streamdecks = DeviceManager.DeviceManager().enumerate()
                    showed_libusb_help = False
                except DeviceManager.ProbeError:
                    if not showed_libusb_help:
                        print("\n------------------------")
                        print("*** Problem detected ***")
                        print("------------------------")
                        print("A suitable LibUSB installation could not be found.")
                        print("Check installation instructions:")
                        print("https://github.com/timothycrosley/streamdeck-ui")
                        showed_libusb_help = True

                        # No point showing the next help if we can't even enumerate
                        showed_enumeration_help = True
                        continue

                if len(attached_streamdecks) == 0:
                    if not showed_enumeration_help:
                        print("No Stream Deck(s) detected. Attach a Stream Deck.")
                        showed_enumeration_help = True
                else:
                    showed_enumeration_help = False

            # Look for new StreamDecks
            for streamdeck in attached_streamdecks:
                streamdeck_id = streamdeck.id()
                if streamdeck_id not in self.streamdecks:
                    try:
                        self.attached(streamdeck_id, streamdeck)
                        self.streamdecks[streamdeck_id] = streamdeck
                        showed_open_help = False
                    except TransportError:
                        if not showed_open_help:
                            print("\n------------------------")
                            print("*** Problem detected ***")
                            print("------------------------")
                            print("A Stream Deck is attached, but it could not be opened.")
                            print("Check installation instructions and ensure a udev rule has been added and loaded.")
                            print("https://github.com/timothycrosley/streamdeck-ui")
                            showed_open_help = True
                        pass

            # Look for suspended/resumed StreamDecks
            for streamdeck in list(self.streamdecks.values()):
                # Note that streamdeck.connected() will enumerate the devices attached.
                # Enumeration must not be done while other device operations on other
                # threads are running. Protect with the lock.
                # Note that it will only enumerate when is_open() returns false (short circuit),
                # so it won't do it uncessarily anyways.

                # Use a flag so we don't hold the lock while executing callback
                failed_but_attached = False
                with self.lock:
                    if not streamdeck.is_open() and streamdeck.connected():
                        failed_but_attached = True

                # The recovery strategy is to treat this as a detach and let the
                # next enumeration pick up the device and reinitialize.
                if failed_but_attached:
                    del self.streamdecks[streamdeck.id()]
                    self.detached(streamdeck.id())

            # Remove unplugged StreamDecks
            for streamdeck_id in list(self.streamdecks.keys()):
                if streamdeck_id not in [deck.id() for deck in attached_streamdecks]:
                    streamdeck = self.streamdecks[streamdeck_id]
                    del self.streamdecks[streamdeck_id]
                    self.detached(streamdeck_id)
            sleep(1)
