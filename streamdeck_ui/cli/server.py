import os
import sys
import optparse
import json
import socket
from threading import Event, Thread

from streamdeck_ui.cli.commands import create_command
from streamdeck_ui.api import StreamDeckServer

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
        if(self.quit.is_set()):
            return

        self.quit.set()
        try:
            self.cli_thread.join()
        except RuntimeError:
            pass

    def _run(self):
        try: # If streamdeck.sock already exists, destroy it and bind a new one.
            os.remove("/tmp/streamdeck_ui.sock")
        except OSError:
            pass
        self.sock.bind("/tmp/streamdeck_ui.sock")
        self.sock.listen(1)
        self.sock.settimeout(CLIStreamDeckServer.SOCKET_CONNECTION_TIMEOUT_SECOND)

        while not self.quit.is_set():
            try:
                conn, _ = self.sock.accept()
                cfg = read_json(conn)
                cmd = create_command(cfg)
                cmd.execute(self.api, self.ui)
                conn.close()
            except:
                pass
        try:
            os.remove("/tmp/streamdeck_ui.sock")
        except OSError:
            pass
        
def execute():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--page", type="int", dest="page_index", help="change to specified page (indice is from 1)", metavar="INDEX")
    (options, args) = parser.parse_args(sys.argv)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/streamdeck_ui.sock")
    data = None
    if(hasattr(options, "page_index")):
        data = {
            "command": "page_change",
            "page": options.page_index
        }
    
    if data is not None:
        write_json(sock, data)

