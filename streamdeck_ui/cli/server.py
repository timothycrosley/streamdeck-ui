import os
import sys
import socket
from threading import Event, Thread

class CLIStreamDeckServer:
    SOCKET_CONNECTION_TIMEOUT_SECOND = 0.5

    def __init__(self):
        self.quit = Event()
        self.cli_thread = None

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
        while not self.quit.is_set():
            try:
                # handle cli request
                pass
            except:
                pass