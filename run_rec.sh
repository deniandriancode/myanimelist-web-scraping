#!/bin/bash

source venv/bin/activate
python3 anime_recommendation.py
python3 manga_recommendation.py
deactivate
git add .
git commit -m "automated commit"
git push origin
