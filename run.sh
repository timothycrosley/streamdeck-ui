#!/bin/bash

source /opt/anaconda/bin/activate root
conda activate streamdeck
cd ~/streamdeck-ui && poetry run streamdeck
