#!/bin/bash -xe

poetry run mypy --ignore-missing-imports streamdeck_ui/
poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100 --recursive --check --diff --recursive streamdeck_ui/ tests/
poetry run black --check -l 100 streamdeck_ui/ tests/
poetry run flake8 streamdeck_ui/ tests/ --max-line 100 --ignore F403,F401,W503
poetry run safety check
poetry run bandit -r streamdeck_ui/
