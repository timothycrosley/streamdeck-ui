import threading
from typing import Callable


class Dimmer:
    def __init__(self, timeout: int = 0, brightness: int = -1, brightness_dimmed: int = -1, brightness_callback: Callable[[int], None] = None):
        """Constructs a new Dimmer instance

        :param int timeout: The time in seconds before the dimmer starts.
        :param int brightness: The normal brightness level.
        :param Callable[[int], None] brightness_callback: Callback that receives the current
                                                          brightness level.
        """
        self.timeout = timeout
        self.brightness = brightness
        self.brightness_dimmed = brightness_dimmed
        self.brightness_callback = brightness_callback
        self.__stopped = False
        self.__dimmed = False
        self.__timer = None

    def stop(self) -> None:
        """Stops the dimmer and sets the brightness back to normal. Call
        reset to start normal dimming operation."""
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None

        try:
            self.brightness_callback(self.brightness)
        except KeyError:
            # During detach cleanup, this is likely to happen
            pass
        self.__stopped = True

    def reset(self) -> bool:
        """Reset the dimmer and start counting down again. If it was busy dimming, it will
        immediately stop dimming. Callback fires to set brightness back to normal."""

        self.__stopped = False
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None

        if self.timeout:
            self.__timer = threading.Timer(self.timeout, self.dim)
            self.__timer.start()

        if self.__dimmed:
            self.brightness_callback(self.brightness)
            self.__dimmed = False
            if self.brightness_dimmed < 20:
                # The screen was "too dark" so reset and let caller know
                return True

        return False
        # Returning false means "I didn't have to reset it"

    def dim(self, toggle: bool = False):
        """Manually initiate a dim event.
        If the dimmer is stopped, this has no effect."""

        if self.__stopped:
            return

        if toggle and self.__dimmed:
            # Don't dim
            self.reset()
        elif self.__timer:
            # No need for the timer anymore, stop it
            self.__timer.cancel()
            self.__timer = None

            self.brightness_callback(self.brightness_dimmed)
            self.__dimmed = True
