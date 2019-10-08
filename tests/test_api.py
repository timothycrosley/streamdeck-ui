from hypothesis_auto import auto_pytest_magic

from streamdeck_ui import api

auto_pytest_magic(api.set_button_command)
auto_pytest_magic(api.get_button_command)
auto_pytest_magic(api.set_button_switch_page)
auto_pytest_magic(api.get_button_switch_page)
auto_pytest_magic(api.set_button_keys)
auto_pytest_magic(api.get_button_keys)
auto_pytest_magic(api.set_button_write)
auto_pytest_magic(api.get_button_write)
auto_pytest_magic(api.set_brightness, auto_allow_exceptions_=(KeyError,))
auto_pytest_magic(api.get_brightness)
auto_pytest_magic(api.change_brightness, auto_allow_exceptions_=(KeyError,))
auto_pytest_magic(api.set_page)
auto_pytest_magic(api.get_page)
auto_pytest_magic(api.render)
