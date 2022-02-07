import threading
from time import time
from typing import Dict
from StreamDeck import ImageHelpers
from StreamDeck.Devices.StreamDeck import StreamDeck
from streamdeck_ui.display.pipeline import Pipeline


class DisplayGrid:
    """
    A DisplayGrid is made up of a collection of pipelines, each processing
    filters for one individual button display.
    """
    def __init__(self, streamdeck: StreamDeck, fps: int = 25):
        # Reference to the actual device, used to update icons
        self.streamdeck = streamdeck
        # A dictionary of lists of pipelines. Each page has
        # a list, corresponding to each button.
        self.pages: Dict[int, Dict[int, Pipeline]] = {}
        self.current_page: int = None
        self.pipeline_thread: threading.Thread = None
        self.running = False
        self.fps = fps

    def set_pipeline(self, page: int, button: int, pipeline: Pipeline):
        # TODO: Do we need to lock before manipulating?
        page_dict = self.pages.setdefault(page, {})
        page_dict.setdefault(button, pipeline)

    def get_pipeline(self, page: int, button: int) -> Pipeline:
        return self.pages[page][button]

    def _run(self):
        """Method that runs on background thread and updates the pipelines."""
        frames = 0
        start = time()
        while self.running:
            page = self.pages[self.current_page]

            for button, pipeline in page.items():

                image = pipeline.execute()
                image = ImageHelpers.PILHelper.to_native_format(self.streamdeck, image)

                # TODO: Should the last step convert it? What about UI?
                self.streamdeck.set_key_image(button, image)

            frames += 1
            if time() - start > 1.0:
                print(f"FPS: {frames}")
                frames = 0
                start = time()

    def set_page(self, page: int):
        """Switches to the given page. Pipelines for that page starts running,
        other page pipelines stop.

        Args:
            page (int): The page number to switch to.
        """
        self.current_page = page

    def start(self):
        if self.pipeline_thread is not None:
            self.running = False
            try:
                self.pipeline_thread.join()
            except RuntimeError:
                pass

        self.running = True
        self.pipeline_thread = threading.Thread(target=self._run)
        self.pipeline_thread.daemon = True
        self.pipeline_thread.start()

    def stop(self):

        if self.pipeline_thread is not None:
            self.running = False
            try:
                self.pipeline_thread.join()
            except RuntimeError:
                pass
