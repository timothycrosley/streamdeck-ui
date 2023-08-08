import json
import optparse
import os
import socket
import sys
import tempfile
from threading import Event, Thread

from streamdeck_ui.api import StreamDeckServer
from streamdeck_ui.cli.commands import create_command


def read_json(sock: socket.socket) -> dict:
    header = sock.recv(4)
    num_bytes = int.from_bytes(header, "little")

    return json.loads(sock.recv(num_bytes))


def write_json(sock: socket.socket, data: dict) -> None:
    binary_data = json.dumps(data).encode("utf-8")
    num_bytes = len(binary_data)

    sock.send(num_bytes.to_bytes(4, "little"))
    sock.send(binary_data)


class CLIStreamDeckServer:
    SOCKET_CONNECTION_TIMEOUT_SECOND = 0.5

    def __init__(self, api: StreamDeckServer, ui):
        self.quit = Event()
        self.cli_thread = None

        self.api = api
        self.ui = ui

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def start(self):
        if not self.quit.is_set:
            return

        self.cli_thread = Thread(target=self._run)
        self.quit.clear()
        self.cli_thread.start()

    def stop(self):
        if self.quit.is_set():
            return

        self.quit.set()
        try:
            self.cli_thread.join()
        except RuntimeError:
            pass

    def _run(self):
        try:
            tmpdir = tempfile.gettempdir()
            filename = "streamdeck_ui.sock"

            saved_umask = os.umask(0o077)
            path = os.path.join(tmpdir, filename)

            if os.path.exists(path):
                os.remove(path)

            self.sock.bind(path)
            self.sock.listen(1)
            self.sock.settimeout(CLIStreamDeckServer.SOCKET_CONNECTION_TIMEOUT_SECOND)
        except OSError:
            print("warning: for some reason, unable to utilize CLI commands.")
            pass

        while not self.quit.is_set():
            try:
                conn, _ = self.sock.accept()
                cfg = read_json(conn)
                cmd = create_command(cfg)
                cmd.execute(self.api, self.ui)
                conn.close()
            except BaseException:
                pass
        try:
            os.remove(path)
        except OSError:
            pass
        finally:
            os.umask(saved_umask)


def execute():
    parser = optparse.OptionParser()

    parser.add_option(
        "-a",
        "--action",
        type="string",
        dest="action",
        help="the action to be performed. valid options (case-insensitive): " + "SET_PAGE, SET_BRIGHTNESS, SET_TEXT, SET_ALIGNMENT, SET_CMD, SET_KEYS, SET_WRITE, SET_ICON, CLEAR_ICON",
        metavar="NAME",
    )

    parser.add_option("-d", "--deck", type="int", dest="deck_index", help="the deck to be manipulated. defaults to the currently selected deck in the ui", metavar="INDEX")
    parser.add_option("-p", "--page", type="int", dest="page_index", help="the page to be manipulated. defaults to the currently active page", metavar="INDEX")
    parser.add_option("-b", "--button", type="int", dest="button_index", help="the button to be manipulated", metavar="INDEX")

    parser.add_option("--icon", type="string", dest="icon_path", help="path to an icon. used with SET_ICON", metavar="PATH")
    parser.add_option("--brightness", type="int", dest="brightness", help="brightness to set, 0-100. used with SET_BRIGHTNESS", metavar="VALUE")
    parser.add_option("--text", type="string", dest="button_text", help="button text to set. used with SET_TEXT", metavar="VALUE")
    parser.add_option("--write", type="string", dest="button_write", help="text to be written when the button is pressed. used with SET_WRITE", metavar="VALUE")
    parser.add_option("--command", type="string", dest="button_cmd", help="button command to set. used with SET_CMD", metavar="VALUE")
    parser.add_option("--keys", type="string", dest="button_keys", help="button keys to set. used with SET_KEYS", metavar="VALUE")
    parser.add_option(
        "--alignment", type="string", dest="button_text_alignment", help="button text alignment. used with SET_ALIGNMENT. valid values: top, middle-top, middle, middle-bottom, bottom", metavar="VALUE"
    )

    (options, args) = parser.parse_args(sys.argv)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    tmpdir = tempfile.gettempdir()
    file = "streamdeck_ui.sock"
    path = os.path.join(tmpdir, file)
    sock.connect(path)
    data = None

    if options.action is not None:
        action_name = options.action.lower()
        if action_name == "set_page":
            if options.page_index is None:
                print("error: --page not set...")
                return
            data = {"command": "set_page", "deck": options.deck_index, "page": options.page_index}
        elif action_name == "set_brightness":
            if options.brightness is None:
                print("error: --brightness not set...")
                return
            data = {"command": "set_brightness", "deck": options.deck_index, "value": options.brightness}
        elif action_name == "set_text":
            if options.button_text is None:
                print("error: --text not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_button_text", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "text": options.button_text}
        elif action_name == "set_write":
            if options.button_write is None:
                print("error: --write not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_button_write", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "write": options.button_write}
        elif action_name == "set_alignment":
            if options.button_text_alignment is None:
                print("error: --alignment not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_alignment", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "alignment": options.button_text_alignment}
        elif action_name == "set_cmd":
            if options.button_cmd is None:
                print("error: --command not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_button_cmd", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "button_cmd": options.button_cmd}
        elif action_name == "set_keys":
            if options.button_keys is None:
                print("error: --keys not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_button_keys", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "button_keys": options.button_keys}
        elif action_name == "set_icon":
            if options.icon_path is None:
                print("error: --icon not set...")
                return
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "set_button_icon", "deck": options.deck_index, "page": options.page_index, "button": options.button_index, "icon": options.icon_path}
        elif action_name == "clear_icon":
            if options.button_index is None:
                print("error: --button not set...")
                return
            data = {"command": "clear_button_icon", "deck": options.deck_index, "page": options.page_index, "button": options.button_index}

    if data is not None:
        write_json(sock, data)
