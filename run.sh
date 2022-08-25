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

if [[ -f myanimelist.log ]]; then
    rm myanimelist.log
fi

source venv/bin/activate
python3 topanime.py
python3 topmanga.py
python3 anime_recommendation.py
python3 manga_recommendtaion.py
python3 anime_review.py
python3 manga_review.py
deactivate
