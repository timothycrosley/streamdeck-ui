# Troubleshooting

> Note you may need to use `python`, `python3` or `python3.8` in the commands shown below, depending on your distribution. The examples simply use `python` for simplicity's sake.

## Basics
There are **four** important things you need to get a working system.

1. You need a working Python 3.8 or higher with pip installed.
2. You need to install hidapi.
3. You need a udev rule that allows access to your Stream Deck.
4. You need to install streamdeck-ui and all its dependencies with pip.

## Key Press and Write Text do not work
  Streamdeck uses [pynput](https://github.com/moses-palmer/pynput) for simulating **Key Presses** but it was not designed for [Wayland](https://github.com/moses-palmer/pynput/issues/189). Generally your results will be good when using X, but it seems like most new releases of Linux are switching away from it.

## ImportError

If you get an error such as:
```
ImportError: cannot import name 'QtWidgets' from 'PySide6'
```
This usually means a problem with PySide6. Try resolving with this:
``` console
python -m pip install --force-reinstall --no-cache-dir pyside6
```

## No System Tray Indicator
You may receive an error like this on start-up:
```
qt.core.qobject.connect: QObject::connect: No such signal QPlatformNativeInterface::systemTrayWindowChanged(QScreen*)
```

This is because gnome does not provide a System Tray out the box and you will need an extension
 [KStatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/) to make the system tray icon show up.

## Could not load the Qt platform plugin "xcb"

You may get the following error:
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
```
 On Ubuntu, resolve this problem by installing:
``` console
sudo apt install libxcb-xinerama0
```

On Arch, resolve this problem by installing:
```
sudo pacman -S qt6-base
```
You could also try [`qt5-x11extras`](https://archlinux.org/packages/extra/x86_64/qt5-x11extras/) if `qt6-base` didn't work for you.

## ModuleNotFoundError: No module named 'pkg_resources'
This module is part of `setuptools` but may be missing on your system.
```
python -m pip install setuptools
```


