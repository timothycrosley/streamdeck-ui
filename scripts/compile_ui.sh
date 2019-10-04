#!/bin/bash -xe

poetry run pyside2-uic streamdeck_ui/main.ui > streamdeck_ui/ui_main.py
