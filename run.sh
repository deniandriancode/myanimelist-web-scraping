#!/bin/bash

# DON'T RUN THIS SCRIPT YET! NEED TO APPLY MULTITHREADING IN PYTHON FIRST
source venv/bin/activate
python3 topanime.py &
python3 topmanga.py
deactivate
git add .
git commit -m "automated commit"
git push origin
