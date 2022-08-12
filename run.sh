#!/usr/bin/env bash

# =======================================================================
# Make sure you have python virtual environment installed on your machine
# =======================================================================

if ! [[ -d venv ]]; then
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    deactivate
fi

source venv/bin/activate
python3 main.py
deactivate
