#!/usr/bin/env bash

echo Activate virtual env
. venv/bin/activate

echo Run tests
python3 manage.py test

echo Deactivate virtual env
deactivate
