#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports streamdeck_ui/
poetry run isort --check --diff streamdeck_ui/ tests/ --skip ui_main.py
poetry run black --check streamdeck_ui/ tests/ --exclude ui_main.py
poetry run flake8 streamdeck_ui/ tests/ --ignore F403,F401,W503 --exclude ui_main.py
poetry run safety check -i 39462
poetry run bandit -r streamdeck_ui/
