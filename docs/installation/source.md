# Installation from Source

To install from source, you first need to install the dependencies and configure the udev rules (access to Elgato devices) according to your distribution guide.

## Follow the steps below to install the application from source:

1. Clone the repository:

```
git clone <https://github.com/streamdeck-linux-gui/streamdeck-linux-gui.git>

```

2. Change to the directory:

```
cd streamdeck-linux-gui

```

3. Build the package using the following command:

```
python -m build --wheel --no-isolation

```

4. Install the package on the system:

```
python -m installer -p $HOME/.local dist/*.whl

```

5. Execute the application:

```
streamdeck

```

# Uninstall

## Follow the steps below to uninstall the application:

1. Remove the application:

```
rm -rf $HOME/.local/bin/streamdeck
```

2. Remove the libraries:

```
rm -rf $HOME/.local/lib/${PYTHON_VERSION}/site-packages/streamdeck_*
```

where ${PYTHON_VERSION} is the Python version that you used to install the application.
