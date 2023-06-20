#!/bin/bash

source /opt/anaconda/bin/activate root
conda activate streamdeck
cd ~/streamdeck-ui 
python3 -m poetry run streamdeck
