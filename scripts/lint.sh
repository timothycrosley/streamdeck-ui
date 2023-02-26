#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports streamdeck_ui/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py'
poetry run isort --check --diff streamdeck_ui/ tests/ --skip ui_main.py --skip resources_rc.py --skip ui_settings.py --line-length 200
poetry run black --check --diff streamdeck_ui/ tests/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py' --line-length 200
poetry run flake8 streamdeck_ui/ tests/ --ignore F403,F401,W503 --exclude ui_main.py,resources_rc.py,ui_settings.py
poetry run safety check -i 39462 -i 40291 -i 44715 -i 47794 -i 51457
poetry run bandit -r streamdeck_ui/
