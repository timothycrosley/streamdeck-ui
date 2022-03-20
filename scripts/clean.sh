#!/bin/bash
set -euxo pipefail

poetry run isort streamdeck_ui/ tests/ --line-length 200 --skip ui_main.py --skip resources_rc.py --skip ui_settings.py --skip ui_keypress.py --skip ui_commandwidget.py --skip ui_obs.py --skip ui_text.py --skip ui_brightness.py
poetry run black streamdeck_ui/ tests/ --line-length 200 --exclude 'ui_main.py|resources_rc.py|ui_settings.py|ui_keypress.py|ui_commandwidget.py|ui_obs.py|ui_text.py|ui_brightness.py' 
