#!/bin/bash
set -euxo pipefail

poetry run isort streamdeck_ui/ tests/
poetry run black streamdeck_ui/ tests/
