import time

from hypothesis_auto import auto_pytest_magic

from streamdeck_ui import api

server = api.StreamDeckServer()

auto_pytest_magic(server.set_button_command)
auto_pytest_magic(server.get_button_command)
auto_pytest_magic(server.set_button_switch_page)
auto_pytest_magic(server.get_button_switch_page)
auto_pytest_magic(server.set_button_keys)
auto_pytest_magic(server.get_button_keys)
auto_pytest_magic(server.set_button_write)
auto_pytest_magic(server.get_button_write)
auto_pytest_magic(server.set_brightness, auto_allow_exceptions_=(KeyError,))
auto_pytest_magic(server.get_brightness)
auto_pytest_magic(server.change_brightness, auto_allow_exceptions_=(KeyError,))
auto_pytest_magic(server.get_page)
