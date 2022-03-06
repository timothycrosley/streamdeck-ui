#!/bin/bash -xe

poetry run pyside2-uic streamdeck_ui/main.ui --from-imports streamdeck_ui -o streamdeck_ui/ui_main.py
poetry run pyside2-uic streamdeck_ui/settings.ui --from-imports streamdeck_ui -o streamdeck_ui/ui_settings.py
poetry run pyside2-rcc streamdeck_ui/resources.qrc -o streamdeck_ui/resources_rc.py

poetry run pyside2-uic streamdeck_ui/actions/command/commandwidget.ui --from-imports streamdeck_ui -o streamdeck_ui/actions/command/ui_commandwidget.py
poetry run pyside2-uic streamdeck_ui/actions/text/text.ui --from-imports streamdeck_ui -o streamdeck_ui/actions/text/ui_text.py
poetry run pyside2-uic streamdeck_ui/actions/keypress/keypress.ui --from-imports streamdeck_ui -o streamdeck_ui/actions/keypress/keypress.py
