# Troubleshooting

## Basics
There are **four** important things you need to get a working system.

1. You need a working Python 3.8 or higher with pip installed.
2. You need to install hidapi.
3. You need a udev rule that allows access to your Stream Deck.
4. You need to install streamdeck-ui and all its dependencies with pip.

## ImportError

If you get an error such as `ImportError: cannot import name 'QtWidgets' from 'PySide6'` you can try this:
``` console
python -m pip install --force-reinstall --no-cache-dir pyside6
```
> note you may need to use `python3` or `python3.8` etc based on your distribution

## No System Tray Indicator
You may receive an error like this on start-up.
`qt.core.qobject.connect: QObject::connect: No such signal QPlatformNativeInterface::systemTrayWindowChanged(QScreen*)`

This is because gnome does not provide a System Tray out the box and you will need an extension
 [KStatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/) to make the system tray icon show up.

## Key Press and Write Text does not work
  Streamdeck uses [pynput](https://github.com/moses-palmer/pynput) for simulating **Key Presses** but it was not designed for [Wayland](https://github.com/moses-palmer/pynput/issues/189). Generally your results will be good when using X, but it seems like most new releases of Linux are switching away from it.