# Installation from Source

To install from source, you first need to install the dependencies and configure the udev rules (access to Elgato devices) according to your distribution guide.

## Follow the steps below to install the application from source

Clone the repository:

```bash
git clone <https://github.com/streamdeck-linux-gui/streamdeck-linux-gui.git>
```

Change to the directory:

```bash
cd streamdeck-linux-gui
```

Build the package using the following command:

```bash
python -m build --wheel --no-isolation
```

Install the package on the system:

```bash
python -m installer -p $HOME/.local dist/*.whl
```

Execute the application:

```bash
streamdeck
```

# Uninstall

## Follow the steps below to uninstall the application

Remove the application:

```bash
rm -rf $HOME/.local/bin/streamdeck
```

Remove the libraries:

```bash
rm -rf $HOME/.local/lib/${PYTHON_VERSION}/site-packages/streamdeck_*
```

where ${PYTHON_VERSION} is the Python version that you used to install the application.
