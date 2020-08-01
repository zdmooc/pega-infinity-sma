#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Run server
gunicorn config.wsgi

echo Deactivate virtual env
deactivate
