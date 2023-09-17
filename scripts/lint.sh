#!/bin/bash
set -euo pipefail

# if arg --fix is passed, fix the code
enable_fix=0
black_flag="--check --diff"
isort_flag="--check --diff"
if [[ $# -eq 1 ]] && [[ $1 == "--fix" ]]; then
    enable_fix=1
    black_flag=""
    isort_flag=""
fi



poetry run mypy --ignore-missing-imports streamdeck_ui/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py'
poetry run isort $isort_flag streamdeck_ui/ tests/ --skip ui_main.py --skip resources_rc.py --skip ui_settings.py --line-length 200
poetry run black $black_flag streamdeck_ui/ tests/ --exclude 'ui_main.py|resources_rc.py|ui_settings.py' --line-length 200
poetry run flake8 streamdeck_ui/ tests/ --ignore F403,F401,W503 --exclude ui_main.py,resources_rc.py,ui_settings.py
poetry run safety check -i 39462 -i 40291 -i 44715 -i 47794 -i 51457
poetry run bandit -r streamdeck_ui/
