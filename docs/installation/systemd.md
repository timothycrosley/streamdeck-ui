# systemd installation

Once you have a working streamdeck-linux-gui installation, you can also configure it to run as a systemd user service. It will automatically run when you login and you can manage it using `systemctl`.

## Installation

Make a directory where the systemd user configuration will be stored.

``` bash
mkdir -p $HOME/.local/share/systemd/user/
```

Create (an empty) configuration file.

``` bash
touch $HOME/.local/share/systemd/user/streamdeck.service
```

Use your favorite editor and paste the following content into the `streamdeck.service` file (rembember replace `<yourusername>`):

```ini
[Unit]
Description=A Linux compatible UI for the Elgato Stream Deck.

[Service]
Type=simple
ExecStart=/home/<yourusername>/.local/bin/streamdeck -n
Restart=on-failure

[Install]
WantedBy=default.target
```

To make the configuration take effect and install the service into systemd, run the following commands:

```bash
systemctl --user daemon-reload
systemctl --user enable streamdeck
```

> Tip: Before you continue, make sure you are not already running streamdeck-linux-gui. If it's open, click File > Exit. Only one instance of streamdeck-linux-gui can be running at a time.

You are now all set. To start the service, run the following command:

```bash
systemctl --user start streamdeck
```

There are some additional commands that may be useful.

To see the status of the service, run:

```bash
systemctl --user status streamdeck
```

To review the service log file (newest entries at the top) for troubleshooting, run:

```bash
journalctl --user -r
```

To stop the service, run:

```bash
systemctl --user stop streamdeck
```

## Installation in virtual environment

If you have installed streamdeck-linux-gui in a virtual environment, you can still use it in a systemd service.

Assume you are in the following directory:

```bash
/home/johnsmith/streamdeck-linux-gui
```

You create a virtual environment, called `.venv` and activate it as follows:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

and finally install streamdeck-linux-gui like this:

```bash
python3 -m pip install streamdeck-linux-gui
```

> Your virtual environment is now configured and located in `/home/johnsmith/streamdeck-linux-gui/.venv`

The steps for installing the systemd service is exactly the same. The only difference is you have to point the `ExecStart=` to the streamdeck executable inside the virtual environment, like so:

```ini
ExecStart=/home/johnsmith/streamdeck-linux-gui/.venv/bin/streamdeck -n
```

## Uninstalling

The following steps will stop, disable, remove the configuration file and finally reload the settings:

```bash
systemctl --user stop streamdeck
systemctl --user disable streamdeck
rm $HOME/.local/share/systemd/user/streamdeck.service
systemctl --user daemon-reload
```
