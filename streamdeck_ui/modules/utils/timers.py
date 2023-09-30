from functools import partial

from PySide6.QtCore import QTimer


def debounce(timeout=500):
    """
    Decorator to debounce a function call.
    Each decorated function will have its own QTimer.
    """

    def decorator(func):
        timer = QTimer()
        timer.setSingleShot(True)

        def partial_func(*args, **kwargs):
            timer.timeout.disconnect()
            return func(*args, **kwargs)

        def wrapped(*args, **kwargs):
            if timer.isActive():
                timer.stop()
            timer.timeout.connect(partial(partial_func, *args, **kwargs))
            timer.start(timeout)

        return wrapped

    return decorator
