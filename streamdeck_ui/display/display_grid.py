import threading
from time import sleep, time
from typing import Callable, Dict, List, Optional

from PIL import Image
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.Devices.StreamDeckOriginal import StreamDeckOriginal
from StreamDeck.ImageHelpers import PILHelper
from StreamDeck.Transport.Transport import TransportError

from streamdeck_ui.display.empty_filter import EmptyFilter
from streamdeck_ui.display.filter import Filter
from streamdeck_ui.display.keypress_filter import KeypressFilter
from streamdeck_ui.display.pipeline import Pipeline


class DisplayGrid:
    """
    A DisplayGrid is made up of a collection of pipelines, each processing
    filters for one individual button display.
    """

    _empty_filter: EmptyFilter = EmptyFilter()
    "Static instance of EmptyFilter shared by all pipelines"

    def __init__(self, lock: threading.Lock, streamdeck: StreamDeck, pages: int, cpu_callback: Callable[[str, int], None], fps: int = 25):
        """Creates a new display instance

        :param lock: A lock object that will be used to get exclusive access while enumerating
        Stream Decks. This lock must be shared by any object that will read or write to the
        Stream Deck.
        :type lock: threading.Lock
        :param streamdeck: The StreamDeck instance associated with this display
        :type streamdeck: StreamDeck
        :param pages: The number of logical pages (screen sets)
        :type pages: int
        :param cpu_callback: A function to call whenever the CPU changes
        :type cpu_callback: Callable[[str, int], None]
        :param fps: The desired FPS, defaults to 25
        :type fps: int, optional
        """
        self.streamdeck = streamdeck
        # Reference to the actual device, used to update icons

        if streamdeck.is_visual():
            self.size = streamdeck.key_image_format()["size"]
        else:
            self.size = (StreamDeckOriginal.KEY_PIXEL_WIDTH, StreamDeckOriginal.KEY_PIXEL_HEIGHT)
            # Default to original stream deck size - even though we're not actually going to display anything
        self.serial_number = streamdeck.get_serial_number()

        self.pages: Dict[int, Dict[int, Pipeline]] = {}
        # A dictionary of lists of pipelines. Each page has
        # a list, corresponding to each button.

        # Initialize with a pipeline per key for all pages
        for page in range(pages):
            self.pages[page] = {}
            for button in range(self.streamdeck.key_count()):
                self.pages[page][button] = Pipeline()

        self.current_page: int = -1
        self.pipeline_thread: Optional[threading.Thread] = None
        self.quit = threading.Event()
        self.fps = fps
        # Configure the maximum frame rate we want to achieve
        self.time_per_frame = 1 / fps
        self.lock = lock
        self.sync = threading.Event()
        self.cpu_callback = cpu_callback
        # The sync event allows a caller to wait until all the buttons have been processed
        DisplayGrid._empty_filter.initialize(self.size)

    def replace(self, page: int, button: int, filters: List[Filter]):
        with self.lock:
            pipeline = Pipeline()
            pipeline.add(DisplayGrid._empty_filter)
            for filter in filters:
                filter.initialize(self.size)
                pipeline.add(filter)
            keypress = KeypressFilter()
            keypress.initialize(self.size)
            pipeline.add(keypress)
            self.pages[page][button] = pipeline

    def get_image(self, page: int, button: int) -> Image.Image:
        with self.lock:
            # REVIEW: Consider returning not the last result, but a thumbnail
            # or something that represents the current "static" look of
            # a button. This will need to be added to the interface
            # of a filter.
            return self.pages[page][button].last_result()

    def set_keypress(self, button: int, active: bool):
        with self.lock:
            for filter in self.pages[self.current_page][button].filters:
                if isinstance(filter[0], KeypressFilter):
                    filter[0].active = active

    def synchronize(self):
        # Wait until the next cycle is complete.
        # To *guarantee* that you have one complete pass, two waits are needed.
        # The first gets you to the end of one cycle (you could have called it
        # mid cycle). The second gets you one pass through. Worst case, you
        # do two full cycles. Best case, you do 1 full and one partial.
        self.sync.wait()
        self.sync.wait()

    def _run(self):
        """Method that runs on background thread and updates the pipelines."""
        frames = 0
        start = time()
        last_page = -1
        execution_time = 0
        frame_cache = {}

        while not self.quit.isSet():
            current_time = time()

            with self.lock:
                page = self.pages[self.current_page]

            force_update = False

            if last_page != page:
                # When a page switch happen, force the pipelines to redraw so icons update
                force_update = True
                last_page = page

            pipeline_cache_count = 0

            for button, pipeline in page.items():
                # Process all the steps in the pipeline and return the resulting image
                with self.lock:
                    image, hashcode = pipeline.execute(current_time)

                pipeline_cache_count += len(pipeline.output_cache)

                # If none of the filters in the pipeline yielded a change, use
                # the last known result
                if force_update and image is None:
                    image = pipeline.last_result()

                if image:
                    # We cannot afford to do this conversion on every final frame.
                    # Since we want the flexibilty of a pipeline engine that can mutate the
                    # images along a chain of filters, the outcome can be somewhat unpredicatable
                    # For example - a clock that changes time or an animation that changes
                    # the frame and font that overlays. In many instances there is a finite
                    # number of frames per pipeline (a looping GIF with image, a pulsing icon etc)
                    # Some may also be virtually have infinite mutations. A cache per pipeline
                    # with an eviction policy of the oldest would likely suffice.
                    # The main problem is since the pipeline can mutate it's too expensive to
                    # calculate the actual hash of the final frame.
                    # Create a hash function that the filter itself defines. It has to
                    # update the hashcode with the unique attributes of the input it requires
                    # to make the frame. This could be time, text, frame number etc.
                    # The hash can then be passed to the next step and XOR'd or combined
                    # with the next hash. This yields a final hash code that can then be
                    # used to cache the output. At the end of the pipeline the hash can
                    # be checked and final bytes will be ready to pipe to the device.

                    if self.streamdeck.is_visual():
                        # FIXME: This will be unbounded, old frames will need to be evicted
                        if hashcode not in frame_cache:
                            image = PILHelper.to_native_format(self.streamdeck, image)
                            frame_cache[hashcode] = image
                        else:
                            image = frame_cache[hashcode]

                        try:
                            with self.lock:
                                self.streamdeck.set_key_image(button, image)
                        except TransportError:
                            # Review - deadlock if you wait on yourself?
                            self.stop()
                            pass
                            return

            self.sync.set()
            self.sync.clear()
            # Calculate how long we took to process the pipeline
            elapsed_time = time() - current_time
            execution_time += elapsed_time

            # Calculate how much we have to sleep between processing cycles to maintain the desired FPS
            # If we have less than 5ms left, don't bother sleeping, as the context switch and
            # overhead of sleeping/waking up is consumed
            time_left = self.time_per_frame - elapsed_time
            if time_left > 0.005:
                sleep(time_left)

            frames += 1
            if time() - start > 1.0:
                execution_time_ms = int(execution_time * 1000)
                if self.cpu_callback:
                    self.cpu_callback(self.serial_number, int(execution_time_ms / 1000 * 100))
                # execution_time_ms = int(execution_time * 1000)
                # print(f"FPS: {frames} Execution time: {execution_time_ms} ms Execution %: {int(execution_time_ms/1000 * 100)}")
                # print(f"Output cache size: {len(frame_cache)}")
                # print(f"Pipeline cache size: {pipeline_cache_count}")
                execution_time = 0
                frames = 0
                start = time()

    def set_page(self, page: int):
        """Switches to the given page. Pipelines for that page starts running,
        other page pipelines stop.

        Args:
            page (int): The page number to switch to.
        """
        with self.lock:
            if self.current_page >= 0:
                # Ensure none of the button filters are active anymore
                old_page = self.pages[self.current_page]
                for _, pipeline in old_page.items():
                    for filter in pipeline.filters:
                        if isinstance(filter[0], KeypressFilter):
                            filter[0].active = False
            # REVIEW: We could detect the active key on the last page, and make it active
            # on the target page
            self.current_page = page

    def start(self):
        if self.pipeline_thread is not None:
            self.quit.set()
            try:
                self.pipeline_thread.join()
            except RuntimeError:
                pass

        self.quit.clear()
        self.pipeline_thread = threading.Thread(target=self._run)
        self.pipeline_thread.daemon = True
        self.pipeline_thread.start()
        self.synchronize()
        # Wait for first frames to become ready

    def stop(self):
        if self.pipeline_thread is not None:
            self.quit.set()
            try:
                self.pipeline_thread.join()
            except RuntimeError:
                pass
            self.pipeline_thread = None
