#!/bin/bash -xe

poetry run pyside6-uic streamdeck_ui/main.ui --from-imports streamdeck_ui -o streamdeck_ui/ui_main.py
poetry run pyside6-uic streamdeck_ui/settings.ui --from-imports streamdeck_ui -o streamdeck_ui/ui_settings.py
poetry run pyside6-uic streamdeck_ui/button.ui --from-imports streamdeck_ui -o streamdeck_ui/ui_button.py
poetry run pyside6-rcc streamdeck_ui/resources.qrc -o streamdeck_ui/resources_rc.py