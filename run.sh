#!/bin/bash

source venv/bin/activate
python3 topanime.py 
python3 topmanga.py
python3 anime_recommendation.py
python3 manga_recommendation.py
deactivate
