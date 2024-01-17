#!/bin/bash

source /opt/anaconda/bin/activate root
conda create -n streamdeck python=3.8
conda activate streamdeck
cd ~/streamdeck-ui 
pip3 install poetry pynput PySide2 pillow StreamDeck cairosvg filetype obsws-python
