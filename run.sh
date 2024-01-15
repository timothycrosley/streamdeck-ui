#!/bin/bash

source /opt/anaconda/bin/activate root
conda activate streamdeck
cd ~/streamdeck-ui 

python3 -m poetry run streamdeck &
sleep 3
kill $(pgrep -f "streamdeck/bin/python")
python3 -m poetry run streamdeck
