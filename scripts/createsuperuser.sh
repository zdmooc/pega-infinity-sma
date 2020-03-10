#!/usr/bin/env bash
echo Activate virtual env
. venv/bin/activate

echo Create superuser
python3 manage.py createsuperuser

echo Deactivate virtual env
deactivate