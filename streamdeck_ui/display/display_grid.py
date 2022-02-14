import threading
from time import sleep, time
from typing import Dict, Optional, List

from StreamDeck import ImageHelpers
from StreamDeck.Devices.StreamDeck import StreamDeck

from streamdeck_ui.display.pipeline import Pipeline
from streamdeck_ui.display.filter import Filter

from PIL import Image


class DisplayGrid:
    """
    A DisplayGrid is made up of a collection of pipelines, each processing
    filters for one individual button display.
    """

    def __init__(self, streamdeck: StreamDeck, pages: int, fps: int = 25):
        # Reference to the actual device, used to update icons
        self.streamdeck = streamdeck
        # TODO: Makes more sense that the display tells the filters what size
        # images to create than to have to create the filter with a size in mind.
        # This also means that filter creation and intialization needs to be
        # seperated. Maybe also needs a method to provide a thumbnail?
        self.size = streamdeck.key_image_format()["size"]

        # A dictionary of lists of pipelines. Each page has
        # a list, corresponding to each button.
        self.pages: Dict[int, Dict[int, Pipeline]] = {}

        # Initialize with a pipeline per key for all pages
        for page in range(pages):
            self.pages[page] = {}
            for button in range(self.streamdeck.key_count()):
                self.pages[page][button] = Pipeline(self.size)

        self.current_page: int = -1
        self.pipeline_thread: Optional[threading.Thread] = None
        self.quit = threading.Event()
        self.fps = fps
        # Configure the maximum frame rate we want to achieve
        self.time_per_frame = 1 / fps
        self.lock = threading.Lock()

    def replace(self, page: int, button: int, filters: List[Filter]):
        with self.lock:
            pipeline = Pipeline(self.size)
            for filter in filters:
                pipeline.add(filter)
            self.pages[page][button] = pipeline

    def add_filter(self, page: int, button: int, filter: Filter):
        with self.lock:
            self.pages[page][button].add(filter)

    def get_image(self, page: int, button: int) -> Image.Image:
        with self.lock:
            # FIXME: Consider returning not the last result, but an thumbnail
            # or something that represents the current "static" look of
            # a button. This will need to be added to the interface
            # of a filter.
            return self.pages[page][button].last_result()

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

                    # FIXME:
                    # This will be unbounded, old frames will need to be evicted
                    if hashcode not in frame_cache:
                        image = ImageHelpers.PILHelper.to_native_format(self.streamdeck, image)
                        frame_cache[hashcode] = image
                    else:
                        image = frame_cache[hashcode]

                    self.streamdeck.set_key_image(button, image)

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
                # TODO: push an event or callback so the UI can get access to this data
                #print(f"FPS: {frames} Execution time: {execution_time_ms} ms Execution %: {int(execution_time_ms/1000 * 100)}")
                #print(f"Output cache size: {len(frame_cache)}")
                #print(f"Pipeline cache size: {pipeline_cache_count}")
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

    def stop(self):
        if self.pipeline_thread is not None:
            self.quit.set()
            try:
                self.pipeline_thread.join()
            except RuntimeError:
                pass
            self.pipeline_thread = None
