#!/bin/bash
set -euxo pipefail

poetry run isort streamdeck_ui/ tests/ --skip ui_main.py --skip resources_rc.py --skip ui_settings.py
poetry run black streamdeck_ui/ tests/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py' --line-length 200
