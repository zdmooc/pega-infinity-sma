#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Run server
python server.py

echo Deactivate virtual env
deactivate
