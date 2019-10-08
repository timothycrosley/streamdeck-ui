#!/bin/bash -xe

./scripts/lint.sh
poetry run pytest -s --cov=streamdeck_ui/ --cov=tests --cov-report=term-missing ${@} --cov-report xml
