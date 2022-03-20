#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports streamdeck_ui/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py|ui_keypress.py|ui_commandwidget.py|ui_obs.py|ui_text.py|ui_brightness.py'
poetry run isort --check --diff streamdeck_ui/ tests/ --line-length 200 --skip ui_main.py --skip resources_rc.py --skip ui_settings.py --skip ui_keypress.py --skip ui_commandwidget.py --skip ui_obs.py --skip ui_text.py --skip ui_brightness.py
poetry run black --check --diff streamdeck_ui/ tests/ --line-length 200 --exclude 'ui_main.py|resources_rc.py|ui_settings.py|ui_keypress.py|ui_commandwidget.py|ui_obs.py|ui_text.py|ui_brightness.py'
poetry run flake8 streamdeck_ui/ tests/ --ignore F403,F401,W503 --exclude ui_main.py,resources_rc.py,ui_settings.py,ui_keypress.py,ui_commandwidget.py,ui_obs.py,ui_text.py,ui_brightness.py
poetry run safety check -i 39462 -i 40291 -i 44715
poetry run bandit -r streamdeck_ui/
