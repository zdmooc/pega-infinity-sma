#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Run server
python3 manage.py runserver

echo Deactivate virtual env
deactivate