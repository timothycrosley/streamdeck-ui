import os
import sys
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
        self.sock.bind("/tmp/streamdeck.sock")
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
            os.remove("/tmp/streamdeck.sock")
        except OSError:
            pass