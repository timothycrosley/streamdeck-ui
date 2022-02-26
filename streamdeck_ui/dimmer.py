import threading
from typing import Callable, Optional


class Dimmer:
    def __init__(self, timeout: int, brightness: int, brightness_dimmed: int, brightness_callback: Callable[[int], None]):
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
        self.dimmed = False
        "True if the Stream Deck is dimmed, False otherwise"
        self.__timer: Optional[threading.Timer] = None

    def stop(self) -> None:
        """Stops the dimmer and sets the brightness back to normal. Call
        reset to start normal dimming operation."""
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None

        try:
            self.brightness_callback(self.brightness)
        except Exception:
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

        if self.dimmed:
            self.brightness_callback(self.brightness)
            self.dimmed = False
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

        if toggle and self.dimmed:
            # Don't dim
            self.reset()
        elif self.__timer:
            # No need for the timer anymore, stop it
            self.__timer.cancel()
            self.__timer = None

            self.brightness_callback(self.brightness_dimmed)
            self.dimmed = True
