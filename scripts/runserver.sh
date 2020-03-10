#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Run server
python3 manage.py runserver 0.0.0.0:8000

echo Deactivate virtual env
deactivate