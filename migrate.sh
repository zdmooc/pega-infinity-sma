#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Run migrations
python3 manage.py migrate

echo Deactivate virtual env
deactivate